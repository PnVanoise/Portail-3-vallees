import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import json
import os
import numpy as np
from datetime import datetime
import sqlalchemy 

import logging
from logging.handlers import RotatingFileHandler

# GET DIRECTORY PATH
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(script_dir, 'config.json')

# LOG FILE
log_file = os.path.join(script_dir,'import_data.log')
log_level = logging.INFO
max_file_size = 1024 * 1024  # 1 Mo
backup_count = 5

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# LOG FILES ROTATION
# Custom filename for rotated log files
log_file_rotated = "/home/portail/Portail-3-vallees/import_data_{}.log".format(backup_count)

handler = RotatingFileHandler(log_file, mode='a', maxBytes=max_file_size, backupCount=backup_count, encoding=None, delay=False)
handler.setLevel(log_level)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Set the custom filename for rotated log files
handler.rotator = lambda source, dest: log_file_rotated
logger.addHandler(handler)

logger.info("Start import data")

# Load configuration from JSON file
with open(config_file_path, 'r') as config_file:
    config_data = json.load(config_file)

# Extract database connection parameters from config
db_host = config_data.get("db_host", "")
db_name = config_data.get("db_name", "")
db_user = config_data.get("db_user", "")
db_password = config_data.get("db_password", "")

# CONNECT TO DATABASE
try:
    conn = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()
    print("Connected to the database!")
    logger.info("Connected to the database!")
except Exception as e:
    print("Error connecting to the database:", e)
    logger.error("Error connecting to the database:", e)

# LOOP THROUGH DATA SOURCES
for lsource, source_data in config_data.get("data_sources", {}).items():
    ldir = source_data.get('csv_folder', '')
    header = source_data.get('csv_header', '')

    # GET AND STORE FIELD MAPPING FROM CONFIG FILE
    column_mapping = source_data.get("csv_columns", {})
    column_indexes = list(column_mapping.values())

    # LOOP THROUGH FILES IN DATA SOURCE FOLDER (SORT BY DATE)
    for lfile in sorted(os.listdir(ldir), key=lambda x: os.path.getmtime(os.path.join(ldir, x))):
        if not lfile.endswith(".csv"):
            print("Skipping file:", lfile, "(not a CSV file)")
            logger.info("Skipping file:" + lfile + "(not a CSV file)")
            continue

        if os.path.getsize(os.path.join(ldir, lfile)) == 0:
            print("Skipping file:", lfile, "(Empty file)")
            logger.info("Skipping file:" + lfile + "(Empty file)")
            continue

        column_mapping = source_data.get("csv_columns", {})
        print("Processing file " + lfile)
        logger.info("Processing file " + lfile)

        if "SMS" in lfile:
            print("Skipping file " + lfile + " (contains 'SMS' in the name)")
            logger.info("Skipping file " + lfile + " (contains 'SMS' in the name)")
            continue

        if header == "TRUE":
            data = pd.read_csv(ldir + '/' + lfile, usecols=column_indexes, header=None, skiprows=1)
        else:
            data = pd.read_csv(ldir + '/' + lfile, usecols=column_indexes, header=None)

        data = data.rename(columns=dict(zip(column_indexes, column_mapping.keys())))
        
        # data = pd.DataFrame.from_dict(zip(column_indexes, column_mapping.keys()))
        csv_device = str(data['id_device'].unique()[0])
        
        # CHECK IF THE DEVICE EXISTS AND IS PRESENT ON A REGISTERED ANIMAL
        query = "select followdem.cor_animal_devices.id_device from followdem.cor_animal_devices left join followdem.t_devices on followdem.cor_animal_devices.id_device = followdem.t_devices.id_device where followdem.cor_animal_devices.date_end is null and ref_device= '"+csv_device+"'"
        cursor.execute(query)
        row = cursor.fetchone()
        
        if row is not None:
            
            print("The device "+csv_device+" exists in the database")
            logger.info("The device "+csv_device+" exists in the database")    
            id_device = row[0]

            # REMOVE DATA WHERE LONG, LAT OR ALTITUDE ARE NULL
            data = data[(data['longitude'] != 0) & (data['latitude'] != 0) & (data['altitude'] != 0) & (data['datatype'].isin(['GPS', 'GPRS']))]
            
            # IF COLUMN DATATYPE, REMOVE NON GPS DATATYPES AND REMOVE COLUMN
            if 'datatype' in data.columns:
                # FILTER ROWS BY 'datatype' COLUMN
                data = data[data['datatype'].isin(['GPS', 'GPRS'])]
                # REMOVE 'datatype' COLUMN
                data.drop('datatype', axis=1, inplace=True)
            if data.empty:
                print("Skipping file " + lfile + " (empty file)")
                logger.info("Skipping file " + lfile + " (empty file)")
                continue
                
            # REPLACE REF_DEVICE BY ID_DEVICE
            data['id_device'] = id_device

            # MAKE SURE EACH COLUMN IS THE RIGHT TYPE
            if 'gps_date' in data.columns:
                data['gps_date'] = pd.to_datetime(data['gps_date'])
            if 'longitude' in data.columns:
                data['longitude'] = pd.to_numeric(data['longitude'])
            if 'latitude' in data.columns:
                data['latitude'] = pd.to_numeric(data['latitude'])
            if 'hdop' in data.columns:
                data['hdop'] = pd.to_numeric(data['hdop'])
            if 'sat_number' in data.columns:
                data['sat_number'] = data['sat_number'].astype(int)
            if 'altitude' in data.columns:
                data['altitude'] = pd.to_numeric(data['altitude'])
            if 'temperature' in data.columns:
                data['temperature'] = pd.to_numeric(data['temperature'])
            if 'dimension' in data.columns:
                data['dimension'] = data['dimension'].astype(str)
            if 'ttf' in data.columns:
                data['ttf'] = data['ttf'].astype(int)
            if 'accurate' in data.columns:
                data['accurate'] = data['accurate'].astype(bool)

            # CONVERT DATAFRAME TO TUPLES
            data_tuples = [tuple(row.values()) for row in data.to_dict(orient='records')]

            # DEFINE INSERT QUERY
            insert_query = """
                INSERT INTO followdem.t_gps_data
                ({columns})
                VALUES ({placeholders})
            """

            # EXTRACT COLUMNS AND PLACEHOLDERS
            columns = ', '.join(data.columns)
            placeholders = ', '.join(['%s'] * len(data.columns))

            # BATCH INSERT
            try:
                cursor.executemany(
                    insert_query.format(columns=columns, placeholders=placeholders),
                    data_tuples
                )
                conn.commit()
                print("Insertion successful : "+str(len(data))+" rows inserted")
                logger.info("Insertion successful : "+str(len(data))+" rows inserted")

                # SUPPRIMER LE CSV
                try:
                    os.remove(ldir+'/'+lfile)
                    print(lfile+" deleted")
                    logger.info(lfile+" deleted")
                except Exception as e:
                    print("Error deleting the file:", e)
                    logger.info("Error deleting the file:", e)

            except Exception as e:
                print("Error inserting data:", e)
                logger.info("Error inserting data:", e)
                conn.rollback()

        else:
            print("The device "+csv_device+" is absent from the database, the file "+lfile+" will not be transfered")
            logger.info("The device "+csv_device+" is absent from the database, the file "+lfile+" will not be transfered")
            
            # Move the unprocessed file to the 'unprocessed' subdirectory
            try:
                unprocessed_dir = os.path.join(ldir, "unprocessed")
                if not os.path.exists(unprocessed_dir):
                    os.mkdir(unprocessed_dir)

                os.rename(os.path.join(ldir, lfile), os.path.join(unprocessed_dir, lfile))
                print("File " + lfile + " moved to 'unprocessed' directory")
                logger.info("File " + lfile + " moved to 'unprocessed' directory")
            except Exception as e:
                print("Error moving the file to 'unprocessed' directory:", e)
                logger.info("Error moving the file to 'unprocessed' directory:", e)

# REFRESH MATERIALIZED VIEWS
# query = "REFRESH MATERIALIZED VIEW followdem.vm_animals_loc WITH DATA;"
#cursor.execute(query)
#print("Materialized view refreshed!")
#logger.info("Materialized view refreshed!")
logger.info("Completed import data")

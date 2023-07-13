###############################################################################
#     CONFIGURATION
###############################################################################

# Base de données
db_host= "localhost"
db_name = "followdem"
db_user = "bddgps"
db_password = "bdd_GPS2023"


# Interface carto
MAPCONFIG: {
    "CENTER": [45.4, 6.8],
    "ZOOM_DEFAULT": 10,
    "ZOOM_MAX": 16,
    "BASEMAP": [
        {
            "name": "Scan 25 IGN",
            "url": "https://wxs.ign.fr/4lpxv93m9i5p68oiceh6knu2/geoportail/wmts?LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS&EXCEPTIONS=text/xml&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}",
            "attribution": "&copy IGN"
        },
        {
            "name": "Ortho IGN",
            "url": "https://wxs.ign.fr/essentiels/geoportail/wmts?LAYER=ORTHOIMAGERY.ORTHOPHOTOS&EXCEPTIONS=text/xml&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}",
            "attribution": "IGN-F/Geoportail"
        },
        {
            "name": "Parcelles cadastrales IGN",
            "url": "https://wxs.ign.fr/essentiels/geoportail/wmts?&layer=CADASTRALPARCELS.PARCELLAIRE_EXPRESS&FORMAT=image/png&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}",
            "attribution": "IGN-F/Geoportail"
        },
        {
            "name": "OpenstreetMap",
            "url": "//{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
            "attribution": "OSM contributors"
        }
    ]
}

# Sources des données (csv)
# chaque section data_source définit une source de données
# La section csv_columns donne la correspondance entre les colonnes du csv et les colonnes de la table t_gps_data
# id_device, gps_date,ttf,temperature,sat_number,hdop,latitude,longitude,altitude,dimension,accurate

data_sources = {
	"ornitela":{
		"csv_folder":"/home/ftpgps/data_ornitela",
		"csv_columns" : {
			"id_device":0,
			"gps_date":1,
			"temperature":15,
			"sat_number":5,
			"hdop":9,
			"latitude":10,
			"longitude":11,
			"altitude":12,
			"datatype":4
		},
		"csv_header":"TRUE"
	},
	"biotrack":{
		"csv_folder":"/home/ftpgps/data_biotrack",
		"csv_columns" : {
			"id_device":0,
			"gps_date":1,
			"temperature":15,
			"sat_number":5,
			"hdop":9,
			"latitude":10,
			"longitude":11,
			"altitude":12
		},
		"csv_header":"TRUE"
	},
	"eobs":{
		"csv_folder":"/home/ftpgps/data_eobs",
		"csv_columns" : {
			"id_device":0,
			"gps_date":1,
			"temperature":15,
			"sat_number":5,
			"hdop":9,
			"latitude":10,
			"longitude":11,
			"altitude":12
		},
		"csv_header":"FALSE"
	},
	"technosmart":{
		"csv_folder":"/home/ftpgps/data_technosmart",
		"csv_columns" : {
			"id_device":0,
			"gps_date":1,
			"temperature":15,
			"sat_number":5,
			"hdop":9,
			"latitude":10,
			"longitude":11,
			"altitude":12
		},
		"csv_header":"TRUE"
	}

}

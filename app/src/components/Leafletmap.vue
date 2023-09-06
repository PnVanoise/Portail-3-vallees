<script setup>
import Sidebar from "./Sidebar.vue";
import "leaflet/dist/leaflet.css";
import "leaflet/dist/leaflet.js";
import "leaflet-polylinedecorator/dist/leaflet.polylineDecorator.js";
import "leaflet.markercluster/dist/leaflet.markercluster.js";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import { ref, onMounted } from 'vue';

// Variables réactives
let map = ref(null);
let geojsonLayers = ref({});
let data = ref({});
let individuLayers = ref({});
let fetchedIndividus = [];

let fetchedIndividusData = [];

let individusToFetch = [];


const getIndividus = async (individus) => {
  console.log("Received new individus:", individus);

  // console.log("app:", individusRef.value);

  console.log("individus length :", individus);
  console.log("fetchedIndividus length :", fetchedIndividus);

  if (individus.length < fetchedIndividus.length) {
    const individusToRemove = fetchedIndividus.filter((individuName) =>
      !individus.some((individu) => individu.name === individuName)
    );

    await Promise.all(individusToRemove.map(async (individuName) => {
      console.log("Individu to remove :", individuName);
      await removeIndividus(individuName);
    }));

  }

  individusToFetch = individus.filter((individu) => 
    !fetchedIndividus.includes(individu.name)
  );

  fetchedIndividus = fetchedIndividus.concat(individusToFetch.map((individu) => individu.name));
  fetchedIndividusData = fetchedIndividusData.concat(individusToFetch.map((individu) => individu));

  if (individusToFetch.length > 0) {
    const lastIndividutoFetch = individusToFetch[individusToFetch.length - 1];

    console.log("Individus to fetch :", lastIndividutoFetch);
    fetchData([lastIndividutoFetch], timeRef.value);
  }

};

const removeIndividus = async (individuName) => {

  if (individuLayers.value[individuName + '_point']) {
    console.log("Removing point layer:", individuName + '_point');
    geojsonLayers.value.removeLayer(individuLayers.value[individuName + '_point']);
    delete individuLayers.value[individuName + '_point'];
  }

  if (individuLayers.value[individuName + '_ligne']) {
    console.log("Removing ligne layer:", individuName + '_ligne');
    geojsonLayers.value.removeLayer(individuLayers.value[individuName + '_ligne']);
    delete individuLayers.value[individuName + '_ligne'];
  }

  if (individuLayers.value[individuName + '_fleche']) {
    console.log("Removing fleche layer:", individuName + '_fleche');
    geojsonLayers.value.removeLayer(individuLayers.value[individuName + '_fleche']);
    delete individuLayers.value[individuName + '_fleche'];
  }
  if (timeSelected.length == 1) {
    const index = fetchedIndividus.indexOf(individuName);
    if (index !== -1) {
      fetchedIndividus.splice(index, 1);
    }
    const indexBis = fetchedIndividusData.indexOf(individuName);
    if (indexBis !== -1) {
      fetchedIndividusData.splice(indexBis, 1);
    }
  }
};

let timeRef = ref(15);
let timeSelected = [15];
console.log("Période par défaut :", timeRef.value);

const getTime = (timeSelect) => {
  timeRef.value = timeSelect;
  console.log("Période sélectionnée :", timeRef.value);

  timeSelected.push(timeRef.value);
  // console.log("Liste des périodes sélectionnées :", timeSelected);

  if (timeSelected.length > 1) {
    if (fetchedIndividus.length > 0) {
      console.log("FetchedIndividus :", fetchedIndividusData)
  
      for (let i of fetchedIndividusData) {
        console.log("Remove individu :", i);
        removeIndividus(i.name);
        console.log("Fetch individu :", i);
        fetchData([i], timeRef.value);
      }
      timeSelected = [15];
      // console.log("Liste des périodes sélectionnées :", timeSelected);
    }
  }
};


const fetchData = async (individus, time) => {
  try {

    if (individus.length > 0) {
      console.log("Fetching data for:", individus);

      //const time = `${timeRef.value}`;
  

      individus.map(async (individu) => {
        console.log("Processing data for:", individu.name);

        const name = individu.name;
        const color = individu.attributs.fill;

        //Données
        const response = await fetch(window.config.api_url + '/v_animals_loc?name=' + name + '&last_day=' + time);
        data.value = await response.json();
        console.log(data.value.features.length);
        if (data.value.features.length > 0) {

          // Initialisation du style des points
          const stylePoint = { "color": "#000", "fillColor": "#FFF", "Opacity": 1, "fillOpacity": 1, "weight": 3 };

          // On traduit les données en points avec popup
          const geojsonLayerPoint = L.geoJSON(data.value, {
            style: stylePoint,
            pointToLayer: function (feature, latlng) {
              return L.circleMarker(latlng, { radius: 5 });
            },
            onEachFeature: function (feature, layer) {
              if (feature.properties) {
                let popupString = '';
                let attributs = {
                  'name': 'Surnom',
                  'nom_vern': 'Espèce',
                  'attributs': 'Attributs',
                  'birth_year': 'Année de naissance',
                  'gps_date': 'Date de la localisation',
                  'altitude': 'Altitude (en m)'
                };
                let attributsOrder = ['name', 'nom_vern', 'attributs', 'birth_year', 'gps_date', 'altitude'];
                for (let i = 0; i < attributsOrder.length; i++) {
                  const key = attributsOrder[i];
                  if (key in feature.properties) {
                    if (key === 'attributs') {
                      const attributsObj = feature.properties[key];
                      for (const attrKey in attributsObj) {
                        if (attributsObj.hasOwnProperty(attrKey)) {
                          if (attrKey === 'sex_libelle') {
                            popupString += '<strong>Sexe</strong> : ' + attributsObj[attrKey] + '<br />';
                          } else if (attrKey === 'age_libelle') {
                            popupString += '<strong>Age</strong> : ' + attributsObj[attrKey] + '<br />';
                          }
                        }
                      }
                    } else {
                      popupString += '<strong>' + attributs[key] + '</strong> : ' + feature.properties[key] + '<br />';
                    }
                  }
                }
                layer.bindPopup(popupString);
              }
            }
          });
          individuLayers.value[name + '_point'] = geojsonLayerPoint;
          geojsonLayers.value.addLayer(geojsonLayerPoint);


          let lineCoordinate = [];

          for (let i in data.value.features) {
            let pointJson = data.value.features[i];
            let coord = pointJson.geometry.coordinates;
            lineCoordinate.push([coord[1], coord[0]]);
          }

          if (lineCoordinate.length > 1) {
            const geojsonLayerLine = L.polyline(lineCoordinate, {
              color: color,
              opacity: 1, 
              fillOpacity: 1,
              weight: 3
            }).addTo(map.value);

            let fleche = L.polylineDecorator(geojsonLayerLine, {
              patterns: [{
                offset: 0,
                repeat: '50px',
                symbol: new L.Symbol.arrowHead({
                  pixelSize: 10,
                  polygon: false,
                  pathOptions: { "interactive": false, "color": "#7F2B7F", "Opacity": 1, "weight": 3 }
                })
              }]
            }).addTo(map.value);
            individuLayers.value[name + '_fleche'] = fleche;
            geojsonLayers.value.addLayer(fleche);
            individuLayers.value[name + '_ligne'] = geojsonLayerLine;
            geojsonLayers.value.addLayer(geojsonLayerLine);

          }
          map.value.fitBounds(geojsonLayerPoint.getBounds());


        } else {
          alert("Aucunes données disponibles pour " + name + " sur les " + time + " derniers jours.");
        }
      }); 
    } 
  } catch (error) {
    console.log("error fetching data:", error);
  }
};


onMounted(async () => {
  try {

    // Fonds de plan
    const osm = L.tileLayer(window.config.leaflet_fonds_carte.OSM.url, {
      maxZoom: window.config.leaflet_fonds_carte.OSM.maxZoom,
      attribution: window.config.leaflet_fonds_carte.OSM.attribution
    });
    const igncarte = L.tileLayer(window.config.leaflet_fonds_carte.IGNCARTE.url, {
      maxZoom: window.config.leaflet_fonds_carte.IGNCARTE.maxZoom,
      attribution: window.config.leaflet_fonds_carte.IGNCARTE.attribution
    });
    const ignphoto = L.tileLayer(window.config.leaflet_fonds_carte.IGNPHOTO.url, {
      maxZoom: window.config.leaflet_fonds_carte.IGNPHOTO.maxZoom,
      attribution: window.config.leaflet_fonds_carte.IGNPHOTO.attribution
    });

    const baseMaps = {
      "OpenStreetMap": osm,
      "Carte IGN": igncarte,
      "Photo aérienne IGN": ignphoto
    };

    // Carte
    map.value = L.map("map", {
      center: window.config.leaflet_centrage_initial,
      zoom: window.config.leaflet_zoom_initial,
      zoomControl: false,
      layers: osm
    });

    const layerControl = L.control.layers(baseMaps).addTo(map.value);
    L.control.zoom({ position: 'topright' }).addTo(map.value);
    L.control.scale({ imperial: false, position: 'bottomright' }).addTo(map.value);



    geojsonLayers.value = L.layerGroup().addTo(map.value);

    


  } catch (error) {
    console.log("error during initial data fetch:", error);
  }
});



</script>

<template>


  <div class="d-flex flex-col">
    <div id="map" class="map-container"></div>
    <div class="d-flex flex-row">
      <Sidebar @send-individu="getIndividus" @sendTime="getTime" />
    </div>  
    
    
  </div>
 
    
</template>

<style>

/* .accueil-container {
  display: flex;
  flex-direction: column;
  position: relative;
} */

/* .map-container {
  width: 100%;
  height: 100vh; 
  /* position: absolute; */
  /*z-index: 1;
} */

#map {
  width: -webkit-fill-available;
  height: -webkit-fill-available;
  /* width: 100%;
  height: 88vh; */
  /* margin: 0; */
  position: fixed;
  z-index: 1;
}
</style>


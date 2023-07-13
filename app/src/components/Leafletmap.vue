<script setup>

import "leaflet/dist/leaflet.css";
import { ref, onMounted, watch, watchEffect } from 'vue';
import "leaflet/dist/leaflet.js";
import "leaflet-polylinedecorator/dist/leaflet.polylineDecorator.js";

// Variables réactives
let map = ref(null);
let geojsonLayerLineGroup = ref(null);
let geojsonLayerPoint = ref(null);
let data = ref({});

const props = defineProps({
  name:Object,
  time:Number
});

let name = ref(props.name);
console.log(name);

watchEffect(async () =>  {

  console.log(props.name);

  // Ne rien afficher si aucun individu n'est sélectionné
  if (props.name === null) {
    return 
  };
  data.value = {};

  // Données
  const response = await fetch('http://5.196.111.112:5000/api/animals_loc?name=' + props.name);
  data.value = await response.json();
  console.log(data.value);

  geojsonLayerLineGroup.value = L.layerGroup();
  geojsonLayerLineGroup.value.addTo(map.value);

  // Initialisation du style des tracés
  const styleTrace = {"color":"#000","fillColor":"#FFF","Opacity":1,"fillOpacity":1,"weight":3};

  // On traduit les données en points avec popup
    geojsonLayerPoint.value = L.geoJSON(data.value, {
    style: styleTrace,
    pointToLayer: function(feature, latlng) {
      return L.circleMarker(latlng, {radius: 5});
    },
    onEachFeature: function(feature, layer) {
      if (feature.properties) {
        let popupString = '';
        let attributs = {
          'name': 'Surnom',
          'nom_vern': 'Espèce',          
          'attributs' : 'Attributs',
          'birth_year': 'Année de naissance',
          'gps_date': 'Date de la localisation',
          'altitude': 'Altitude (en m)'          
        };
        let attributsOrder = ['name', 'nom_vern', 'attributs', 'birth_year', 'gps_date', 'altitude'];
        // attributsOrder.forEach(key => {
        //   if (key in feature.properties) {
        //     if (key === 'attributs') {
        //       feature.properties[key].forEach(attributs => {
        //         let [attributKey, attributValue] = attributs.split(':');
        //         if (attributKey === 'sex_libelle') {
        //         popupString += '<strong>Sexe</strong> : ' + attributValue + '<br />';
        //       } else if (attributKey === 'age_libelle') {
        //         popupString += '<strong>Age</strong> : ' + attributValue + '<br />';
        //       }
        //     });
        //     } else {
        //       popupString += '<strong>' + attributs[key] + '</strong> : ' + feature.properties[key] + '<br />';
        //     }
        //   }
        // });
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
  map.value.addLayer(geojsonLayerPoint.value);


  let lineCoordinate = [];

  for (let i in data.value.features){
    let pointJson = data.value.features[i];
    let coord = pointJson.geometry.coordinates;
    lineCoordinate.push([coord[1], coord[0]]);
  }
  console.log(lineCoordinate);

  if (lineCoordinate.length > 1) {
    const geojsonLayerLine = L.polyline(lineCoordinate, {
    style: styleTrace
    }).addTo(map.value);

    // Initialisation du groupe de layers
    // geojsonLayerLineGroup.value.clearLayers();

    let fleche = L.polylineDecorator(geojsonLayerLine, {
            patterns: [{
              offset: 0, 
              repeat: '50px',
              symbol: new L.Symbol.arrowHead({
                pixelSize: 10, 
                polygon: false,
                pathOptions: {"color":"#7F2B7F","Opacity":1,"weight":3}
              })
            }]
          }).addTo(map.value);
          geojsonLayerLineGroup.value.addLayer(fleche);
  

    geojsonLayerLineGroup.value.addLayer(geojsonLayerLine);

  }
});

onMounted(async () => {

  // Carte
  map.value = L.map("map", {
    center: [45.3874, 6.7949],
    zoom: 10,
    zoomControl: false
  }); 
  L.control.zoom({position: 'topright'}).addTo(map.value);
  L.control.scale({imperial: false, position: 'bottomright'}).addTo(map.value);

  // Fond de plan
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map.value);


});




</script>

<template>
  
  <div id="map" class="d-flex"></div>

</template>

<style>

  #map {
    /* height: 100%; */
    width: 100%;
    margin: 0;
    position: absolute;
  }

</style>

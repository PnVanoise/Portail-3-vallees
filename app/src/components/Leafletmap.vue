<script setup>

import "leaflet/dist/leaflet.css";
import { ref, onMounted, watch, watchEffect, computed, watchPostEffect, reactive } from 'vue';
import "leaflet/dist/leaflet.js";
import "leaflet-polylinedecorator/dist/leaflet.polylineDecorator.js";

// Variables réactives
let map = ref(null);
let geojsonLayers = ref({});
let data = ref({});

// let toto = null;

// let selectedBirdNames = ref([]);


const props = defineProps({
  individus: Array,
  time: Number
});


const fetchData = async (individus) => {
  try {
    //console.log(geojsonLayers.value);
    console.log("FETCH");
    if (individus.length > 0) {
  

      individus.map(async (individu) => {
        const name = individu.name;
        const color = individu.attributs.fill;

        //Données
        const response = await fetch(window.config.api_url + '/v_animals_loc?name=' + name);
        data.value = await response.json();
        console.log(data.value);


        // geojsonLayerLineGroup.value.clearLayers();

        // if (geojsonLayers.value[name]) {
        //   map.value.removeLayer(geojsonLayers.value[name]);
        // }

        
        //toto = L.layerGroup().addTo(map.value);


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

        geojsonLayers.value.addLayer(geojsonLayerPoint);
        //toto.addLayer(geojsonLayerPoint);
        //geojsonLayers.value.push(geojsonLayerPoint);
        //geojsonLayerLineGroup.value.addLayer(geojsonLayerPoint);

        // if (!selectBirdNames.value.includes(name)) {
        //   selectBirdNames.value.push(name);
        // }


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

          // Initialisation du groupe de layers
          // geojsonLayerLineGroup.value.clearLayers();

          let fleche = L.polylineDecorator(geojsonLayerLine, {
            patterns: [{
              offset: 0,
              repeat: '50px',
              symbol: new L.Symbol.arrowHead({
                pixelSize: 10,
                polygon: false,
                pathOptions: { "color": "#7F2B7F", "Opacity": 1, "weight": 3 }
              })
            }]
          }).addTo(map.value);
          geojsonLayers.value.addLayer(fleche);
          //toto.addLayer(fleche);
          //geojsonLayerLineGroup.value.addLayer(fleche);

          geojsonLayers.value.addLayer(geojsonLayerLine);

          // var toto = geojsonLayers.value.getLayers();
          // console.log("toto layers:", toto);

          //toto.addLayer(geojsonLayerLine);
          //geojsonLayerLineGroup.value.addLayer(geojsonLayerLine);

          // for (const geojsonLayer of geojsonLayers.value) {
          //   geojsonLayerLineGroup.value.addLayer(geojsonLayer);
          // }
        }
      });
    }
  } catch (error) {
    console.log("error fetching data:", error);
  }
};

// FLOURS
const loadDatadeux = async (individus) => {
  console.log("fonction loadatadeux:", individus);
  fetchData(individus);
};

// A REMETTRE
// const loadData = async (name) => {
//   if (geojsonLayers.value[name]) {
//     map.value.removeLayer(geojsonLayers.value[name]);
//     delete geojsonLayers.value[name];
//   }
//   await fetchData(name);
// };

// const NameChange = async (newName, oldName) => {
//   if (oldName) {
//     if (geojsonLayers.value[oldName]) {
//       map.value.removeLayer(geojsonLayers.value[oldName]);
//       delete geojsonLayers.value[oldName];
//     }
//   }
//   if (newName) {
//     selectedBirdNames.value.push(newName);
//     await loadData(newName);
//   }
// }

onMounted(async () => {
  try {

    // Carte
    map.value = L.map("map", {
      center: window.config.leaflet_centrage_initial,
      zoom: window.config.leaflet_zoom_initial,
      zoomControl: false
    });
    L.control.zoom({ position: 'topright' }).addTo(map.value);
    L.control.scale({ imperial: false, position: 'bottomright' }).addTo(map.value);

    // Fond de plan
    L.tileLayer(window.config.leaflet_fonds_carte.OSM.url, {
      maxZoom: window.config.leaflet_fonds_carte.OSM.maxZoom,
      attribution: window.config.leaflet_fonds_carte.OSM.attribution
    }).addTo(map.value);

    geojsonLayers.value = L.layerGroup().addTo(map.value);

    // geojsonLayerLineGroup.value = L.layerGroup();
    // geojsonLayerLineGroup.value.addTo(map.value);
    //geojsonLayers = {};

    // if (props.name !== null) {
    //   selectedName.value = props.name;
    //   loadData(props.name);
    //   // currentName.value = props.name;
    //   // geojsonLayers.value[props.name] = L.layerGroup().addTo(map.value);
    // }
    // for (const name of selectedBirdNames.value) {
    //   await loadData(name);
    // }


  } catch (error) {
    console.log("error during initial data fetch:", error);
  }
});

// A REMETTRE //
// watch(() => props.individus, (newIndividus) => {
//   // loadDatadeux(newIndividus, oldIndividus);
//   console.log(newIndividus);
// });

//  FLOURS
// watch(() => props.individus, (newItems, oldItems) => {
//   for (const individu of newItems) {
//     console.log(individu);
//     if (geojsonLayers.value[individu.name]) {
//       map.value.removeLayer(geojsonLayers.value[individu.name]); //clearLayer() ??
//       delete geojsonLayers.value[individu.name];
//     }
//   };
//   if (newItems !== oldItems) { // trouver d'autres conditions sans doute là
//     loadDatadeux(newItems);
//   };
//   },
//   { deep: true }
// );

// ALIX TEST 22/08
// watch(() => props.individus, (newItems, oldItems) => {
//   console.log("newitems=", newItems);
//   for (const item of newItems) {
//     console.log("item=", item);

//     // let geojson = null;

//     // geojsonLayers.value.eachLayer(layer => {
//     //   console.log("layer =", layer);
//     //   if (layer.options.onEachFeature) {
//     //     layer.eachLayer(innerlayer => {
//     //       geojson = innerlayer;
//     //       return false;
//     //     });
//     //     return false;
//     //   }
//     // });

//     //console.log("geojson =", geojson.feature.properties);
    
//     if (data.value.name == item.name) {
//       console.log(item.name, "a déjà été cartographié");
//       geojsonLayers.value.clearLayers();
//     } else {
//       fetchData(item);
//       console.log("geojsonLayers =", geojsonLayers.value);
//     }
//   };
// }, { deep: true }
// );

watch(() => props.individus, (newItems, oldItems) => {
  console.log("DANS WATCH");
  console.log("NEW:", newItems);
  //console.log("OLD:", oldItems);
  //console.log("item:", Items);

  //if (newItems.length != oldItems.length) {
  if (newItems.length != 0) {
    console.log("WATCH 1");

  //   console.log("new 1:", newItems, "old 1:", oldItems);
    loadDatadeux(newItems);
	  //geojsonLayers.value.clearLayers();

   } else {
    // for (const individu of oldItems) {
    //   if (newItems === individu) {
    //     console.log("coucou");
    //   }
    // }
    //console.log("WATCH 2");
  //   console.log("new 2:", newItems, "old 2:", oldItems);
    //geojsonLayers.value.clearLayers();
   }

  // if (newItems.length === 0) {
  //   for (const individu of oldItems) {
  //     // map.value.removeLayer(geojsonLayers.value[individu.name]);
  //     // delete geojsonLayers.value[individu.name];
      
  //     console.log(individu.name);
  //     // for (const layer in geojsonLayers.value.getLayers()) {
  //     //   console.log("layer:", layer);
  //     // //   if (layer === individu.name) {
  //     // //     console.log("GROS TRUC");
  //     // //     map.value.removeLayer(layer); //clearLayer() ??
  //     // //     delete layer;
  //     // // }
  //     // }

  //   }
  // } else {
  //   if (oldItems.length === 0) {
  //     loadDatadeux(newItems);
  //   } else {
  //     for (const individu of oldItems) {
  //       if (geojsonLayers.value[individu.name]) {
  //       map.value.removeLayer(geojsonLayers.value[individu.name]); //clearLayer() ??
  //       delete geojsonLayers.value[individu.name];
  //       }
  //     }
  //     loadDatadeux(newItems);
      
  //   }
  // }
},// { immediate: true }
);



// A REMETTRE
// watch(selectedBirdNames, async (newNames, oldNames) => {
//   const removedNames = oldNames.filter((name) => !newNames.includes(name));
//   for (const name of removedNames) {
//     if (geojsonLayers.value[name]) {
//       map.value.removeLayer(geojsonLayers.value[name]);
//       delete geojsonLayers.value[name];
//     }
//   }
//   for (const name of newNames) {
//     if (!geojsonLayers.value[name]) {
//       await loadData(name);
//     }
//   }
// });


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


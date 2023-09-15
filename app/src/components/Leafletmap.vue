<script setup>
import Sidebar from "./Sidebar.vue";
import "leaflet/dist/leaflet.css";
import "leaflet/dist/leaflet.js";
import "leaflet-polylinedecorator/dist/leaflet.polylineDecorator.js";
import "leaflet.markercluster/dist/leaflet.markercluster.js";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import { ref, onMounted } from 'vue';

// Variables
let map;
let loading = ref(false);
let geojsonLayers = ref({});
// let data = ref({});
let individuLayers = ref({});
let fetchedIndividus = [];
let fetchedIndividusData = [];
let individusToFetch = [];

// Récupération des individus selectionnés ou déselectionnés
const getIndividus = async (individus) => {
  console.log("Received new individus:", individus);
  console.log("fetchedIndividus length :", fetchedIndividus);

  // Si la liste des individus reçue est < à la liste des individus chargés sur la carte alors on supprime l'individu manquant 
  if (individus.length < fetchedIndividus.length) {
    const individusToRemove = fetchedIndividus.filter((individuName) =>
      !individus.some((individu) => individu.name === individuName)
    );

    const individusDataToRemove = fetchedIndividusData.filter((individu) =>
      !individus.some((ind) => ind === individu)
    );

    await Promise.all(individusToRemove.map(async (individuName) => {
      console.log("Individu to remove :", individuName);
      await removeIndividus(individuName);
      const index = fetchedIndividus.indexOf(individuName);
      if (index !== -1) {
        fetchedIndividus.splice(index, 1);
      }
    }));

    await Promise.all(individusDataToRemove.map(async (individuData) => {
      console.log("Individu Data to remove :", individuData);
      await removeIndividus(individuData);
      const indexBis = fetchedIndividusData.indexOf(individuData);
      if (indexBis !== -1) {
        fetchedIndividusData.splice(indexBis, 1);
      }
    }))

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

// Fonction qui retire les données de la carte 
const removeIndividus = async (individuName) => {

  if (individuLayers.value[individuName + '_point']) {
    console.log("Removing point layer:", individuName + '_point');
    geojsonLayers.value.removeLayer(individuLayers.value[individuName + '_point']);
    delete individuLayers.value[individuName + '_point'];
  }

  if (individuLayers.value[individuName + '_lastpoint']) {
    console.log("Removing point layer:", individuName + '_lastpoint');
    geojsonLayers.value.removeLayer(individuLayers.value[individuName + '_lastpoint']);
    delete individuLayers.value[individuName + '_lastpoint'];
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

  // // if (timeSelected.length == 1) {
  //   const index = fetchedIndividus.indexOf(individuName);
  //   if (index !== -1) {
  //     fetchedIndividus.splice(index, 1);
  //   }
  //   const indexBis = fetchedIndividusData.indexOf(individuName);
  //   if (indexBis !== -1) {
  //     fetchedIndividusData.splice(indexBis, 1);
  //   }
  // // }
};

let timeRef = ref(15);
let timeSelected = [15];
console.log("Période par défaut :", timeRef.value);

// Récupération de la période sélectionnée 
const getTime = (timeSelect) => {
  timeRef.value = timeSelect;
  console.log("Période sélectionnée :", timeRef.value);

  timeSelected.push(timeRef.value);
  console.log("Liste des périodes sélectionnées :", timeSelected);
  console.log("Liste des individués sélectionnés :", fetchedIndividus);

  // Si la liste des périodes sélectionnées est > à 1 et qu'il y a déjà des données chargées sur la carte alors on les retire et on les re-affiche à jour
  if (timeSelected.length > 1 && fetchedIndividus.length > 0) {
    // if (fetchedIndividus.length > 0) {
      console.log("FetchedIndividus :", fetchedIndividusData)

      for (let i of fetchedIndividusData) {
        console.log("Remove individu :", i);
        removeIndividus(i.name);
        console.log("Fetch individu :", i);
        fetchData([i], timeRef.value);
      }
      timeSelected = [15];
      // console.log("Liste des périodes sélectionnées :", timeSelected);
    // }
  }
};

// Fonction qui charge les données
const fetchData = async (individus, time) => {
  try {

    if (individus.length > 0) {

      loading.value = true;

      console.log("Fetching data for:", individus);
      const fetchRequests = individus.map(async (individu) => {
        console.log("Processing data for:", individu.name);

        const name = individu.name;
        const nameBis = individu.name.replace(/\s+/g, "_");
        const color = individu.attributs.fill;

        let apiUrl = window.config.api_url + '/v_animals_loc?name=' + name;

        if (time !== "All") {
          apiUrl += '&last_day=' + time;
        }

        const response = await fetch(apiUrl);
        const data = await response.json();

        return { name, data, nameBis, color };
      });

      const results = await Promise.all(fetchRequests);

      results.forEach(({ name, data, nameBis, color }) => {
        if (data.features.length > 0) {
          // Initialisation du style des points et des popup
          const stylePoint = { "color": "#000", "fillColor": "#FFF", "Opacity": 1, "fillOpacity": 1, "weight": 3 };
          const lastPointIcon = L.divIcon({
            html: `<svg viewBox='0 0 500 820' version='1.1' xmlns='http://www.w3.org/2000/svg' xml:space='preserve' style='fill-rule: evenodd; clip-rule: evenodd; stroke-linecap: round;'>
            <defs>
              <linearGradient id='map-marker-${nameBis}-f' x1='0%' y1='0%' x2='100%' y2='0%'>
                <stop offset='0%' style='stop-color:${color};stop-opacity:1' />
                <stop offset='100%' style='stop-color:${color};stop-opacity:1' />
              </linearGradient>
              <!-- Define a linear gradient with a unique ID for the stroke -->
              <linearGradient id='map-marker-${nameBis}-s' x1='0%' y1='0%' x2='100%' y2='0%'>
                <stop offset='0%' style='stop-color:rgb(0,0,0);stop-opacity:1' />
                <stop offset='100%' style='stop-color:rgb(0,0,0);stop-opacity:1' />
              </linearGradient>
            </defs>
            <g transform="matrix(19.5417,0,0,19.5417,-7889.1,-9807.44)">
              <path xmlns='http://www.w3.org/2000/svg' fill='#FFFFFF' d='M421.2,515.5c0,2.6-2.1,4.7-4.7,4.7c-2.6,0-4.7-2.1-4.7-4.7c0-2.6,2.1-4.7,4.7-4.7 C419.1,510.8,421.2,512.9,421.2,515.5z'/>
              <path d="M416.544,503.612C409.971,503.612 404.5,509.303 404.5,515.478C404.5,518.256 406.064,521.786 407.194,524.224L416.5,542.096L425.762,524.224C426.892,521.786 428.5,518.433 428.5,515.478C428.5,509.303 423.117,503.612 416.544,503.612ZM416.544,510.767C419.128,510.784 421.223,512.889 421.223,515.477C421.223,518.065 419.128,520.14 416.544,520.156C413.96,520.139 411.865,518.066 411.865,515.477C411.865,512.889 413.96,510.784 416.544,510.767Z" stroke-width="1.1px" fill="url(#map-marker-${nameBis}-f)" stroke="url(#map-marker-${nameBis}-s)"/></g>
          </svg>`,
            className: "",
            iconSize: [30, 30],
            iconAnchor: [16, 42],
          });
          const popUp = (feature, layer) => {
            if (feature.properties) {
              let popupString = '';
              let attributs = {
                'name': 'Nom',
                'nom_vern': 'Espèce',
                'attributs': 'Attributs',
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
                          popupString += '<strong>Maturité</strong> : ' + attributsObj[attrKey] + '<br />';
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
          };

          // const geojsonMarkerOptions = {
          //   radius: 5,
          //   fillColor: "#FFF",
          //   color: "#000",
          //   opacity: 1,
          //   fillOpacity: 1,
          //   weight: 3
          // };

          // const markers = L.markerClusterGroup();

          // L.geoJSON(data.value, {
          //   pointToLayer: function (feature, latlng) {
          //     return markers.addLayer(L.circleMarker(latlng, geojsonMarkerOptions));
          //   },
          //   onEachFeature: function (feature, layer) {
          //     if (feature.properties) {
          //       let popupString = '';
          //       let attributs = {
          //         'name': 'Surnom',
          //         'nom_vern': 'Espèce',
          //         'attributs': 'Attributs',
          //         'birth_year': 'Année de naissance',
          //         'gps_date': 'Date de la localisation',
          //         'altitude': 'Altitude (en m)'
          //       };
          //       let attributsOrder = ['name', 'nom_vern', 'attributs', 'birth_year', 'gps_date', 'altitude'];
          //       for (let i = 0; i < attributsOrder.length; i++) {
          //         const key = attributsOrder[i];
          //         if (key in feature.properties) {
          //           if (key === 'attributs') {
          //             const attributsObj = feature.properties[key];
          //             for (const attrKey in attributsObj) {
          //               if (attributsObj.hasOwnProperty(attrKey)) {
          //                 if (attrKey === 'sex_libelle') {
          //                   popupString += '<strong>Sexe</strong> : ' + attributsObj[attrKey] + '<br />';
          //                 } else if (attrKey === 'age_libelle') {
          //                   popupString += '<strong>Age</strong> : ' + attributsObj[attrKey] + '<br />';
          //                 }
          //               }
          //             }
          //           } else {
          //             popupString += '<strong>' + attributs[key] + '</strong> : ' + feature.properties[key] + '<br />';
          //           }
          //         }
          //       }
          //       layer.bindPopup(popupString);
          //     }
          //   }

          // });
          // individuLayers.value[name + '_point'] = markers;
          // geojsonLayers.value.addLayer(markers);

          // Affichage du dernier point
          const lastPoint = data.features.slice(-1)[0];

          const geojsonLastPoint = L.geoJSON(lastPoint, {
            pointToLayer: function (feature, latlng) {
              return L.marker(latlng, {
                icon: lastPointIcon
              })
            },
            onEachFeature: popUp
          }).addTo(map);
          individuLayers.value[name + '_lastpoint'] = geojsonLastPoint;
          geojsonLayers.value.addLayer(geojsonLastPoint);


          //On traduit les données en points avec popup
          const geojsonLayerPoint = L.geoJSON(data, {
            style: stylePoint,
            pointToLayer: function (feature, latlng) {
              return L.circleMarker(latlng, { radius: 5 });
            },
            onEachFeature: popUp
          }).addTo(map);
          individuLayers.value[name + '_point'] = geojsonLayerPoint;
          geojsonLayers.value.addLayer(geojsonLayerPoint);


          let lineCoordinate = [];

          for (let i in data.features) {
            let pointJson = data.features[i];
            let coord = pointJson.geometry.coordinates;
            lineCoordinate.push([coord[1], coord[0]]);
          }

          if (lineCoordinate.length > 1) {
            const geojsonLayerLine = L.polyline(lineCoordinate, {
              color: color,
              opacity: 1,
              fillOpacity: 1,
              weight: 3
            }).addTo(map);

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
            }).addTo(map);
            individuLayers.value[name + '_fleche'] = fleche;
            geojsonLayers.value.addLayer(fleche);
            individuLayers.value[name + '_ligne'] = geojsonLayerLine;
            geojsonLayers.value.addLayer(geojsonLayerLine);

          }
          if (geojsonLayerPoint !== null) {
            map.fitBounds(geojsonLayerPoint.getBounds());
          }

        } else {
          alert("Aucunes données disponibles pour " + name + " sur les " + time + " derniers jours.");
        }
      });

      loading.value = false;
    }
  } catch (error) {
    console.log("Error fetching data:", error);
  }
};

// Au chargement de la page, la carte, les fonds de plan et la légende sont générés en premier
onMounted(() => {
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
    map = L.map("map", {
      center: window.config.leaflet_centrage_initial,
      zoom: window.config.leaflet_zoom_initial,
      zoomControl: false,
      zoomAnimation: false,
      layers: [osm]
    });

    L.control.layers(baseMaps).addTo(map);
    L.control.zoom({ position: 'topright' }).addTo(map);
    L.control.scale({ imperial: false, position: 'bottomright' }).addTo(map);

    const legend = L.control({ position: 'bottomright' });
    legend.onAdd = function (map) {
      let div = L.DomUtil.create('div', 'legend');
      div.innerHTML += '<div class="d-flex"><div class="col"><div class"row"><div class="col"><h5>Légende</h5></div></div>'
      div.innerHTML += '<div class="row"><div class="col item"><i class="point"></i></div><div class="col text"><p>Point GPS</p></div></div>'
      div.innerHTML += '<div class="row"><div class="col item"><svg class="track" width="117" height="42" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" overflow="hidden"><defs><clipPath id="clip0"><rect x="941" y="541" width="117" height="42"/></clipPath><clipPath id="clip1"><rect x="-6096.32" y="-0.143369" width="719390" height="256054"/></clipPath><image width="117" height="42" xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHUAAAAqCAMAAAC6AuSsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADhUExURQAAAECAv4BAn3Awn0B1v3U1n0hwx3Awn0ZzxnMzn3Awn3Iyn0R0w3Awn0Nxw3Eyn0NzwnAwn3Exn3Awn0VxxHExn0RyxHAwn0RxxHExn3Awn0RzxHExoURyxHAwoHExoEVyxXAwoHExoERyxXAwoERyxHExoERzxHAwoERyxHExoERzxHAwoHExoEVyxXAwoHExoERyxHAwoERyxHExoERyxEduwklqv0lswUtovkxmvU5kvFFgulRZtldVtFlTs1xQsV1NsGBJrmFHrWJFq2c/qGg8p2w3o200om8zoXAwoLg6QmAAAAA1dFJOUwAICBAYGCAgKCgwOEBASEhQUFhgaGhwcHh4gIeHj4+Xn5+nr6+3t7+/x8fPz9ff3+fv7/f3ZRkUsAAAAAlwSFlzAAAXEQAAFxEByibzPwAAAaVJREFUWEfN19lSwjAAheFYQCyLLBURRLQCiihQWRVFEesC7/9ApuVEaJzJ0IzJ8F2F5OKfZtqSkl0WO3d6l0n80MVoLz3NHH7rUfKjVNfCjA5XiFIauxtVr2tgWrEiguCUI1hQq44e09PTLTroMXq6xs50B9UY1pSyuugxurp36DGaurkWeoymbrqJHqOpm+CfX01d00aPCduNnl0PJYzn6DGL2QhLAp3GkR/N3mMitLGLHvP9ghWhmygh+9JRasJ3Z1gQahBygaGkCbfPz5gXSpFbjKSN3xH0vWFW6Jh0MJL1MPtC0OdiWuiE1DCS8xS4UGqKBaEsSWEkY/qB1q/PLR6eYWePkFOMwxq9BrbW524T7ae8B/ZQ5oZ6nC9QWnMnWBTp1w7810R4hsX/79CTRTWOVTXiFf5MQU+rBbWnmUzgbLxSz2BRjUhh9cGzSfXWJu0BSmvtgtIPgVjp72Wq3to8f3iglN+1/IGUUry1FH8aXS41fLfnkGKcso6jmYXaSiuPacVM9KiBbWJSPfY6ail+7wVFvOfGqei7TDDTCYz+ASE/sOp91oP4jdcAAAAASUVORK5CYII=" preserveAspectRatio="none" id="img2"></image><clipPath id="clip3"><rect x="0" y="0" width="713293" height="256054"/></clipPath></defs><g clip-path="url(#clip0)" transform="translate(-941 -541)"><g clip-path="url(#clip1)" transform="matrix(0.000164028 0 0 0.000164028 941 541)"><g clip-path="url(#clip3)" transform="matrix(1 0 0 1 -0.222688 -0.178711)"><use width="100%" height="100%" xlink:href="#img2" transform="scale(2000 2000)"></use></g></g></g></svg></div><div class="col text"><p>Trace GPS</p></div></div>'
      div.innerHTML += '<div class="row"><div class="col item"><svg class="marker" viewBox="0 0 500 820" version="1.1" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" style="fill-rule: evenodd; clip-rule: evenodd; stroke-linecap: round;"><defs><linearGradient x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(2.30025e-15,-37.566,37.566,2.30025e-15,416.455,540.999)" id="map-marker-38-f"><stop offset="0" stop-color="rgb(18,111,198)"/><stop offset="1" stop-color="rgb(18,111,198)"/></linearGradient><linearGradient x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1.16666e-15,-19.053,19.053,1.16666e-15,414.482,522.486)" id="map-marker-38-s"><stop offset="0" stop-color="rgb(0,0,0)"/><stop offset="1" stop-color="rgb(0,0,0)"/></linearGradient></defs><g transform="matrix(19.5417,0,0,19.5417,-7889.1,-9807.44)"><path d="M416.544,503.612C409.971,503.612 404.5,509.303 404.5,515.478C404.5,518.256 406.064,521.786 407.194,524.224L416.5,542.096L425.762,524.224C426.892,521.786 428.5,518.433 428.5,515.478C428.5,509.303 423.117,503.612 416.544,503.612ZM416.544,510.767C419.128,510.784 421.223,512.889 421.223,515.477C421.223,518.065 419.128,520.14 416.544,520.156C413.96,520.139 411.865,518.066 411.865,515.477C411.865,512.889 413.96,510.784 416.544,510.767Z" stroke-width="1.1px" fill="url(#map-marker-38-f)" stroke="url(#map-marker-38-s)"/></g></svg></div><div class="col text"><p>Dernier point GPS</p></div></div></div></div>'

      return div;
    };
    legend.addTo(map);

    geojsonLayers.value = L.layerGroup().addTo(map);


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

  <div class="spinner-container" v-if="loading">
    <div class="d-flex justify-content-center">
      <div class="spinner-border" role="status"></div> 
    </div>
  </div>


</template>

<style>
#map {
  width: -webkit-fill-available;
  height: -webkit-fill-available;
  /* width: 100%;
  height: 88vh; */
  /* margin: 0; */
  position: fixed;
  z-index: 1;
}

.legend {
  width: min-content;
  line-height: 18px;
  border-radius: 5px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  background-color: rgba(255, 255, 255, 0.8);
  padding: 8px 8px;
}

.legend h5 {
  text-align: center;
  font-weight: bold;
  font-size: 16px;
  margin: 2px 12px 8px;
  color: #000;
}

.legend .item {
  margin: 2px;
  padding: 0;
  text-align: center;
  width: 20px;
}

.legend .text {
  padding: 0;
  width: 200px;
  align-self: center;

}

.legend p {
  text-align: start;
  font-size: 13px;
  color: #000;
  margin: 0;
  /* float: left; */
}

.legend .marker {
  width: 20px;
  /* margin-right: 8px;
  margin-left: 8px; */
  /* margin-top: 8px; */
  /* float: left; */
}

.legend .track {
  width: 40px;
  height: 15px;
  /* float: left; */
  /* margin-top: 8px; */
  /* margin-bottom: 8px; */
}

.legend i.point {
  background-color: #fff;
  border: 3px solid #000;
  border-radius: 50%;
  /* fill-opacity: 1;
  fill-rule: evenodd; */
  width: 18px;
  height: 18px;
  /* float:left; */
  margin-right: 8px;
  margin-left: 8px;
  display: inline-flex;

}

.spinner-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; 
}

.spinner-border {
  background-color: rgba(255, 255, 255, 0.8); 
  width: 50px; 
  height: 50px;
}


</style>


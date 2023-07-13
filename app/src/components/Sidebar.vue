<script setup>
import { ref, onMounted, computed } from 'vue';

// Définition des variables
let especes = ref(null); 
let individus = ref(null);

let selectEspece =ref([]); 
let isDataLoaded = ref(false); 
let showIndividus = ref(false); 

let selectIndividu = [];

const emit = defineEmits(["sendIndividu", "sendTime"]);



// const onIndividuSelected = (individu) => {
//     if (selectIndividu.value.includes(individu)) {
//         selectIndividu.value = selectIndividu.value.filter((item) => item !== individu);
//     } else {
//         selectIndividu.value.push(individu);
//     }
//     // Émettre les individus sélectionnés au composant Leafletmap.vue
//     emit('sendSelectedIndividus', selectIndividu.value);
// };



const clearOrfetchIndividu = (event) => {
    console.log("coucou");
    console.log(event);
    console.log(selectIndividu);
};

// Mise à jour du tableau selectEspece quand on sélectionne/désélectionne une espèce 
const onEspeceSelected = (espece) => {
    if (selectEspece.value.includes(espece)) {
        selectEspece.value = selectEspece.value.filter((item) => item !== espece);
        showIndividus.value = selectEspece.value.length > 0;
    } else {
        selectEspece.value.push(espece);
        showIndividus.value = true;
    }
};

// Vérification de la sélection 
const isEspeceSelected = (espece) => {
    return selectEspece.value.includes(espece);
};

// Données correspondantes aux espèces
onMounted(async () => {
    console.log(this)
    console.log(window.config);
    
    const response = await fetch(window.config.api_url + '/especes');
    const data = await response.json();

    especes.value = data;
    console.log(especes);

});

// Données correspondantes aux individus
onMounted(async () => {
    const response = await fetch('http://5.196.111.112:5000/api/animals_color');
    const data = await response.json();

    individus.value = data;
    console.log(individus);
    isDataLoaded.value = true;

});

// Filtre les individus en fonction de l'espèce sélectionnée ou désélectionnée. individu.active correspond aux animaux équipés encore actifs.
const filteredIndividus = computed(() => {
    if (isDataLoaded.value && selectEspece.value.length > 0) {
    return individus.value.filter((individu) => selectEspece.value.some((e) => e.id_espece === individu.id_espece));
  } else {
    return individus.value;
  }

});

// Liste des derniers jours 
const selectedLastDay = ref(15);
const options = ref([
    { value: 3},
    { value: 15},
    { value: 30},
    { value: 60},
    { value: 90},
    { value: 120},
    { value: 150},
    { value: 180},
    { value: 210},
    { value: 240},
    { value: 270},
    { value: 300},
    { value: 330},
    { value: 360}]);

</script>

<template>

    <!-- <button class="btn" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasLeft" aria-controls="offcanvasLeft"><i class="fa fa-bars"></i></button>
    <button class="btn btn-sm custom-btn" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasLeft" aria-controls="offcanvasLeft">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-arrow-bar-right" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M6 8a.5.5 0 0 0 .5.5h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L12.293 7.5H6.5A.5.5 0 0 0 6 8Zm-2.5 7a.5.5 0 0 1-.5-.5v-13a.5.5 0 0 1 1 0v13a.5.5 0 0 1-.5.5Z"/>
        </svg>
    </button> -->
    
    <button class="btn btn-sm btn-light opacity-75 custom-btn" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasLeft" aria-controls="offcanvasLeft">
          <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-arrow-bar-right" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M6 8a.5.5 0 0 0 .5.5h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L12.293 7.5H6.5A.5.5 0 0 0 6 8Zm-2.5 7a.5.5 0 0 1-.5-.5v-13a.5.5 0 0 1 1 0v13a.5.5 0 0 1-.5.5Z"/>
          </svg>
    </button>

    <div class="row h-100">
        <div class="offcanvas offcanvas-start custom-offcanvas" data-bs-backdrop="false" tabindex="-1" id="offcanvasLeft" aria-labelledby="offcanvasLeftLabel">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title" id="offcanvasLeftLabel">Oiseaux à cartographier</h5>
                <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
                <nav>
                    <div class="nav nav-tabs" id="nav-tab" role="tablist">
                        <button class="nav-link active" id="nav-espece-tab" data-bs-toggle="tab" data-bs-target="#nav-espece" type="button" role="tab" aria-controls="nav-espece" aria-selected="true"><h5>Espèces</h5></button>
                        <button class="nav-link" id="nav-individu-tab" data-bs-toggle="tab" data-bs-target="#nav-individu" type="button" role="tab" aria-controls="nav-individu" aria-selected="false"><h5>Individus</h5></button>
                    </div>
                </nav>
                <div class="tab-content" id="nav-tabContent">
                    <div class="tab-pane fade show active" id="nav-espece" role="tabpanel" aria-labelledby="nav-espece-tab" tabindex="0">
                        <div class="list-group list-group-flush">
                            <!-- Pour chaque espèce on génère des items-->
                            <label v-for="espece in especes" class="list-group-item">
                                <div class="d-flex flex-row">
                                    <input class="form-check-input me-3" type="checkbox" :checked="isEspeceSelected(espece)" @change="onEspeceSelected(espece)">
                                    <img id="img_espece" :src="espece.lien_img" width="50" height="50" >
                                    <div class="d-flex align-items-center ms-3">
                                        <div>
                                            {{ espece.nom_vern }}<br>
                                            <i>{{ espece.lb_nom }}</i>
                                        </div>
                                    </div>
                                </div>
                            </label> 
                        </div>

                    </div>
                    <div class="tab-pane fade" id="nav-individu" role="tabpanel" aria-labelledby="nav-individu-tab" tabindex="0">
                        <strong>Cliquez sur le nom d'un oiseau pour voir son parcours</strong>
                        <br>
                        Pour les 
                        <select v-model="selectedLastDay">
                            <option v-for="option in options" @input="$emit('sendTime', option)">{{ option.value }}</option>
                        </select>
                        derniers jours.
                        <div class="list-group list-group-flush" v-show="showIndividus">
                            <!-- Pour chaque individu on génère des items en fonction de ou des espèce(s) sélectionnée(s)-->
                            {{ selectIndividu }}
                            <label v-for="individu in filteredIndividus" class="list-group-item">
                                <div class="d-flex flex-row">
                                    
                                    <input :id="individu" :name="individu" v-model="selectIndividu" class="form-check-input me-3" type="checkbox" :value=individu @change="clearOrfetchIndividu($event)" >
                                    <label :for="individu"> {{ individu }} </label>
                                    <svg width="40" height="40" viewBox="0 0 72 61" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M72 30.5111L61.5429 26.4549C60.6514 22.327 58.4229 19.9579 58.4229 19.9579C57.0888 18.5584 55.5043 17.4482 53.7599 16.6907C52.0156 15.9331 50.1456 15.5432 48.2571 15.5432C46.3687 15.5432 44.4987 15.9331 42.7544 16.6907C41.01 17.4482 39.4255 18.5584 38.0914 19.9579L33.0171 25.2704L10.2857 0C6.85714 14.3582 10.2857 28.7163 18.6857 40.2747L0 59.2275C0 59.2275 30.48 66.4065 48.24 51.8689C57.7029 44.1155 59.8286 39.5927 61.1657 34.8186L72 30.5111ZM53.8629 31.3008C52.5257 32.7007 50.3314 32.7007 48.9943 31.3008C48.6764 30.9687 48.4243 30.5743 48.2522 30.14C48.0802 29.7058 47.9916 29.2403 47.9916 28.7702C47.9916 28.3001 48.0802 27.8346 48.2522 27.4003C48.4243 26.9661 48.6764 26.5716 48.9943 26.2396C50.3314 24.8396 52.5257 24.8396 53.8629 26.2396C55.2 27.6395 55.2 29.9009 53.8629 31.3008Z" :fill="individu.attributs.fill"/>
                                    </svg>
                                    <!-- <img src="https://static.thenounproject.com/png/80049-200.png" width="40" height="40"> -->
                                    <div class="d-flex align-items-center ms-3">
                                        <div>
                                            {{ individu.name }} <br>
                                            <i>Sexe : {{ individu.attributs.sex_libelle }} </i>
                                        </div>
                                    </div>
                                </div>
                            </label> 
                        </div>
                    </div>
                </div>
                
            </div>
            <div class="offcanvas-footer">
                <!-- <img src="https://storage.needpix.com/rsynced_images/tracks-296631_1280.png" class="rotateimg90" height="100"> -->
            </div>
        </div>
    </div>

</template>

<style scoped>

.custom-btn {
    position: absolute;
    top: 0;
    z-index: 1;
}

#img_espece {
  border-radius: 50%;
}


/* .rotateimg90 {
  -webkit-transform:rotate(90deg);
  -moz-transform: rotate(90deg);
  -ms-transform: rotate(90deg);
  -o-transform: rotate(90deg);
  transform: rotate(90deg);
} */

.custom-offcanvas {
  width: 300px; 
  top: 76px; 
  bottom: 0;
  
}

.custom-offcanvas .nav-link {
  color: inherit; 
}

.custom-offcanvas .nav-link:hover {
  color: inherit; 
}

.custom-offcanvas .nav-link:active {
  color: inherit; 
}

</style>

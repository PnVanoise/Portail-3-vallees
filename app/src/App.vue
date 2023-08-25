<script setup>

  import Leafletmap from './components/Leafletmap.vue';
  import Sidebar from './components/Sidebar.vue';
  import Apropos from './components/Apropos.vue';
  import Partenaires from './components/Partenaires.vue';
  import Aide from './components/Aide.vue';
  import Intromodal from './components/Intromodal.vue';
 
  import { ref, reactive, onMounted } from 'vue';

  // MODAL

  let isModalVisible = ref(true); //const ?

  function closeModal() {
    isModalVisible.value = false;
  }

  // ONGLETS

  let page = ref("Accueil"); //par défaut c'est la page accueil 

  const apropos_page = () => {
    page.value = 'Apropos'; //Changement de la valeur de page au clique et redirige vers composant Apropos
  };
  const aide_page = () => {
    page.value = 'Aide';
  };
  const accueil_page = () => {
    page.value = 'Accueil';
  };
  const partenaires_page = () => {
    page.value = 'Partenaires';
  };

  // PROPS

  let individusRef = ref([]);

  const getIndividus = (individus) => {
      individusRef.value = individus;
      console.log("app:", individusRef.value);
  };

  let timeRef = ref(null);

  const getTime = (timeSelect) => {
    console.log(timeSelect);
    timeRef.value = timeSelect.name;
  };
  
</script>

<template>
 
  <!-- <Intromodal v-show="isModalVisible" @close="closeModal"/> -->
 
  <nav class="navbar fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand">
        <img src="../GPS3V.png" class="bi me-2" width="200" height="60">
      </a>
      <ul class="navbar-nav justify-content-end flex-row gap-3">
        <li class="nav-item">
          <a :class="['nav-link', { 'active': page === 'Accueil' }]" @click="accueil_page"><strong>ACCUEIL</strong></a>
        </li>
        <li class="nav-item">
          <a :class="['nav-link', { 'active': page === 'Apropos' }]" @click="apropos_page"><strong>A PROPOS</strong></a>
        </li>
        <li class="nav-item">
          <a :class="['nav-link', { 'active': page === 'Partenaires' }]" @click="partenaires_page"><strong>PARTENAIRES</strong></a>
        </li>
        <li class="nav-item">
          <a :class="['nav-link', { 'active': page === 'Aide' }]" @click="aide_page"><strong>AIDE</strong></a>
        </li>
      </ul>
    </div>
  </nav>


  <div class="d-flex flex-row">
    <div class="leaflet-container">
      <div class="col-xs-12 col-sm-12 col-md-7 col-lg-8">
        <Leafletmap v-if="page=='Accueil'" :individus="individusRef" :time="timeRef"/>

        <Sidebar v-if="page=='Accueil'" @send-individu="getIndividus" @sendTime="getTime"/>



        <Apropos v-if="page=='Apropos'"/>
        
        <Partenaires v-if="page=='Partenaires'"/>

        <Aide v-if="page=='Aide'"/>

        

      </div>
    </div>
  </div>

</template>

<style scoped>

/* .container {
  height: 100%;
  width: 100%;
  display: flex;
  margin: 0;
  padding: 0;
  flex-direction: column;
} */



.flex-grow-1 {
  overflow: hidden;
}

.nav-link strong {
  color: #FFFFFF;  
}

.nav-link.active strong, .nav-link strong:hover {
  color: #F16764;
}

.leaflet-container {
  min-height: 88vh;
  flex: 1; 
  position: relative;
  z-index: 0;
}

</style>

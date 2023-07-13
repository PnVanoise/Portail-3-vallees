<script setup>

  import Leafletmap from './components/Leafletmap.vue';
  import Apropos from './components/Apropos.vue';
  import Sidebar from './components/Sidebar.vue';
  import { ref, onMounted } from 'vue';

  let page = ref("Accueil"); //par défaut c'est la page accueil 

  const apropos_page = () => {
    page.value = 'Apropos'; //Changement de la valeur de page au clique et redirige vers composant Apropos
  }
  const aide_page = () => {
    page.value = 'Aide';
  }
  const accueil_page = () => {
    page.value = 'Accueil';
  }
  const partenaires_page = () => {
    page.value = 'Patenaires';
  }

  let nameRef = ref(null);

  const getIndividu = (individu) => {
    console.log(individu);
    nameRef.value = individu.name;
  }

  let timeRef = ref(null);

  const getTime = (timeSelect) => {
    console.log(timeSelect);
    timeRef.value = timeSelect.name;
  }
  
</script>

<template>
  <!-- <div class="d-flex flex-row">

    <header id="header" class="d-flex flex-wrap justify-content-center py-2" >
      
      <div class="d-flex justify-content-start"> -->
      <!-- <div class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none"> -->
        <!-- <img src="../GPS3V.png" class="bi me-2" width="200" height="60">
      </div>
      
      <div class="d-flex gap-2 justify-content-end">

        <button class="btn btn-danger btn-sm align-self-end" @click="accueil_page">ACCUEIL</button>
        <button class="btn btn-danger btn-sm align-self-end" @click="apropos_page">A PROPOS</button>
        <button class="btn btn-danger btn-sm align-self-end" @click="partenaires_page">PARTENAIRES</button> 
        <button class="btn btn-danger btn-sm align-self-end" @click="aide_page">AIDE</button>

      </div>

    </header>
  </div>  -->

  <nav class="navbar fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand">
        <img src="../GPS3V.png" class="bi me-2" width="200" height="60">
      </a>
      <!-- <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button> -->
      <!-- <div class="collapse navbar-collapse" id="navbarCollapse"> -->
      <ul class="navbar-nav justify-content-end flex-row gap-2">
        <li class="nav-item">
          <!-- <button class="btn btn-danger btn-sm" @click="accueil_page">ACCUEIL</button> -->
          <a class="nav-link active" @click="accueil_page">ACCUEIL</a>
        </li>
        <li class="nav-item">
          <!-- <button class="btn btn-danger btn-sm" @click="apropos_page">A PROPOS</button> -->
          <a class="nav-link" @click="apropos_page">A PROPOS</a>
        </li>
        <li class="nav-item">
          <!-- <button class="btn btn-danger btn-sm" @click="partenaires_page">PARTENAIRES</button>  -->
          <a class="nav-link" @click="partenaires_page">PARTENAIRES</a>
        </li>
        <li class="nav-item">
          <!-- <button class="btn btn-danger btn-sm" @click="aide_page">AIDE</button> -->
          <a class="nav-link" @click="aide_page">AIDE</a>
        </li>
      </ul>
      <!-- </div> -->
    </div>
  </nav>

  

  <div class="d-flex flex-row">
    <div class="leaflet-container">
      <div class="col-xs-12 col-sm-12 col-md-7 col-lg-8">
        <Leafletmap v-if="page=='Accueil'" :name="nameRef" :time="timeRef"/>

        <!-- <button class="btn btn-sm btn-light opacity-75 custom-btn" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasLeft" aria-controls="offcanvasLeft">
          <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-arrow-bar-right" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M6 8a.5.5 0 0 0 .5.5h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L12.293 7.5H6.5A.5.5 0 0 0 6 8Zm-2.5 7a.5.5 0 0 1-.5-.5v-13a.5.5 0 0 1 1 0v13a.5.5 0 0 1-.5.5Z"/>
          </svg>
        </button> -->
      </div>
      <div class="col-xs-12 col-sm-12 col-md-5 col-lg-4">
        <Sidebar v-if="page=='Accueil'" @send-individu="getIndividu" @sendTime="getTime"/>
      </div>
    </div>
  </div>



  <Apropos v-if="page=='Apropos'"/>


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

.leaflet-container {
  min-height: 100vh;
  /* flex: 1; */
  /* position: relative; */
  /* z-index: 0; */
}

/* .custom-btn {
    position: absolute;
    top: 0;
    z-index: 1;
} */

</style>

<script setup>
  import Leafletmap from './components/Leafletmap.vue';
  import Apropos from './components/Apropos.vue';
  import Partenaires from './components/Partenaires.vue';
  import Aide from './components/Aide.vue';
  import Intromodal from './components/Intromodal.vue';
 
  import { ref } from 'vue';

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

  
</script>

<template>
 
  <Intromodal v-show="isModalVisible" @close="closeModal"/>
 
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


  <div id="content" >
      
      <Leafletmap v-if="page=='Accueil'" />

      <Apropos v-if="page=='Apropos'"/>
      
      <Partenaires v-if="page=='Partenaires'"/>

      <Aide v-if="page=='Aide'"/>

  </div>

</template>

<style scoped>

.flex-grow-1 {
  overflow: hidden;
}

.nav-link strong {
  color: #FFFFFF;  
}

.nav-link.active strong, .nav-link strong:hover {
  color: #F16764;
}

#content {
  position: relative;
  /* width: 100%; */
  /* height: 100%; */
  /* min-height: 88vh; */
  /* flex: 1;  */
  background-color: #FFFFFF;
}

</style>

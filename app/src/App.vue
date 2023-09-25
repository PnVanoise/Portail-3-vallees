<script setup>
  import Leafletmap from './components/Leafletmap.vue';
  import Apropos from './components/Apropos.vue';
  import Partenaires from './components/Partenaires.vue';
  // import Aide from './components/Aide.vue';
  import Intromodal from './components/Intromodal.vue';
 
  import { ref, computed } from 'vue';

  // Config Items 
  const appLogo = computed(() => window.config.app_logo);
  const copyrightLogo = computed(() => window.config.img_partenaires.pnv);
  const pnUrl = computed(() => window.config.pnx_url);
  const onglet = window.config.onglets;

  // Modal
  let isModalVisible = ref(true); 

  function closeModal() {
    isModalVisible.value = false;
  }

  // Onglets
  let page = ref(onglet.onglet_a); //par défaut c'est la page accueil 

  function changePage(selectOnglet) {
    page.value = selectOnglet;
  }
  
</script>

<template>
 
  <Intromodal v-show="isModalVisible" @close="closeModal"/>

  <nav class="navbar fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand">
        <img :src="appLogo" class="ms-4" width="200" height="60">        
      </a>
      <ul class="navbar-nav justify-content-end flex-row gap-3 me-4">
        <li class="nav-item" v-for="(ongletLabel, ongletKey) in onglet" :key="ongletKey">
          <a :class="['nav-link', { 'active': page === ongletLabel }]" @click="changePage(ongletLabel)"><strong>{{ ongletLabel }}</strong></a>
        </li>
      </ul>
    </div>
  </nav>


  <div id="content" >

      <Leafletmap v-if="page==onglet.onglet_a" />

      <Apropos v-if="page==onglet.onglet_b"/>
      
      <Partenaires v-if="page==onglet.onglet_c"/>

      <!-- <Aide v-if="page=='Aide'"/> -->

  </div>

  <footer v-if="page!==onglet.onglet_a">
    <div id="footer" class="m-2">
    <small style="color: white;">
      &copy; Copyright GPS 3 Vallées, 2023
      <a :href="pnUrl" target="_blank">
        <img :src="copyrightLogo" width="100" >
      </a><br>
      OpenSource<br> 
      <a href="https://github.com/PnVanoise/Portail-3-vallees" target="_blank">
        <img src="/public/images/github.png" width="30">
      </a><br>
      <small>Auteur·ices : Alix Cornu-Lachamp, Claire Lagaye, Christophe Chillet</small> 
    </small>
    </div>
  </footer>

</template>

<style scoped>


.nav-link strong {
  color: #FFFFFF;  
}

.nav-link.active strong, .nav-link strong:hover {
  color: #F16764;
}


#content {
  position: relative;
  background-color: #FFFFFF;
}

#footer {
  text-align: center;
  bottom: 0;
  left: 0;
  right: 0;
}

</style>

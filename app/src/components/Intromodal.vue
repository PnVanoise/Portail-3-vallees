<script setup>
import { ref, onMounted, computed } from 'vue';

// Config Items 
const modalLogo = computed(() => window.config.modal_logo);

let myModal = ref(null);

onMounted(() => {

    const modal = myModal.value;
    modal.addEventListener('shown.bs.modal', () => {
        const myInput = document.getElementById('myInput');
        myInput.focus();
        // console.log('Modal loaded');
    });

});

// Evenement envoyé à App 
const emit = defineEmits(['close']);

</script>

<template>
    <!-- Modal -->
    <div class="modal" id="myModal" ref="myModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">Besoin d'aide ?</h3>
                    <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>
                        Bienvenue sur le portail cartographique :
                        <br><img :src="modalLogo" width="200" height="200">
                        <br>Cliquez dès à présent sur une <strong>espèce</strong> pour ouvrir et visualiser les <strong>déplacements</strong> de ses <strong>individus équipés.</strong>
                        <br> Pour plus d'informations, consultez les onglets <strong>A PROPOS</strong> et <strong>PARTENAIRES.</strong>
                        <!-- <br>En cas de doute, rendez-vous sur l'onglet <strong>AIDE.</strong> -->
                    </p>
                    
                </div>
            </div>

        </div>
    </div>
</template>

<style>

#myModal {
    position: fixed;
    z-index: 9999;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); 
    display: flex; 
    justify-content: center;
    align-items: center; 
} 

.modal-content {
    overflow: auto;
    visibility: visible;
}

p {
    text-align: center;
}

</style>
<script setup>
import { ref, onMounted } from 'vue';

let myModal = ref(null);

onMounted(() => {

    const modal = myModal.value;
    modal.addEventListener('shown.bs.modal', () => {
        const myInput = document.getElementById('myInput');
        myInput.focus();
        console.log('Modal loaded');
    });

});

const emit = defineEmits(['close']);

</script>

<template>
    <!-- Modal -->
    <div class="modal" id="myModal" ref="myModal">
        <div class="modal-dialog">
            <!-- Modal content-->
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">Besoin d'aide ?</h3>
                    <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>
                        Bienvenue sur le portail cartographique
                        <br><img src="/GPS3V_black.png" width="200" height="200">
                        <br>Cliquez dès à présent sur une espèce pour ouvrir et visualiser les déplacements de ses individus équipés
                        <br> Pour plus d'informations, consultez les onglets A PROPOS et PARTENAIRES
                        <br>En cas de doute, rendez-vous sur l'onglet AIDE
                    </p>
                    
                </div>
                <!-- <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fermer</button>
                </div> -->
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
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black overlay */
    display: flex; 
    justify-content: center;
    align-items: center; 

/* 
    display: flex;
    top: 20%;
    z-index: 1; */
} 

.modal-content {
    overflow: auto;
    visibility: visible;
}

p {
    text-align: center;
}

</style>
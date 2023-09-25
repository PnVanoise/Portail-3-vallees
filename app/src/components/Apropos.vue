<script setup>
import { computed } from 'vue';

// Config Items 
const aproposLogo = computed(() => window.config.img_apropos);

</script>

<template>
  <div class="d-flex justify-content-center">
    <div id="context-text" class="col-10 m-5">
      <div class="row mb-5">
        <h1>La Convention Trois Vallées</h1>
      </div>
      <div class="row">
        <h5>Le 24 janvier 2022, aux Allues, a eu lieu le renouvellement de la convention de partenariat en faveur des
          oiseaux patrimoniaux sur le domaine skiable des 3 Vallées. Les communes des Belleville, des Allues et de
          Courchevel ont rejoint ce partenariat qui associait déjà depuis 2019 les sociétés de remontées mécaniques des
          Menuires, de Val Thorens, de Méribel et de Courchevel (SEVABEL, SETAM, Méribel Alpina, S3V), aux côtés de
          l’Office national des forêts, l’Office français de la biodiversité, la Fédération des chasseurs de Savoie et le
          Parc national de la Vanoise.</h5>
      </div>
      <div class="row my-3">
        <img :src="aproposLogo.convention_signataires" class="rounded mx-auto d-block" style="height: 350px;width: auto;">
      </div>

      <div class="row">

        <h4><br>Un engagement dans la durée pour mieux connaître et protéger les oiseaux sur
          le domaine skiable des 3 Vallées</h4>

        <p><br>Ces acteurs de la montagne se sont engagés jusqu’en 2024 à <strong>poursuivre l’amélioration de la connaissance
            et la protection de quatre espèces d’oiseaux remarquables - tétras-lyre, lagopède alpin, perdrix bartavelle et
            aigle royal </strong>- fréquentant les domaines skiables en hiver.</p>

        <p>Avec le développement des loisirs de plein air en hiver, ces espèces fragiles sont en effet <strong>exposées à
            diverses sources de dérangement pouvant impacter leur survie</strong> en cette saison difficile pour eux.</p>

        <p>Dans ce contexte, des <strong>espaces dits refuge</strong> (ou de quiétude) ont été créés en faveur du
          tétras-lyre, où la pénétration touristique hivernale est déconseillée, voire (plus rarement) interdite. À noter
          que <strong>le tétras-lyre est une espèce «&nbsp;parapluie&nbsp;»</strong> dont la protection bénéficie à de
          nombreuses autres espèces. Ces refuges, implantés dans ou en dehors des domaines skiables, ne sont pas toujours
          compris des pratiquants et subissent des pressions de dérangement très variables.</p>

        <p>Une première étude a été menée de 2019 à 2021 dans le cadre d’un premier partenariat avec les domaines skiables
          sur l’ensemble du domaine des 3 Vallées avec la Réserve naturelle nationale de Plan de Tuéda attenante.
          L’objectif était de <strong>mieux comprendre l’utilisation de l’espace</strong> (domaine vital, rythme
          d’activités journalières, …) <strong>par les oiseaux</strong> étudiés et de <strong>mieux évaluer les
            dérangements</strong>.</p>

        <p>Les enseignements de ces trois premières années de suivi sont <strong>riches mais encore incomplets</strong>
          pour pouvoir proposer des <strong>actions de protection et de gestion réellement adaptées</strong>.</p>

        <h4><br>Un partenariat financier important pour mettre en œuvre des solutions efficaces</h4>

        <ul>
          <p><br>Les partenaires impliqués dans cette première étude, rejoints par les trois communes
          concernées, ont décidé de s’engager pour 3 ans pour&nbsp;:</p>
          <li><strong>compléter les données acquises</strong> lors de la première étude concernant
            l’utilisation spatiale et temporelle du domaine par les oiseaux et l’impact des dérangements,</li>
          <li>mettre en place des <strong>solutions de gestion s’appuyant directement sur les
              résultats</strong> des études (zones de quiétudes plus adaptées, sensibilisation plus ciblée mais aussi
            visualisation de câbles de remontées mécaniques par balises),</li>
          <li><strong>vulgariser largement les résultats</strong> pour sensibiliser le grand public.
          </li>
        </ul>

        <p>Sur les 3 ans, les 4 sociétés de remontées mécaniques ainsi que les communes des 3 Vallées
        et la Fédération des chasseurs de Savoie se sont engagées sur un montant total de 142&nbsp;500 €. Ce financement
        va notamment permettre <strong>l'achat des balises satellitaires</strong> qui seront posées sur les oiseaux et
        le <strong>matériel de capture</strong> nécessaire.</p>

      <p>L’Office français de la biodiversité, l’Office national des forêts et le Parc national de la
        Vanoise mèneront les <strong>opérations de capture des oiseaux, de pose de balises satellitaires et de suivi des
          oiseaux</strong>, sur la base d’un protocole défini par les experts, dont l’Observatoire des galliformes de
        montagne.</p>

      <p>L’ensemble des données seront analysées puis communiquées à l’ensemble des cosignataires de
        la convention ainsi qu’aux observatoires de la biodiversité.</p>

      <p>À travers cette nouvelle convention, État, collectivités, opérateurs publics et exploitants
        du domaine skiable des 3 Vallées poursuivent leur collaboration <strong>au service de la biodiversité et d'un
          tourisme économiquement performant mais préservant son capital écologique</strong>.</p>

      <p>Par cette démarche volontariste, le site unique des 3 Vallées est également devenu un
        <strong>site de référence national </strong>pour étudier les effets des activités humaines hivernales sur un
        cortège d’espèces emblématiques des Alpes.</p>

      <p>Et à l’approche des championnats du monde de ski alpin qui seront accueillis sur place en
        2023, cette convention montre toute la <strong>dynamique de conciliation entre activités sportives et
          biodiversité</strong> et le caractère exemplaire des partenariats développés en Savoie.</p>

    </div>

  </div>
</div>
</template>

<style scoped>

li{
  margin-left: 50px;
}

h1 {
  text-align: center;
}


p, h5 {
  text-align: justify;
}

</style>

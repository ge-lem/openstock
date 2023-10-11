<template>
  <div class="container text-justify p-4 col-lg-8 offset-lg-2">
    <main class="row">
      <h1 class="os-page-title">Crédits</h1>
      <PartageTools />

      <div class="os-page-content">
        <h3>Conception du site</h3>
        <p><strong>Réalisation :</strong> Nom</p>
        <p><strong>Contenus :</strong> </p>
        <p>
          <strong>Conception graphique :</strong>
        </p>
        <h3>Outils de gestion et d'administration du site</h3>
        <p>
          <strong>Gestion des contenus :</strong> ce site fonctionne avec
          les outils Django et VusJs.
        </p>
        <p>
          <strong>Gestion des cookies :</strong>
        </p>
        <h3>Photographies/Vidéos</h3>
        <p>Droits réservés :</p>
        <p>© Structure</p>
      </div>

      <PartageTools />

      <footer class="os-page-date">
        <div>
          <p>
            <time class="published" datetime="2023-09-01T00:00:00+02:00">
              Publié le 01 septembre 2023
            </time>
          </p>
        </div>
      </footer>
    </main>
  </div>
</template>
<script setup>
import PartageTools from "@/components/ui/PartageTools.vue";
</script>

<template>
  <div class="container text-justify p-4 col-lg-8 offset-lg-2">
    <main class="row">
      <h1 class="os-page-title">Contact</h1>
      <PartageTools/>
      
      <div class="os-page-content">
        <p>
          <strong>Structure</strong><br />
          80 rue Example<br />
          99999 Ville<br />
        </p>
        <p>
          <a href="mailto:contact@exemple.fr"
            >contact@exemple</a
          >
        </p>
      </div>

      <PartageTools/>
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

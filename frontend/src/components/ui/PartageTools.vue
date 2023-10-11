<template>
  <div class="os-partage-tools">
    <ul class="list-inline">
      <li class="list-inline-item">
        <span class="libelle">Imprimer</span>
        <button
          class="btn btn-link"
          title="Imprimer"
          onclick="window.print(); return false;"
        >
          <svg class="svg-icon">
            <use href="#printer"></use>
          </svg>
          <span aria-hidden="true" class="icon icon-printer"></span>
        </button>
      </li>
      <li class="list-inline-item">
        <span class="libelle">Partager</span>
        <a :href="fullPath" rel="bookmark" title="Permalink to Contact">
          <svg class="svg-icon">
            <use href="#favoris"></use>
          </svg>
        </a>
      </li>
      <li class="list-inline-item">
        <a
          :href="'https://www.facebook.com/sharer.php?u=' + fullPathEncoded"
          target="_blank"
        >
          <svg class="svg-icon">
            <use href="#facebook"></use>
          </svg>
        </a>
      </li>
      <li class="list-inline-item">
        <a
          :href="'https://twitter.com/intent/tweet?url=' + fullPathEncoded"
          target="_blank"
        >
          <svg class="svg-icon">
            <use href="#twitter"></use>
          </svg>
        </a>
      </li>
      <li class="list-inline-item">
        <a
          :href="
            'https://www.linkedin.com/sharing/share-offsite/?url=' +
            fullPathEncoded
          "
          target="_blank"
        >
          <svg class="svg-icon">
            <use href="#linkedin"></use>
          </svg>
        </a>
      </li>
    </ul>
  </div>
  <template></template>
</template>
<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const fullPath = computed(() => {
  return window.location.origin + "/#" + route.fullPath;
});
const fullPathEncoded = computed(() => {
  return encodeURIComponent(fullPath.value);
});
</script>

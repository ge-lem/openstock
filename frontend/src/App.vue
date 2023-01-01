<template>
  <div class="container">
    <div v-if="firstCheck">
      <Header />
      <router-view class="mr-5 ml-5" />
      <Footer />
    </div>
    <modal
      id="modal-cookie"
      title="Utilisation de cookie"
      :show="showCookie"
      hide-footer
    >
      <p>
        Ce site utilise des cookies afin de fonctionner. Ils sont uniquement
        utilisés pour gerer la session de l'utilisateur. Il n'y a pas de cookie
        de tierces parties ou d'utilisation à des fins statistiques.
      </p>

      <div>
        <div class="btn-group" role="group" aria-label="Accepter">
          <button type="button" class="btn btn-primary" @click="validCookie">
            J'ai compris
          </button>
        </div>
      </div>
    </modal>
    <svg style="display: none" version="2.0">
      <defs>
        <symbol id="edit" viewBox="0 0 20 20">
          <path
            fill="#fff"
            d="M19.404,6.65l-5.998-5.996c-0.292-0.292-0.765-0.292-1.056,0l-2.22,2.22l-8.311,8.313l-0.003,0.001v0.003l-0.161,0.161c-0.114,0.112-0.187,0.258-0.21,0.417l-1.059,7.051c-0.035,0.233,0.044,0.47,0.21,0.639c0.143,0.14,0.333,0.219,0.528,0.219c0.038,0,0.073-0.003,0.111-0.009l7.054-1.055c0.158-0.025,0.306-0.098,0.417-0.211l8.478-8.476l2.22-2.22C19.695,7.414,19.695,6.941,19.404,6.65z M8.341,16.656l-0.989-0.99l7.258-7.258l0.989,0.99L8.341,16.656z M2.332,15.919l0.411-2.748l4.143,4.143l-2.748,0.41L2.332,15.919z M13.554,7.351L6.296,14.61l-0.849-0.848l7.259-7.258l0.423,0.424L13.554,7.351zM10.658,4.457l0.992,0.99l-7.259,7.258L3.4,11.715L10.658,4.457z M16.656,8.342l-1.517-1.517V6.823h-0.003l-0.951-0.951l-2.471-2.471l1.164-1.164l4.942,4.94L16.656,8.342z"
          ></path>
        </symbol>
        <symbol id="eye" viewBox="0 0 20 20">
          <path
            fill="#fff"
            d="M19.471,8.934L18.883,8.34c-2.096-2.14-4.707-4.804-8.903-4.804c-4.171,0-6.959,2.83-8.996,4.897L0.488,8.934c-0.307,0.307-0.307,0.803,0,1.109l0.401,0.403c2.052,2.072,4.862,4.909,9.091,4.909c4.25,0,6.88-2.666,8.988-4.807l0.503-0.506C19.778,9.737,19.778,9.241,19.471,8.934z M9.98,13.787c-3.493,0-5.804-2.254-7.833-4.3C4.182,7.424,6.493,5.105,9.98,5.105c3.536,0,5.792,2.301,7.784,4.332l0.049,0.051C15.818,11.511,13.551,13.787,9.98,13.787z"
          ></path>
          <circle fill="#fff" cx="9.98" cy="9.446" r="1.629"></circle>
        </symbol>
      </defs>
    </svg>
  </div>
</template>

<script setup>
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import Modal from "@/plugins/modal";
import Header from "@/components/AppHeader.vue";
import Footer from "@/components/AppFooter.vue";

import { ref, onBeforeMount } from "vue";

const showCookie = ref(false);
const store = useAuthStore();
const { firstCheck } = storeToRefs(store);

onBeforeMount(async () => {
  document.title = import.meta.env.VITE_APP_TITLE;
  if (localStorage.getItem("cookiepopup") == null) {
    showCookie.value = true;
  }
  store.checkAuth();
});
function validCookie() {
  localStorage.setItem("cookiepopup", "true");
  showCookie.value = false;
}
</script>
<style>
/* -----
SVG Icons - svgicons.sparkk.fr
----- */

.svg-icon {
  width: 2em;
  height: 2em;
}
.svg-icon-small {
  width: 1em;
  height: 1em;
}
</style>

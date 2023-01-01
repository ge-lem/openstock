<template>
  <div class="row d-flex justify-content-center">
    <div class="col-md-6">
      <div class="card px-5 py-5" id="form1">
        <div v-if="isAuthenticated">
          <div class="text-center d-flex flex-column">
            <span class="text-center fs-1">Vous êtes bien connecté.</span>
          </div>
        </div>
        <div v-if="failed">
          <div class="text-center d-flex flex-column">
            <span class="text-center fs-1"
              >Les informations d'activation ne sont pas valides.</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
const store = useAuthStore();
const { isAuthenticated } = storeToRefs(store);

const route = useRoute();
const router = useRouter();

const failed = ref(false);

let infos = {};

onMounted(async () => {
  infos.uid = route.params["uid"];
  infos.token = route.params["token"];
  try {
    await store.activateUser(infos);
    router.push({ name: "login" });
  } catch (error) {
    failed.value = true;
    console.log(error);
  }
});
</script>

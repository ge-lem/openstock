<template>
  <div class="row d-flex justify-content-center">
    <div class="col-md-6">
      <div class="card px-5 py-5" id="form1">
        <div v-if="!isSent">
          <div
            v-for="error in errors"
            :key="error"
            class="alert alert-danger"
            role="alert"
          >
            {{ error }}
          </div>
          <form v-if="!isAuthenticated && !casAuth">
            <div class="mb-3">
              <label for="inputEmail" class="form-label">Votre email</label>
              <input
                type="text"
                v-model="email"
                class="form-control"
                id="inputEmail"
              />
            </div>

            <div class="mb-3">
              <button @click.prevent="sendReset" class="btn btn-dark w-100">
                Envoyer la demande
              </button>
            </div>
          </form>
        </div>
        <div v-else>
          <span class="text-center fs-3"
            >Si le mail existe un mail vient d'être envoyé.</span
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
const store = useAuthStore();
const { isAuthenticated } = storeToRefs(store);

const casAuth = import.meta.env.VITE_CAS_AUTH == "true";

const email = ref("");

const errors = ref([]);
const isSent = ref(false);

async function sendReset() {
  try {
    errors.value = [];
    await store.resetPassword(email.value);
    isSent.value = true;
  } catch (error) {
    if (error.response.status == 400) {
      if ("non_field_errors" in error.response.data) {
        errors.value = error.response.data["non_field_errors"];
      } else if ("email" in error.response.data)
        errors.value = error.response.data["email"];
    } else {
      console.log(error);
    }
  }
}
</script>

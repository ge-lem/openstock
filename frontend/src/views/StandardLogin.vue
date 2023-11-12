<template>
  <div class="row d-flex justify-content-center">
    <div class="col-md-6">
      <div class="card px-5 py-5" id="form1">
        <div
          v-for="error in errors"
          :key="error"
          class="alert alert-danger"
          role="alert"
        >
          {{ error }}
        </div>
        <form v-if="!isAuthenticated && !casAuth" ref="flogin">
          <div class="mb-3">
            <label for="inputUsername" class="form-label"
              >Nom Utilisateur</label
            >
            <input
              type="text"
              v-model="username"
              class="form-control"
              id="inputUsername"
              required
            />
          </div>
          <div class="mb-3">
            <label for="inputPassword1" class="form-label">Mot de passe</label>
            <input
              type="password"
              v-model="password"
              class="form-control"
              id="inputPassword1"
              required
            />
          </div>
          <div class="mb-3">
            <button @click.prevent="login" class="btn btn-dark w-100">
              Login
            </button>
          </div>
          <div class="mb-3">
            Pas de compte ? Demandez à un utilisateur de vous inviter.
          </div>
          <div class="mb-3">
            <router-link to="password/reset">Mot de passe perdu.</router-link>
          </div>
        </form>
        <div v-if="!isAuthenticated && casAuth">
          <div class="mb-3">
            <button @click.prevent="casLogin" class="btn btn-dark w-100">
              Login CAS
            </button>
          </div>
        </div>
        <div v-if="isAuthenticated">
          <div class="text-center d-flex flex-column">
            <span class="text-center fs-1">Vous êtes bien connecté.</span>
          </div>
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

const casAuth = import.meta.env.VITE_APP_CAS_AUTH == "true";

const username = ref("");
const password = ref("");
const flogin = ref();

const errors = ref([]);

async function casLogin() {
  await store.casLogin();
}

async function login() {
  if (flogin.value.checkValidity()) {
    try {
      errors.value = [];
      await store.login(username.value, password.value);
    } catch (error) {
      if (error.response.status == 400) {
        if ("non_field_errors" in error.response.data) {
          errors.value = error.response.data["non_field_errors"];
        }
      } else if (error.response.status == 429) {
        errors.value = ["Trop de tentatives, réessayez demain"];
      }
    }
  } else {
    flogin.value.reportValidity();
  }
}
</script>

<template>
  <div class="row d-flex justify-content-center">
    <div class="col-md-6">
      <div class="card px-5 py-5" id="form1">
        <form v-if="!isAuthenticated && !success" class="form needs-validation">
          <div
            v-for="error in errors.non_field_errors"
            :key="error"
            class="alert alert-danger"
            role="alert"
          >
            {{ error }}
          </div>
          <div class="mb-3">
            <label for="inputUsername" class="form-label"
              >Nom Utilisateur</label
            >
            <input
              type="text"
              v-model="reginfos.username"
              class="form-control"
              id="inputUsername"
              :class="{ 'is-invalid': errors.username.length }"
              required
            />
            <div
              v-for="error in errors.username"
              :key="error"
              class="invalid-feedback"
            >
              {{ error }}
            </div>
          </div>
          <div class="mb-3">
            <label for="inputPassword1" class="form-label">Mot de passe</label>
            <input
              type="password"
              v-model="reginfos.password"
              class="form-control"
              id="inputPassword1"
              :class="{ 'is-invalid': errors.password.length }"
              required
            />
            <div
              v-for="error in errors.password"
              :key="error"
              class="invalid-feedback"
            >
              {{ error }}
            </div>
          </div>
          <div class="mb-3">
            <label for="inputPassword2" class="form-label"
              >Confirmation mot de passe</label
            >
            <input
              type="password"
              v-model="reginfos.re_password"
              class="form-control"
              id="inputPassword2"
              :class="{ 'is-invalid': errors.password_mismatch.length }"
              required
            />
            <div
              v-for="error in errors.password_mismatch"
              :key="error"
              class="invalid-feedback"
            >
              {{ error }}
            </div>
          </div>
          <div class="mb-3">
            <label for="inputEmail" class="form-label">Email</label>
            <input
              type="email"
              v-model="reginfos.email"
              class="form-control"
              id="inputEmail"
              :class="{ 'is-invalid': errors.email.length }"
              required
            />
            <div
              v-for="error in errors.email"
              :key="error"
              class="invalid-feedback"
            >
              {{ error }}
            </div>
          </div>
          <div class="mb-3">
            <button @click.prevent="register" class="btn btn-dark w-100">
              Créer un compte
            </button>
          </div>
        </form>
        <div v-if="isAuthenticated">
          <div class="text-center d-flex flex-column">
            <span class="text-center fs-1">Vous êtes bien connecté.</span>
          </div>
        </div>
        <div v-if="success">
          <div class="text-center d-flex flex-column">
            <span class="text-center fs-1"
              >Votre compte est bien créé. Un mail a été envoyé afin que vous
              l'activiez.</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
const store = useAuthStore();
const { isAuthenticated } = storeToRefs(store);

const route = useRoute();

const success = ref(false);

const reginfos = reactive({
  username: "",
  password: "",
  re_password: "",
  email: "",
  invitation_key: "",
});

const errors = reactive({
  username: [],
  password: [],
  re_password: [],
  email: [],
  password_mismatch: [],
  non_field_errors: [],
});

function resetErrors() {
  errors.username = [];
  errors.password = [];
  errors.re_password = [];
  errors.email = [];
  errors.password_mismatch = [];
  errors.non_field_errors = [];
}

async function register() {
  try {
    reginfos.invitation_key = route.query["key"];
    resetErrors();
    await store.registerUser(reginfos);
    success.value = true;
  } catch (error) {
    if (error.response.status == 400) {
      console.log(error.response);
      for (const prop in error.response.data) {
        errors[prop] = error.response.data[prop];
      }
    } else if (error.response.status == 401) {
      errors.non_field_errors.push("Vous devez avoir une invitation valide");
      console.log("Invitation failed");
    }
  }
}
</script>

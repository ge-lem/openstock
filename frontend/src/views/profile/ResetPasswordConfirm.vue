<template>
  <div class="row d-flex justify-content-center">
    <div class="col-md-6">
      <div class="card px-5 py-5" id="form1">
        <div v-if="!isSent" class="text-center d-flex flex-column">
          <span class="text-center fs-3">Changement de mot de passe</span>
          <form>
            <div
              v-for="error in errors.non_field_errors"
              :key="error"
              class="alert alert-danger"
              role="alert"
            >
              {{ error }}
            </div>
            <div
              v-for="error in errors.uid"
              :key="error"
              class="alert alert-danger"
              role="alert"
            >
              {{ error }}
            </div>
            <div class="mb-3">
              <label for="inputPassword1" class="form-label"
                >Nouveau mot de passe</label
              >
              <input
                type="password"
                v-model="infos.new_password"
                class="form-control"
                id="inputPassword1"
                :class="{ 'is-invalid': errors.new_password.length }"
                required
              />
              <div
                v-for="error in errors.new_password"
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
                v-model="infos.re_new_password"
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
              <button @click.prevent="resetPassword" class="btn btn-dark w-100">
                Valider
              </button>
            </div>
          </form>
        </div>
        <div v-else>
          <span class="text-center fs-3"
            >Votre mot de passe est modifié vous pouvez vous connecter.
          </span>
          <router-link to="/login">Login</router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
const store = useAuthStore();
const { isAuthenticated } = storeToRefs(store);

const route = useRoute();
const router = useRouter();

const failed = ref(false);
const isSent = ref(false);

let infos = {};
const errors = reactive({
  new_password: [],
  re_new_password: [],
  password_mismatch: [],
  non_field_errors: [],
  uid: [],
});
function resetErrors() {
  errors.new_password = [];
  errors.re_new_password = [];
  errors.password_mismatch = [];
  errors.non_field_errors = [];
  errors.uid = [];
}
async function resetPassword() {
  try {
    resetErrors();
    await store.resetPasswordConfirm(infos);
    isSent.value = true;
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

onMounted(async () => {
  infos.uid = route.params["uid"];
  infos.token = route.params["token"];
});
</script>

<template>
  <div class="card">
    <div class="card-header">
      <h3>Votre profile</h3>
    </div>
    <div class="card-body">
      <div class="row">
        <form id="editor-form" class="form needs-validation" novalidate>
          <div class="mb-3">
            <label class="form-label" for="username">Username</label
            ><input
              id="username"
              v-model="authUser.username"
              class="form-control"
              type="text"
              readonly
              disabled
            />
          </div>
          <div class="mb-3">
            <label class="form-label" for="firstname">Prénom</label
            ><input
              id="firstname"
              v-model="tempValue.first_name"
              class="form-control"
              type="text"
              required
              :readonly="casAuth"
              :disabled="casAuth"
            />
          </div>
          <div class="mb-3">
            <label class="form-label" for="lastname">Nom</label
            ><input
              id="lastname"
              v-model="tempValue.last_name"
              class="form-control"
              type="text"
              required
              :readonly="casAuth"
              :disabled="casAuth"
            />
          </div>
          <div class="mb-3">
            <label class="form-label" for="email">Email</label
            ><input
              id="email"
              v-model="tempValue.email"
              class="form-control"
              type="email"
              required
              :class="{ 'is-invalid': errors.email.length }"
              :readonly="casAuth"
              :disabled="casAuth"
            />
            <div
              v-for="error in errors.email"
              :key="error"
              class="invalid-feedback"
            >
              {{ error }}
            </div>
          </div>
          <div class="mt-2" role="group">
            <button
              class="btn btn-primary"
              type="button"
              @click.prevent="updateUserButton"
              v-if="!casAuth"
            >
              Valider
            </button>
          </div>
        </form>
      </div>
      <div v-if="!casAuth" class="row mt-3">
        <form ref="invitationForm" class="form needs-validation">
          <div class="input-group mb-3">
            <span class="input-group-text" id="basic-addon1"
              >Inviter une personne</span
            >
            <input
              v-model="inviteInput"
              type="email"
              class="form-control"
              placeholder="email@exemple.com"
              aria-label="email"
              aria-describedby="basic-addon1"
            />
            <button
              @click.prevent="sendInvitation"
              class="btn btn-info"
              type="button"
              id="button-addon2"
            >
              Envoyer invitation
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, inject, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();
const { authUser } = storeToRefs(authStore);
const { updateUser } = authStore;

const showModal = inject("show");

const casAuth = import.meta.env.VITE_APP_CAS_AUTH == "true";

const tempValue = reactive({ first_name: "testsss", last_name: "", email: "" });

onBeforeMount(() => {
  tempValue.first_name = authUser.value.first_name;
  tempValue.last_name = authUser.value.last_name;
  tempValue.email = authUser.value.email;
});

const errors = reactive({
  email: [],
  first_name: [],
  last_name: [],
  non_field_errors: [],
});
function resetErrors() {
  errors.email = [];
  errors.first_name = [];
  errors.last_name = [];
  errors.non_field_errors = [];
}

async function updateUserButton() {
  try {
    resetErrors();
    await updateUser(tempValue);
    showModal({ content: "Profile mis à jour" });
  } catch (error) {
    if (error.response.status == 400) {
      for (const prop in error.response.data) {
        errors[prop] = error.response.data[prop];
      }
    }
  }
}

const inviteInput = ref("");
const invitationForm = ref();

async function sendInvitation() {
  if (invitationForm.value.checkValidity()) {
    try {
      await authStore.inviteUser(inviteInput.value);
      showModal({ content: "Invitation envoyée." });
    } catch (error) {
      console.log(error);
    }
  } else {
    invitationForm.value.reportValidity();
  }
}
</script>

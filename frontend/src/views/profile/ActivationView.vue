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
        <div v-if="isResend">
          <div v-if="!isSent" class="text-center d-flex flex-column">
            <span class="text-center fs-3"
              >Pour renvoyer le mail d'activation veuillez rentrer votre adresse
              email</span
            >
            <form ref="femail">
              <div class="input-group mb-3">
                <input
                  type="email"
                  v-model="email"
                  required
                  class="form-control"
                  placeholder="Votre email"
                  aria-label="Votre email"
                  aria-describedby="button-addon2"
                />
                <button
                  class="btn btn-primary"
                  type="button"
                  id="button-addon2"
                  @click="resend"
                >
                  Renvoyer lien
                </button>
              </div>
            </form>
          </div>
          <div v-else class="text-center d-flex flex-column">
            <span class="text-center fs-1"
              >Si votre adresse email correspond à un compte un mail vient
              d'être envoyer.</span
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
const isResend = ref(false);
const isSent = ref(false);
const email = ref(null);
const femail = ref(null);

let infos = {};

async function resend() {
  if (femail.value.checkValidity()) {
    try {
      await store.resendActivate({ email: email.value });
    } catch (error) {
      if (error.response.status != 400) console.log(error);
    }
    isSent.value = true;
  } else {
    femail.value.reportValidity();
  }
}

onMounted(async () => {
  infos.uid = route.params["uid"];
  infos.token = route.params["token"];
  if (infos.uid && infos.token) {
    try {
      await store.activateUser(infos);
      router.push({ name: "login" });
    } catch (error) {
      failed.value = true;
      console.log(error);
    }
  } else isResend.value = true;
});
</script>

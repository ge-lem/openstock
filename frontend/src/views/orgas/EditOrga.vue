<template>
  <div class="card" v-if="isLoaded">
    <div class="card-header">
      <h3 class="float-start">
        {{ isNew ? "Nouvelle organisation" : orga.name }}
      </h3>
      <button
        v-if="!isNew && isOwner"
        @click.prevent="destroy"
        class="btn btn-danger float-end"
        type="button"
      >
        Supprimer
      </button>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col">
          <form ref="editForm" class="form needs-validation">
            <div class="mb-3">
              <label class="form-label">Nom</label
              ><input
                v-model="orga.name"
                class="form-control"
                type="text"
                required
                :class="{ 'is-invalid': errors.name.length }"
              />
              <div
                v-for="error in errors.name"
                :key="error"
                class="invalid-feedback"
              >
                {{ error }}
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Contact</label
              ><input
                v-model="orga.contact"
                class="form-control"
                type="email"
                required
                :class="{ 'is-invalid': errors.contact.length }"
              />
              <div
                v-for="error in errors.contact"
                :key="error"
                class="invalid-feedback"
              >
                {{ error }}
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Propriétaire</label
              ><input
                :value="ownerName"
                class="form-control"
                type="text"
                readonly
              />
            </div>
            <div>
              <label class="form-label">Manageurs</label
              ><UserDynList v-model="orga.managers">
              </UserDynList>
            </div>
          </form>
        </div>
        <div class="col">
          <h5>Description</h5>
          <textarea
            v-model="orga.description"
            rows="5"
            class="col-12"
          ></textarea>
          <a href="#" @click.prevent="showHelp = true">Aide</a>
          <h5>Aperçu</h5>
          <markdown
            v-model:showHelp="showHelp"
            :description="orga.description"
          />
        </div>
      </div>
      <div class="row mt-3">
        <div class="col">
          <button
            v-if="isNew"
            @click.prevent="create"
            class="btn btn-primary"
            type="button"
          >
            Ajouter
          </button>
          <button
            v-else
            @click.prevent="update"
            class="btn btn-primary"
            type="button"
          >
            Modifier
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, inject, computed, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useOrgaStore } from "@/stores/orgas";
import { useRouter, useRoute } from "vue-router";
import UserDynList from "@/components/ui/UserDynList.vue";
import Markdown from "@/components/ui/MarkdownComponent.vue";

const showConfirm = inject("confirm");

const isLoaded = ref(false);
const showHelp = ref(false);

const authStore = useAuthStore();
const { authUser } = storeToRefs(authStore);
const { getUser } = authStore;

const orgaStore = useOrgaStore();
const { getOrga, updateOrga, deleteOrga, createOrga } = orgaStore;

const route = useRoute();
const router = useRouter();
const isNew = computed(() => route.params["orgaid"] == "new");

const editForm = ref();
const ownerName = ref("");

const orga = ref({
  name: "",
  description: "",
  managers: [],
  contact: "",
  isIndividual: false,
  owner: authUser.id,
});

const isOwner = computed(() => orga.value.owner == authUser.value.id);

const errors = reactive({
  name: [],
  contact: [],
  non_field_errors: [],
});

function resetErrors() {
  errors.name = [];
  errors.contact = [];
  errors.non_field_errors = [];
}

async function update() {
  resetErrors();
  if (editForm.value.checkValidity()) {
    try {
      await updateOrga(orga.value);
      router.push({ name: "myorgas" });
    } catch (error) {
      if (error.response.status == 400) {
        for (const prop in error.response.data) {
          errors[prop] = error.response.data[prop];
        }
      }
    }
  } else {
    editForm.value.reportValidity();
  }
}

async function create() {
  resetErrors();
  if (editForm.value.checkValidity()) {
    try {
      await createOrga(orga.value);
      router.push({ name: "myorgas" });
    } catch (error) {
      if (error.response.status == 400) {
        for (const prop in error.response.data) {
          errors[prop] = error.response.data[prop];
        }
      }
    }
  } else {
    editForm.value.reportValidity();
  }
}

async function destroy() {
  const isConfirmed = await showConfirm({
    content: "Voulez vous vraiment supprimer cette organisation ?",
  });
  if (isConfirmed) {
    try {
      await deleteOrga(orga.value);
    } finally {
      router.push({ name: "myorgas" });
    }
  }
}

onBeforeMount(async () => {
  if (!isNew.value) {
    try {
      orga.value = await getOrga(route.params["orgaid"]);
      if (orga.value.isIndividual) router.push({ name: "myorgas" });
    } catch (error) {
      router.push({ name: "myorgas" });
    }
  } else {
    orga.value.owner = authUser.value.id;
    orga.value.contact = authUser.value.email;
  }
  let owner = null;
  if (orga.value.owner == authUser.value.id) {
    owner = authUser.value;
  } else {
    owner = await getUser(orga.value.owner);
  }
  ownerName.value =
    "@" +
    owner.username +
    " " +
    (owner.first_name ? owner.first_name : "") +
    " " +
    (owner.last_name ? owner.last_name : "");
  isLoaded.value = true;
});
</script>

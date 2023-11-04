<template>
  <div class="card">
    <div class="card-header">
      <h3 class="float-start">Mes organisations</h3>

      <div class="btn-group float-end">
        <button
          class="btn btn-outline-primary"
          @click.prevent="() => (showHelp = true)"
        >
          Ⓘ
        </button>
        <router-link
          class="btn btn-primary"
          :to="{ name: 'editorga', params: { orgaid: 'new' } }"
          >Nouvelle Organisation</router-link
        >
      </div>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col">
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Nom</th>
                  <th>Contact</th>
                  <th class="col-1">Modifier</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="orga in orgas" :key="orga.id">
                  <td>{{ orga.isIndividual ? "Individuelle" : orga.name }}</td>
                  <td>{{ orga.contact }}</td>
                  <td>
                    <router-link
                      v-if="!orga.isIndividual"
                      class="btn btn-primary"
                      :to="{ name: 'editorga', params: { orgaid: orga.id } }"
                    >
                      <svg class="svg-icon-small">
                        <use href="#edit" />
                      </svg>
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <modal
      id="help orga"
      :show="showHelp"
      title="Aide Organisations"
      :resolve="() => (showHelp = false)"
    >
      <div class="row">
        <p>
          Une annonce est forcément reliée à une organisation. Toute personne
          possède au moins une organisation qui lui est propre dont il est le
          seul gestionnaire.
        </p>
        <p>
          Cependant une personne peut également créer une organisation auquelle
          elle peut ajouter des gestionnaires. Les gestionnaires ont les mêmes
          droits que le propriétaire excepté celui de supprimer l'organisation.
        </p>
      </div>
    </modal>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import Modal from "@/plugins/modal";
import { useAuthStore } from "@/stores/auth";
import { useOrgaStore } from "@/stores/orgas";
const { authUser } = storeToRefs(useAuthStore());
const orgaStore = useOrgaStore();
const { fetchOrgas } = orgaStore;

const showHelp = ref(false);

const orgas = ref([]);
onBeforeMount(async () => {
  orgas.value = (await fetchOrgas({ userid: authUser.value.id })).sort(
    (a, b) => {
      if (a.isIndividual) return -1;
      else if (
        a.owner == authUser.value &&
        !b.isIndividual &&
        b.owner != authUser.value
      )
        return -1;
      else if (
        b.owner == authUser.value &&
        !a.isIndividual &&
        a.owner != authUser.value
      )
        return 1;
      else return 0;
    }
  );
});
</script>

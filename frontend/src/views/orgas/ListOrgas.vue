<template>
  <div class="row" v-if="!loading">
    <div class="col">
      <div class="card">
        <div class="card-header">
          <h3 class="float-start">Organisations</h3>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col">
              <ul id="searchlist" class="list-group">
                <router-link
                  v-for="o in orgas"
                  :key="o.id"
                  custom
                  v-slot="{ href, navigate }"
                  :to="{ name: 'showorga', params: { orgaid: o.id } }"
                >
                  <li class="list-group-item" role="button" @click="navigate">
                    <div class="row">
                      <div class="col">
                        <div class="d-flex justify-content-between">
                          <h4>
                            <a class="text-decoration-none" :href="href">
                            {{ o.name}}</a
                            >
                          </h4>
                        </div>
                        <p>Contact : <a :href="'mailto:' + o.contact">Envoyer Email</a></p>
                      </div>
                    </div>
                  </li>
                </router-link>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeMount, ref, computed } from "vue";
import { storeToRefs } from "pinia";
import useDebouncedRef from "@/helpers/useDebouncedRef";

import { useOrgaStore } from "@/stores/orgas";

const orgaStore = useOrgaStore();
const { fetchOrgas } = orgaStore;
const { orgas } = storeToRefs(orgaStore);

const loading = ref(true);

onBeforeMount(async () => {
  await fetchOrgas({indiv:false})
  loading.value = false;
});
</script>

<template>
  <div v-if="!loading" class="card">
    <div class="card-header">
      <h3>{{ orga.name }}</h3>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col">
          <div class="table-responsive">
            <table class="table">
              <tbody>
                <tr>
                  <td scope="row">Contact</td>
                  <td><a :href="'mailto:' + orga.contact">Envoyer Email</a></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div>
            <h5>Description</h5>
          </div>
          <markdown :description="desc" />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { useOrgaStore } from "@/stores/orgas";
import { useRouter, useRoute } from "vue-router";
import Markdown from "@/components/ui/MarkdownComponent.vue";

const loading = ref(true);
const orga = ref(null);

const route = useRoute();
const router = useRouter();
const orgaStore = useOrgaStore();
const { getOrga } = orgaStore;

const desc = computed(() => {
  if (orga.value.isIndividual)
    return "Organisation individuelle de " + orga.value.name;
  else return orga.value.description;
});

onBeforeMount(async () => {
  try {
    orga.value = await getOrga(route.params["orgaid"]);
    loading.value = false;
  } catch (error) {
    router.push({ name: "home" });
  }
});
</script>

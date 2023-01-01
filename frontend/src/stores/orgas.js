import { ref } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/helpers/api.service";

export const useOrgaStore = defineStore("orgas", () => {
  const orgas = ref([]);
  const totalCount = ref([]);

  async function fetchOrgas(params) {
    const { data } = await ApiService.query("orgas", params);
    orgas.value = data.results;
    totalCount.value = data.count;
    return orgas.value;
  }
  async function getOrga(id) {
    const { data } = await ApiService.get("orgas", id);
    return data;
  }
  async function createOrga(orga) {
    const { data } = await ApiService.post("orgas", orga);
    return data;
  }
  async function updateOrga(orga) {
    const { data } = await ApiService.update("orgas", orga.id, orga);
    return data;
  }
  async function deleteOrga(orga) {
    const { data } = await ApiService.delete("orgas", orga.id);
    return data;
  }

  return {
    orgas,
    totalCount,
    fetchOrgas,
    getOrga,
    createOrga,
    updateOrga,
    deleteOrga,
  };
});

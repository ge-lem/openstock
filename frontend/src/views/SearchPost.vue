<template>
  <div class="row" v-if="!loading">
    <div class="col col-md-3">
      <div class="card">
        <div class="card-header">
          <h4>Filtres</h4>
        </div>
        <div class="card-body">
          <form>
            <div class="mb-3">
              <label class="form-label">Recherche</label
              ><input v-model="searchInput" class="form-control" type="text" />
            </div>
            <div class="mb-3">
              <label class="form-label">Tags</label>
              <Multiselect
                v-model="tagsInput"
                mode="tags"
                :close-on-select="false"
                :searchable="true"
                :options="tags"
              />
            </div>
            <div class="mb-3">
              <label class="form-label">Organisations</label>
              <Multiselect
                v-model="orga"
                :searchable="true"
                label="name"
                valueProp="id"
                :options="orgasList"
                :limit="3"
                :minChars="3"
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="select-type"
                >Type d'annonces</label
              >
              <select v-model="typePost" id="select-type" class="form-select">
                <option value="b">Les deux</option>
                <option value="s">Propositions</option>
                <option value="r">Requêtes</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label" for="select-date">Trie par dates</label>
              <select v-model="dateOrder" id="select-date" class="form-select">
                <option value="e">Date expiration</option>
                <option value="c">Date création</option>
              </select>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <div class="card-header">
          <h3 class="float-start">Annonces</h3>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col">
              <ul class="list-group">
                <li v-for="p in posts" :key="p.id" class="list-group-item">
                  <div class="row">
                    <div class="col col-3">
                      <router-link
                        v-if="p.thumbnail"
                        :to="{ name: 'showpost', params: { postid: p.id } }"
                      >
                        <img
                          :src="'/media/' + p.thumbnail"
                          class="img-thumbnail img-fluid"
                          alt="thumbnail"
                        />
                      </router-link>
                    </div>
                    <div class="col">
                      <div class="d-flex justify-content-between">
                        <h4>
                          {{ p.is_request ? "Requête: " : "" }}{{ p.title }}
                        </h4>

                        <div class="ms-1">
                          <router-link
                            class="btn btn-primary"
                            :to="{ name: 'showpost', params: { postid: p.id } }"
                          >
                            Consuler
                          </router-link>
                        </div>
                      </div>
                      <markdown :description="p.abstract" :limit="3" />
                      <p>
                        <router-link
                          :to="{
                            name: 'showorga',
                            params: { orgaid: p.owner },
                          }"
                        >
                          {{ orgas[p.owner].name }}
                        </router-link>
                      </p>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col d-xl-flex justify-content-xl-center">
              <pagination
                :total="totalCount"
                :per-page="perPage"
                :current-page="currentPage"
                @pagechanged="onPageChange"
              />
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
import { usePostStore } from "@/stores/posts";

import useSearchStorage from "@/helpers/useSearchStorage";

import Multiselect from "@vueform/multiselect";
import Pagination from "@/components/ui/ListPagination.vue";
import Markdown from "@/components/ui/MarkdownComponent.vue";

const orgaStore = useOrgaStore();
const { fetchOrgas } = orgaStore;

const postStore = usePostStore();
const { posts, totalCount } = storeToRefs(postStore);
const { searchPosts } = postStore;

const loading = ref(true);

const orga = ref("");
const dateOrder = ref("e");
const typePost = ref("b");
const tagsInput = ref([]);
const tags = ref([]);
const searchInput = useDebouncedRef("");

const currentPage = ref(1);
const perPage = computed(() => {
  return parseInt(import.meta.env.VITE_APP_MAXLIST);
});

function onPageChange(page) {
  currentPage.value = page;
  refresh();
}

async function refresh() {
  let paramsDefault = {};
  paramsDefault["order"] = dateOrder.value;
  paramsDefault["type"] = typePost.value;

  if (searchInput.value) {
    paramsDefault["search"] = searchInput.value;
  }
  if (orga.value) {
    paramsDefault["orga"] = orga.value;
  }
  if (dateOrder.value) {
    paramsDefault["order"] = dateOrder.value;
  }
  if (tagsInput.value.length > 0) {
    paramsDefault["tags"] = tagsInput.value.join();
  }

  paramsDefault.limit = perPage.value;
  paramsDefault.offset = (currentPage.value - 1) * perPage.value;
  await searchPosts({ ...paramsDefault });
}

useSearchStorage(
  "search",
  refresh,
  { orga, searchInput, tagsInput, dateOrder, typePost },
  currentPage
);

const orgas = ref({});
const orgasList = ref([]);

onBeforeMount(async () => {
  tags.value = await postStore.fetchTags();
  orgasList.value = (await fetchOrgas()).sort((a, b) => {
    if (a.isIndividual && !b.isIndividual) return 1;
    else if (!a.isIndividual && b.isIndividual) return -1;
    else return 0;
  });
  orgas.value = Object.assign(
    {},
    ...orgasList.value.map((x) => {
      return { [x.id]: x };
    })
  );
  await refresh();
  loading.value = false;
});
</script>
<style src="@vueform/multiselect/themes/default.css"></style>

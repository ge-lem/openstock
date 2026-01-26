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
            <div v-if="isAuthenticated" class="mb-3">
              <label class="form-label">Organisations</label>
              <Multiselect
                v-model="orga"
                :searchable="true"
                label="name"
                valueProp="id"
                :options="orgas"
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
		  <button class="float-end" v-on:click="downloadCSV(posts)">Exporter en CSV</button>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col">
              <ul id="searchlist" class="list-group">
                <router-link
                  v-for="p in posts"
                  :key="p.id"
                  custom
                  v-slot="{ href, navigate }"
                  :to="{ name: 'showpost', params: { postid: p.id } }"
                >
                  <li class="list-group-item" role="button" @click="navigate">
                    <div class="row">
                      <div class="col col-3">
                        <img
                          v-if="p.thumbnail"
                          :src="'/media/' + p.thumbnail"
                          class="img-thumbnail img-fluid"
                          alt="thumbnail"
                        />
                      </div>
                      <div class="col">
                        <div class="d-flex justify-content-between">
                          <h4>
                            <a class="text-decoration-none" :href="href">
                              {{ p.is_request ? "Requête: " : ""
                              }}{{ p.title }} {{ p.status == 2 ? "(Brouillon privé à l'organisation)" : ""}}</a
                            >
                          </h4>
                        </div>
                        <p>{{ p.abstract }}</p>
                        <p v-if="isAuthenticated" >Organisation : {{ orgasDict[p.owner].name }}</p>
                      </div>
                    </div>
                  </li>
                </router-link>
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
import { onBeforeMount, ref, computed, isProxy, toRaw } from "vue";
import { storeToRefs } from "pinia";
import useDebouncedRef from "@/helpers/useDebouncedRef";

import { useAuthStore } from "@/stores/auth";
import { useOrgaStore } from "@/stores/orgas";
import { usePostStore } from "@/stores/posts";

import useSearchStorage from "@/helpers/useSearchStorage";

import Multiselect from "@vueform/multiselect";
import Pagination from "@/components/ui/ListPagination.vue";
import ApiService from "@/helpers/api.service";

const store = useAuthStore();
const { isAuthenticated } = storeToRefs(store);

const orgaStore = useOrgaStore();
const { orgas, orgasDict } = storeToRefs(orgaStore);
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

function createSearchParams(pagination) {
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

	if (pagination) {
	  paramsDefault.limit = perPage.value;
	  paramsDefault.offset = (currentPage.value - 1) * perPage.value;
	}
	return { ...paramsDefault };
}

async function refresh() {
  await searchPosts(createSearchParams(true));
}

useSearchStorage(
  "search",
  refresh,
  { orga, searchInput, tagsInput, dateOrder, typePost },
  currentPage,
);

onBeforeMount(async () => {
  tags.value = await postStore.fetchTags();
  if(isAuthenticated.value)
  {
    await fetchOrgas()
  }
  await refresh();
  loading.value = false;
});

function escape(text) {
	if (text) {
		return text.replace("\"", "\\\"");
	}
	return "";
}

async function downloadCSV() {
	const { data } = await ApiService.query("posts", createSearchParams(false));
	let array = data.results;
	var csv = "title,owner,abstract,description,quantity,create_date,expire_date,tags\r\n";
	for (var i = 0; i < array.length; i++) {
		var post = array[i];
		csv += '"' + escape(post.title) + "\",";
		csv += '"' + escape(orgas.value.find(e => e.id === post.owner).name) + "\",";
		csv += '"' + escape(post.abstract) + "\",";
		csv += '"' + escape(post.description) + "\",";
		csv += '"' + (post.quantity ? post.quantity : "") + "\",";
		csv += '"' + escape(post.create_date) + "\",";
		csv += '"' + escape(post.expire_date) + "\",";
		csv += '"';
		for (var j = 0; j < post.tags.length; j++) {
			csv += escape(post.tags[j]);
			csv += ',';
		}
		csv += "\",";
		csv += "\r\n";
	}
	var blob = new Blob([csv], {type: 'text/csv;charset=utf-8'});
	var url = URL.createObjectURL(blob);
	var link = document.createElement("a");
	link.href = url;
	link.setAttribute("download", "export.csv");
	link.click();
}
</script>
<style src="@vueform/multiselect/themes/default.css"></style>

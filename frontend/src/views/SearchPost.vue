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
            <div class="mb-3" v-if="atMyPosts">
              <label class="form-label" for="select-status">Status</label
              ><select
                v-model="statusPost"
                id="select-status"
                class="form-select"
              >
                <option value="">Tous les status</option>
                <option :value="2">Brouillon</option>
                <option :value="3">En cours</option>
                <option :value="4">Fermé</option>
                <option :value="5">Expirée</option>
              </select>
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
          <h3 class="float-start">
            {{ atMyPosts ? "Mes annonces" : "Annonces" }}
          </h3>
          <div class="btn-group float-end">
            <button class="btn btn-primary" @click.prevent="downloadCSV()">
              Exporter
            </button>
            <router-link
              v-if="atMyPosts"
              class="btn btn-primary"
              :to="{ name: 'importposts' }"
              >Importer</router-link
            >
          </div>
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
                  :to="toPost(p)"
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
                              {{ p.is_request ? "Requête: " : "" }}{{ p.title }}
                              <span v-if="atMyPosts"
                                >({{ statusDict[p.status] }})</span
                              >
                            </a>
                          </h4>
                          <router-link
                            v-if="atMyPosts"
                            class="btn btn-primary ms-1"
                            :to="{ name: 'editpost', params: { postid: p.id } }"
                          >
                            <svg class="svg-icon-small">
                              <use href="#edit" />
                            </svg>
                          </router-link>
                        </div>
                        <p>{{ p.abstract }}</p>
                        <p v-if="isAuthenticated">
                          Organisation : {{ orgasDict[p.owner].name }}
                        </p>
                        <ul class="list-group list-group-horizontal mb-3">
                          <li
                            v-for="tag in p.tags"
                            :key="tag"
                            class="list-group-item"
                          >
                            <span>{{ tag }}</span>
                          </li>
                        </ul>
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
import { onBeforeMount, ref, computed } from "vue";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import useDebouncedRef from "@/helpers/useDebouncedRef";

import { useAuthStore } from "@/stores/auth";
import { useOrgaStore } from "@/stores/orgas";
import { usePostStore } from "@/stores/posts";

import useSearchStorage from "@/helpers/useSearchStorage";

import Multiselect from "@vueform/multiselect";
import Pagination from "@/components/ui/ListPagination.vue";

const route = useRoute();
const atMyPosts = computed(() => route.name == "myposts");

const store = useAuthStore();
const { isAuthenticated, authUser } = storeToRefs(store);

const orgaStore = useOrgaStore();
const { orgas, orgasDict } = storeToRefs(orgaStore);
const { fetchOrgas } = orgaStore;

const postStore = usePostStore();
const { posts, totalCount } = storeToRefs(postStore);
const { searchPosts, fetchPosts } = postStore;

const statusDict = ref({
  2: "Brouillon",
  3: "En cours",
  4: "Fermée",
  5: "Expirée",
});

const loading = ref(true);

const orga = ref("");
const dateOrder = ref("e");
const typePost = ref("b");
const statusPost = ref("");
const tagsInput = ref([]);
const tags = ref([]);
const searchInput = useDebouncedRef("");

const currentPage = ref(1);
const perPage = computed(() => {
  return parseInt(import.meta.env.VITE_APP_MAXLIST);
});

function toPost(post) {
  if (atMyPosts.value) return { name: "post", params: { postid: post.id } };
  else {
    let orga = orgasDict.value[post.owner];
    let authIsOwner =
      orga.owner == authUser.value.id ||
      orga.managers.indexOf(authUser.value.id) != -1;
    return {
      name: authIsOwner ? "post" : "showpost",
      params: { postid: post.id },
    };
  }
}

function onPageChange(page) {
  currentPage.value = page;
  refresh();
}

function createSearchParams(pagination) {
  let paramsDefault = {};
  paramsDefault["order"] = dateOrder.value;
  paramsDefault["type"] = typePost.value;

  if (statusPost.value) {
    paramsDefault["status"] = statusPost.value;
  }
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
  if (atMyPosts.value) await fetchPosts(createSearchParams(true));
  else await searchPosts(createSearchParams(true));
}

useSearchStorage(
  "search",
  refresh,
  { orga, searchInput, tagsInput, dateOrder, typePost, statusPost },
  currentPage,
);

onBeforeMount(async () => {
  tags.value = await postStore.fetchTags();
  if (isAuthenticated.value) {
    if (atMyPosts.value) {
      await fetchOrgas({ userid: authUser.value.id });
    } else await fetchOrgas();
  }
  await refresh();
  loading.value = false;
});

async function downloadCSV() {
  const params = createSearchParams(false);
  const { posts } = atMyPosts.value
    ? await fetchPosts(params)
    : await searchPosts(params);
  var csv = "#Params : " + JSON.stringify(params) + "\r\n";
  if (atMyPosts.value)
    csv +=
      "title,owner,status,org_comment,abstract,description,quantity,create_date,expire_date,tags\r\n";
  else
    csv +=
      "title,owner,abstract,description,quantity,create_date,expire_date,tags\r\n";
  for (var i = 0; i < posts.value.length; i++) {
    var post = posts.value[i];
    csv += '"' + escape(post.title) + '",';
    csv += '"' + escape(orgasDict.value[post.owner].name) + '",';
    if (atMyPosts.value) {
      csv += '"' + escape(post.status) + '",';
      csv += '"' + escape(post.org_comment) + '",';
    }
    csv += '"' + escape(post.abstract) + '",';
    csv += '"' + escape(post.description) + '",';
    csv += '"' + (post.quantity ? post.quantity : "") + '",';
    csv += '"' + escape(post.create_date) + '",';
    csv += '"' + escape(post.expire_date) + '",';
    csv += '"';
    for (var j = 0; j < post.tags.length; j++) {
      csv += escape(post.tags[j]);
      csv += ",";
    }
    csv += '",';
    csv += "\r\n";
  }
  var blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  var url = URL.createObjectURL(blob);
  var link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", "export.csv");
  link.click();
}
</script>
<style src="@vueform/multiselect/themes/default.css"></style>

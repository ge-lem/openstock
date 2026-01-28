<template>
  <div v-if="!loading" class="card">
    <div class="card-header">
      <h3>Mes annonces</h3>
    </div>
    <div class="card-body">
      <form class="row row-cols-lg-auto g-3 align-items-center">
        <span>Filtres</span>
        <div class="col-auto">
          <input
            v-model="searchInput"
            class="form-control"
            type="search"
            placeholder="Search"
          />
        </div>
        <div class="col-12">
          <label class="form-label visually-hidden" for="select-orga"
            >Oraganisations</label
          ><select v-model="orga" id="select-orga" class="form-select">
            <option value="" selected>Toutes les orgas</option>
            <option v-for="o in orgas" :key="o.id" :value="o.id">
              {{ o.name }}
            </option>
          </select>
        </div>
        <div class="col-12">
          <label class="form-label visually-hidden" for="select-date"
            >Status</label
          ><select v-model="status" id="select-date-1" class="form-select">
            <option value="">Tous les status</option>
            <option :value="2">Brouillon</option>
            <option :value="3">En cours</option>
            <option :value="4">Fermé</option>
            <option :value="5">Expirée</option>
          </select>
        </div>
        <span>Trie</span>
        <div class="col-12">
          <label class="form-label visually-hidden" for="select-date"
            >Dates</label
          ><select v-model="dateOrder" id="select-date" class="form-select">
            <option value="e">Date expiration</option>
            <option value="c">Date création</option>
          </select>
        </div>
      </form>
      <div class="row">
        <div class="col">
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Titre</th>
                  <th>Organisation</th>
                  <th>Status</th>
                  <th>Expiration</th>
                  <th>Quantité</th>
                  <th class="col-2">Modifier</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="p in posts"
                  :key="p.id"
                  :class="{
                    'table-info': p.status == 3,
                    'table-success': p.status == 2,
                    'table-warning': p.status == 4 || p.status == 5,
                  }"
                >
                  <td>{{ p.is_request ? "Requête: " : "" }}{{ p.title }}</td>
                  <td>{{ orgasDict[p.owner].name }}</td>
                  <td>{{ statusDict[p.status] }}</td>
                  <td>{{ p.expire_date }}</td>
                  <td>{{ p.quantity }}</td>
                  <td>
                    <router-link
                      class="btn btn-primary ms-1"
                      :to="{ name: 'editpost', params: { postid: p.id } }"
                    >
                      <svg class="svg-icon-small">
                        <use href="#edit" />
                      </svg>
                    </router-link>
                    <router-link
                      class="btn btn-primary ms-1"
                      :to="{ name: 'showpost', params: { postid: p.id } }"
                    >
                      <svg class="svg-icon-small">
                        <use href="#eye" />
                      </svg>
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
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
</template>

<script setup>
import { onBeforeMount, ref, computed } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useOrgaStore } from "@/stores/orgas";
import { usePostStore } from "@/stores/posts";
import useSearchStorage from "@/helpers/useSearchStorage";
import useDebouncedRef from "@/helpers/useDebouncedRef";
import Pagination from "@/components/ui/ListPagination.vue";

const { authUser } = storeToRefs(useAuthStore());
const orgaStore = useOrgaStore();
const { orgas, orgasDict } = storeToRefs(orgaStore);
const { fetchOrgas } = orgaStore;

const postStore = usePostStore();
const { posts, totalCount } = storeToRefs(postStore);
const { fetchPosts } = postStore;

const loading = ref(true);
const searchInput = useDebouncedRef("");
const orga = ref("");
const status = ref("");
const dateOrder = ref("e");

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
  paramsDefault["search"] = searchInput.value;
  
  if (orga.value) {
    paramsDefault["orga"] = orga.value;
  }
  if (status.value) {
    paramsDefault["status"] = status.value;
  }

  paramsDefault.limit = perPage.value;
  paramsDefault.offset = (currentPage.value - 1) * perPage.value;
  await fetchPosts({ ...paramsDefault });
}

const statusDict = ref({
  2: "Brouillon",
  3: "En cours",
  4: "Fermée",
  5: "Expirée",
});

useSearchStorage("myposts", refresh, { search: searchInput, orga, status, dateOrder }, currentPage);


onBeforeMount(async () => {
  let listOrgas = await fetchOrgas({ userid: authUser.value.id });
  await refresh();
  loading.value = false;
});
</script>

<template>
  <nav class="navbar navbar-light navbar-expand-md">
    <div class="container-fluid">
      <a class="navbar-brand" href="/"
        ><strong>{{ title }}</strong></a
      >
      <button
        data-toggle="collapse"
        class="navbar-toggler"
        data-target="#navcol-1"
        @click="collapse"
      >
        <span class="sr-only">Toggle navigation</span
        ><span class="navbar-toggler-icon" />
      </button>
      <div id="navcol-1" :class="collapsed">
        <ul v-if="isAuthenticated" class="nav navbar-nav me-auto">
          <li class="nav-item" role="presentation">
            <router-link
              active-class="active"
              class="nav-link"
              exact
              :to="{ name: 'search' }"
            >
              Annonces
            </router-link>
          </li>
          <li v-if="orgas.length == 1" class="nav-item" role="presentation">
            <a class="nav-link" href="#" @click.prevent="newPost()"
              >Ajouter une annonce</a
            >
          </li>
          <div
            v-else
            ref="rootDropdown"
            class="dropdown vav-item"
            @focusout="hideDropdown"
          >
            <a
              href=""
              class="nav-link dropdown-toggle"
              :class="[{ show: show }]"
              @click.prevent="toogleDropdown"
              >Ajouter une annonce</a
            >
            <ul class="dropdown-menu" :class="{ show: show }">
              <li v-for="orga in orgas" :key="orga.id">
                <a
                  href=""
                  class="dropdown-item"
                  @click.prevent="newPost(orga)"
                  >{{ orga.name }}</a
                >
              </li>
            </ul>
          </div>
        </ul>
        <ul v-if="isAuthenticated" class="nav navbar-nav d-flex">
          <Dropdown :items="userroutes" :label="authUser.username" is-nav />

          <li class="nav-item" role="presentation">
            <a class="nav-link" href="#" @click.prevent="logout">Logout </a>
          </li>
        </ul>
        <ul v-else class="nav navbar-nav">
          <li class="nav-item" role="presentation">
            <router-link
              active-class="active"
              class="nav-link"
              exact
              :to="{ name: 'login' }"
            >
              Login
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { onBeforeMount, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import Dropdown from "@/components/ui/RouteDropdown.vue";

const title = import.meta.env.VITE_APP_TITLE;

const userroutes = [
  {
    to: { name: "profile" },
    label: "Profile",
  },
  {
    to: { name: "myposts" },
    label: "Mes annonces",
  },
  {
    to: { name: "myorgas" },
    label: "Mes organisations",
  },
];

const collapsed = ref("collapse navbar-collapse");
function collapse() {
  /*
    Emulate bootstrap collapse menu
  */
  if (collapsed.value == "collapse navbar-collapse") {
    collapsed.value = "navbar-collapse";
  } else {
    collapsed.value = "collapse navbar-collapse";
  }
}

const store = useAuthStore();
const { isAuthenticated, authUser } = storeToRefs(store);

function logout() {
  store.logout();
  orgas.value = [];
  router.push("/");
}

let orgaStore = null;
let postStore = null;
const orgas = ref([]);
const show = ref(false);

const toogleDropdown = function () {
  show.value = !show.value;
};
const rootDropdown = ref(null);
function hideDropdown(e) {
  if (rootDropdown.value && !rootDropdown.value.contains(e.relatedTarget)) {
    show.value = false;
  }
}
const router = useRouter();
async function newPost(orga) {
  if (!orga) {
    orga = orgas.value.find((o) => o.isIndividual);
  }
  const newpost = await postStore.getNewPost({ orga: orga.id });
  show.value = false;
  router.push({ name: "editpost", params: { postid: newpost.id } });
}

async function refreshAuth(){
if (isAuthenticated.value) {
    const orgaImp = await import("@/stores/orgas");
    orgaStore = orgaImp.useOrgaStore();
    const postImp = await import("@/stores/posts");
    postStore = postImp.usePostStore();
    orgas.value = (
      await orgaStore.fetchOrgas({ userid: authUser.value.id })
    ).map((o) => {
      if (o.isIndividual) o.name = "Personnelle";
      return o;
    });
  } else {
    console.log("not imported");
  }
}

watch(isAuthenticated,async ()=>{
    console.log("auth watch");
  refreshAuth();

})

onBeforeMount(async () => {
  refreshAuth();
});
</script>

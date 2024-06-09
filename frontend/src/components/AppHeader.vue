<template>
  <header id="header" class="header" role="banner">
    <div class="section clearfix">
      <div class="os-menu-top navbar bg-white d-none d-lg-block">
        <div class="container-liquid">
          <div class="navbar-nav">
            <a
              href="https://www.exemple.fr"
              title="LA STRUCTURE"
              role="button"
              class="btn-back nav-link"
            >
              <span class="icon icon-fleche-precedent">&lt; </span>
              <span class="btn-label">LA STRUCTURE</span>
            </a>
          </div>
          <div class="navbar-nav">
            <Dropdown
              v-if="isAuthenticated"
              :items="userroutes"
              :label="authUser.username"
              isNav
            >
              <span class="btn-label">{{ authUser.username }}</span>
            </Dropdown>
            <router-link
              v-else
              active-class="active"
              class="btn btn-primary"
              exact
              :to="{ name: 'login' }"
            >
              <svg class="svg-icon">
                <use href="#profile" />
              </svg>
              Login
            </router-link>
          </div>
        </div>
      </div>
      <div
        class="social-side-menu-wrapper position-fixed h-100 d-none d-lg-flex align-items-center"
      ></div>
      <div id="os-theme-branding">
        <div class="container-liquid">
          <div class="row h-100 position-relative">
            <div class="col-6 col-md-5 col-lg-3 main-logo">
              <a href="/" rel="home" class="site-logo">
                <img :src="`${publicPath}brand.svg`" alt="Accueil" />
              </a>
            </div>
            <div class="site-name-wrapper col-6 col-md-7 col-lg-5">
              <p class="site-name">{{ title }}</p>
              <p class="site-slogan w-100"></p>
            </div>
            <div
              class="col-md-2 d-none logo-entity d-lg-flex justify-content-center"
            ></div>
            <div
              class="col-md-2 d-none d-lg-flex header-search-block justify-content-end align-items-center"
            ></div>
          </div>
        </div>
      </div>
      <nav
        id="os-theme-menu-main"
        class="os-theme-main-nav navbar navbar-dark navbar-expand-lg d-none d-lg-block bg-primary"
        role="navigation"
        aria-labelledby="os-theme-menu-main-menu"
      >
        <h2 id="os-theme-menu-main-menu" class="visually-hidden">
          Navigation principale
        </h2>

        <div id="mainMenu" class="container-liquid">
          <div
            id="navbarMainContent"
            class="w-100 d-none d-lg-flex collapse"
            style=""
          >
            <ul class="nav navbar-nav">
              <li v-if="!isAuthenticated" class="nav-item">
                <router-link
                  active-class="active"
                  class="nav-link"
                  exact
                  :to="{ name: 'home' }"
                >
                  {{ title }}
                </router-link>
              </li>

              <template v-else>
                <li v-if="isAuthenticated" class="nav-item" role="presentation">
                  <router-link
                    active-class="active"
                    class="nav-link"
                    exact
                    :to="{ name: 'search' }"
                  >
                    Annonces
                  </router-link>
                </li>
                <li
                  v-if="orgas.length == 1"
                  class="nav-item"
                  role="presentation"
                >
                  <a class="nav-link" href="#" @click.prevent="newPost()"
                    >Ajouter une annonce</a
                  >
                </li>
                <Dropdown v-else :items="orgas" isNav>
                  <span class="btn-label">Ajouter une annonce</span>
                </Dropdown>
              </template>
            </ul>
          </div>
        </div>
      </nav>
      <nav
        class="os-theme-main-nav navbar navbar-dark navbar-expand-lg d-block d-lg-none bg-primary"
        role="navigation"
        aria-labelledby="os-theme-menu-main-mobile-menu"
      >
        <h2 id="os-theme-menu-main-mobile-menu" class="visually-hidden">
          Navigation principale mobile
        </h2>
        <div class="container-liquid">
          <label
            for="navbar-toggle-menu"
            class="navbar-toggler btn btn-primary"
            data-toggle="collapse"
            data-target="#navbarMenu"
            aria-expanded="false"
            aria-controls="navbarMenu"
            :class="{ collapsed: !menuCollapse }"
          >
            <svg class="svg-icon">
              <use href="#burger" />
            </svg>
            <span class="btn-label"> Menu </span>
            </label>
            <router-link
            v-if="!isAuthenticated"
              active-class="active"
              class="navbar-toggler collapsed btn btn-primary"
              exact
              :to="{ name: 'login' }"
            >
            <svg class="svg-icon">
              <use href="#profile" />
            </svg>
            <span class="btn-label">Login</span></router-link
          >
          <label
            v-if="isAuthenticated"
            for="navbar-toggle-profile"
            class="navbar-toggler btn btn-primary"
            data-toggle="collapse"
            data-target="#navbarProfile"
            aria-expanded="false"
            aria-controls="navbarProfile"
            :class="{ collapsed: !profileCollapse }"
          >
            <svg class="svg-icon">
              <use href="#profile" />
            </svg>
            <span class="btn-label">Menu utilisateur</span>
          </label>
        </div>
        <input
          id="navbar-toggle-menu"
          v-model="menuCollapse"
          type="checkbox"
          class="navbar-toggler-input"
        />
        <div
          id="navbarMainContent"
          class="navbar-collapse collapse ps-4"
          data-bs-parent="#mobileCollapseGroup"
          :class="{ show: menuCollapse }"
        >
          <ul class="nav navbar-nav">
            <template v-if="!isAuthenticated">
            <li class="nav-item">
              <router-link
                active-class="active"
                class="nav-link"
                exact
                :to="{ name: 'home' }"
              >
                {{ title }}
              </router-link>
            </li>
            </template>
            <template v-else>
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
            <Dropdown
              v-else
              :items="orgas"
              class="dropdown show active"
              is-nav
              is-black
              :absolute="false"
            >
              <span class="btn-label">Ajouter une annonce</span>
            </Dropdown>
            </template>
          </ul>
        </div>

        <input
          id="navbar-toggle-profile"
          v-model="profileCollapse"
          type="checkbox"
          class="navbar-toggler-input"
        />
        <div
          id="navbarProfileContent"
          class="collapse navbar-collapse"
          :class="{ show: profileCollapse }"
        >
          <ul class="nav navbar-nav ps-4">
            <li v-for="route in userroutes" :key="route.to" class="nav-item">
              <router-link
                v-if="route.to"
                active-class="active"
                class="nav-link"
                exact
                :to="route.to"
              >
                {{ route.label }}
              </router-link>
              <a v-else href="" class="nav-link" @click.prevent="route.click()">
                {{ route.label }}
              </a>
            </li>
          </ul>
        </div>
      </nav>
    </div>
    <svg style="display: none" version="2.0">
      <defs>
        <symbol id="burger" viewBox="0 0 20 20">
          <path
            fill="currentColor"
            d="M3.314,4.8h13.372c0.41,0,0.743-0.333,0.743-0.743c0-0.41-0.333-0.743-0.743-0.743H3.314
								c-0.41,0-0.743,0.333-0.743,0.743C2.571,4.467,2.904,4.8,3.314,4.8z M16.686,15.2H3.314c-0.41,0-0.743,0.333-0.743,0.743
								s0.333,0.743,0.743,0.743h13.372c0.41,0,0.743-0.333,0.743-0.743S17.096,15.2,16.686,15.2z M16.686,9.257H3.314
								c-0.41,0-0.743,0.333-0.743,0.743s0.333,0.743,0.743,0.743h13.372c0.41,0,0.743-0.333,0.743-0.743S17.096,9.257,16.686,9.257z"
          ></path>
        </symbol>
        <symbol id="profile" viewBox="0 0 20 20">
          <path
            fill="currentColor"
            d="M12.075,10.812c1.358-0.853,2.242-2.507,2.242-4.037c0-2.181-1.795-4.618-4.198-4.618S5.921,4.594,5.921,6.775c0,1.53,0.884,3.185,2.242,4.037c-3.222,0.865-5.6,3.807-5.6,7.298c0,0.23,0.189,0.42,0.42,0.42h14.273c0.23,0,0.42-0.189,0.42-0.42C17.676,14.619,15.297,11.677,12.075,10.812 M6.761,6.775c0-2.162,1.773-3.778,3.358-3.778s3.359,1.616,3.359,3.778c0,2.162-1.774,3.778-3.359,3.778S6.761,8.937,6.761,6.775 M3.415,17.69c0.218-3.51,3.142-6.297,6.704-6.297c3.562,0,6.486,2.787,6.705,6.297H3.415z"
          />
        </symbol>
      </defs>
    </svg>
  </header>
</template>

<script setup>
import { onBeforeMount, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import Dropdown from "@/components/ui/RouteDropdown.vue";

const title = import.meta.env.VITE_APP_TITLE;
const publicPath = import.meta.env.BASE_URL;

const userroutes = [
  {
    to: { name: "profile" },
    label: "Profil",
  },
  {
    to: { name: "myposts" },
    label: "Mes annonces",
  },
  {
    to: { name: "myorgas" },
    label: "Mes organisations",
  },
  {
    click: () => {
      logout();
    },
    label: "Déconnection",
  },
];

const menuCollapse = ref(false);
const profileCollapse = ref(false);

const store = useAuthStore();
const { isAuthenticated, authUser } = storeToRefs(store);

function logout() {
  console.log("LOGOUT");
  store.logout();
  orgas.value = [];
  router.push("/");
}

let orgaStore = null;
let postStore = null;
const orgas = ref([]);

const router = useRouter();
async function newPost(orga) {
  if (!orga) {
    orga = orgas.value.find((o) => o.isIndividual);
  }
  const newpost = await postStore.getNewPost({ orga: orga.id });
  router.push({ name: "editpost", params: { postid: newpost.id } });
}

async function refreshAuth() {
  function callNew(v) {
    newPost(v);
  }
  if (isAuthenticated.value) {
    const orgaImp = await import("@/stores/orgas");
    orgaStore = orgaImp.useOrgaStore();
    const postImp = await import("@/stores/posts");
    postStore = postImp.usePostStore();

    orgas.value = (
      await orgaStore.fetchOrgas({ userid: authUser.value.id })
    ).map((o) => {
      if (o.isIndividual) o.label = "Personnelle";
      else o.label = o.name;
      o.click = () => {
        callNew(o);
      };
      return o;
    });
  } else {
    console.log("not imported");
  }
}

watch(isAuthenticated, async () => {
  console.log("auth watch");
  refreshAuth();
});

onBeforeMount(async () => {
  refreshAuth();
});
</script>

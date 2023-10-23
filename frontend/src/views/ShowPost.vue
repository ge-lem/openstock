<template>
  <div v-if="!loading" class="card">
    <div class="card-header">
      <h3>{{ post.is_request ? "Requête: " : "" }}{{ post.title }}</h3>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col col-md-3">
          <img
            v-if="post.thumbnail"
            :src="'/media/' + post.thumbnail"
            class="img-thumbnail img-fluid"
            alt="thumbnail"
          />
        </div>
        <div class="col">
          <div class="table-responsive">
            <table class="table">
              <tbody>
                <tr>
                  <td scope="row">Organisation</td>
                  <td>
                    <router-link
                      :to="{
                        name: 'showorga',
                        params: { orgaid: owner.id },
                      }"
                    >
                      {{ owner.name }}
                    </router-link>
                  </td>
                </tr>
                <tr>
                  <td scope="row">Contact</td>
                  <td>
                    <a :href="'mailto:' + owner.contact">Envoyer Email</a>
                  </td>
                </tr>
                <tr v-if="post.expire_date">
                  <td scope="row">Date d'expiration</td>
                  <td>
                    {{ post.expire_date }}
                  </td>
                </tr>
                <tr v-if="post.quantity">
                  <td scope="row">Quantité</td>
                  <td>
                    {{ post.quantity }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <ul class="list-group list-group-horizontal mb-3">
            <li v-for="tag in post.tags" :key="tag" class="list-group-item">
              <span>{{ tag }}</span>
            </li>
          </ul>
          <button
            v-if="post.photos.length != 0"
            class="btn btn-primary mb-3"
            type="button"
            @click="isShowPhotos = true"
          >
            Voir les autres photos
          </button>
          <div>
            <h5>Description</h5>
          </div>
          <p>{{ post.abstract }} </p>
          <markdown :description="post.description" />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <router-link
            v-if="isOwner"
            class="btn btn-primary float-end"
            :to="{ name: 'editpost', params: { postid: post.id } }"
          >
            <svg class="svg-icon">
              <use href="#edit" />
            </svg>
          </router-link>
        </div>
      </div>
    </div>
    <modal
      id="modal-photos"
      :show="isShowPhotos"
      title="Photos"
      :resolve="() => (isShowPhotos = false)"
    >
      <div class="row">
        <img
          v-for="photo in post.photos"
          :key="photo"
          :src="'/media/' + photo"
          class="img col-md-6"
        />
      </div>
    </modal>
  </div>
</template>
<style>
#modal-photos .modal-dialog {
  max-width: 800px;
}
</style>

<script setup>
import { onBeforeMount, ref, computed } from "vue";
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";

import { useAuthStore } from "@/stores/auth";
import { useOrgaStore } from "@/stores/orgas";
import { usePostStore } from "@/stores/posts";

import Markdown from "@/components/ui/MarkdownComponent.vue";
import Modal from "@/plugins/modal";

const { authUser } = storeToRefs(useAuthStore());
const orgaStore = useOrgaStore();

const postStore = usePostStore();

const route = useRoute();

const post = ref(null);
const owner = ref(null);
const loading = ref(true);

const isShowPhotos = ref(false);

const isOwner = computed(() => {
  return (
    owner.value.owner == authUser.value.id ||
    owner.value.managers.indexOf(authUser.value.id) != -1
  );
});

onBeforeMount(async () => {
  try {
    post.value = await postStore.getPost(route.params["postid"]);
    owner.value = await orgaStore.getOrga(post.value.owner);
    loading.value = false;
  } catch (error) {
    console.log(error);
    //router.push({ name: "home" });
  }
});
</script>

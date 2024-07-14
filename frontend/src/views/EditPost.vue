<template>
  <div class="card" v-if="!loading">
    <div class="card-header">
      <h3 class="float-start">
        {{ statusDict[post.status] }} : {{ post.title }}

        <button
          v-if="post.status == 2"
          class="btn btn-outline-primary align-items-center p-0"
          @click.prevent="() => (showHelp = true)"
        >
          <span class="align-top h1"> Ⓘ</span>
        </button>
      </h3>
      <div class="btn-group float-end">
        <button
          @click.prevent="deletePost"
          class="btn btn-danger"
          type="button"
        >
          Supprimer
        </button>
      </div>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col">
          <form ref="editForm">
            <fieldset :disabled="isClosed">
              <div class="btn-group">
                <input
                  id="radio-prop"
                  class="btn-check"
                  type="radio"
                  name="typepost"
                  v-model="post.is_request"
                  :value="false"
                /><label
                  class="form-label btn btn-outline-primary"
                  for="radio-prop"
                  >Proposition</label
                ><input
                  id="radio-req"
                  class="btn-check"
                  type="radio"
                  name="typepost"
                  v-model="post.is_request"
                  :value="true"
                /><label
                  class="form-label btn btn-outline-primary"
                  for="radio-req"
                  >Requête</label
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Titre</label
                ><input
                  class="form-control"
                  type="title"
                  v-model="post.title"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Organisation</label
                ><select v-model="post.owner" class="form-select" required>
                  <option v-for="o in orgas" :value="o.id" :key="o.id">
                    {{ o.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Miniature</label>
                <div class="col-3">
                  <img
                    v-if="post.thumbnail"
                    :src="'/media/' + post.thumbnail"
                    class="img-thumbnail img-fluid"
                    alt="thumbnail"
                  />
                </div>
                <div class="input-group">
                  <input
                    id="thumbnail"
                    ref="thumbnail"
                    class="form-control"
                    type="file"
                    @change="changeThumbnail"
                  />
                  <button
                    v-if="thumbProgress == null"
                    class="btn btn-primary"
                    type="button"
                    :disabled="!thumbF"
                    @click="uploadThumbnail"
                  >
                    Upload
                  </button>
                  <button
                    v-else
                    class="btn btn-secondary"
                    type="button"
                    disabled
                  >
                    Chargement {{ thumbProgress }}
                  </button>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Résumé (max 255 caractères)</label>
                <textarea
                  v-model="post.abstract"
                  :disabled="isClosed"
                  rows="3"
                  maxlength="255"
                  class="col-12"
                ></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Expiration</label>
                <div class="input-group mb-3">
                  <input
                    v-model="post.expire_date"
                    class="form-control"
                    type="date"
                  />
                  <button
                    @click.prevent="post.expire_date = null"
                    class="btn btn-outline-secondary"
                    type="button"
                  >
                    X
                  </button>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Quantité (optionelle)</label>
                <div class="input-group mb-3">
                  <input
                    v-model="post.quantity"
                    class="form-control"
                    type="number"
                  />
                  <button
                    @click.prevent="post.quantity = null"
                    class="btn btn-outline-secondary"
                    type="button"
                  >
                    X
                  </button>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Tags</label>
                <Multiselect
                  v-model="post.tags"
                  mode="tags"
                  :close-on-select="false"
                  :searchable="true"
                  :create-option="true"
                  :options="tags"
                  :disabled="isClosed"
                  :onCreate="addTag"
                />
              </div>
              <div class="mb-3">
                <label class="form-label" for="photos">Photos (max 10)</label>
                <div class="input-group">
                  <input
                    id="addphoto"
                    ref="addphotoinput"
                    class="form-control"
                    type="file"
                    @change="changePhoto"
                  />
                  <button
                    v-if="photoProgress == null"
                    class="btn btn-primary"
                    type="button"
                    :disabled="!photoF"
                    @click="uploadPhoto"
                  >
                    Ajouter
                  </button>
                  <button
                    v-else
                    class="btn btn-secondary"
                    type="button"
                    disabled
                  >
                    Chargement {{ photoProgress }}
                  </button>
                </div>
                <table class="table">
                  <thead>
                    <tr>
                      <th scope="col">Photos</th>
                      <th scope="col">Supprimer</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="img in post.photos" :key="img">
                      <td>
                        <img
                          :src="'/media/' + img"
                          class="img-thumbnail img-fluid col-3"
                          :alt="img"
                        />
                      </td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-danger"
                          @click="delPhoto(img)"
                        >
                          X
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </fieldset>
          </form>
        </div>
        <div class="col">
          <h5>Description</h5>
          <textarea
            v-model="post.description"
            :disabled="isClosed"
            rows="5"
            class="col-12"
          ></textarea>
          <a href="#" @click.prevent="showHelpMark = true"
            >Aide au format Markdown</a
          >
          <h5>Aperçu</h5>
          <markdown
            v-model:showHelp="showHelpMark"
            :description="post.description"
          />
        </div>
        <div class="row mt-3">
          <div class="col">
            <div class="btn-group" role="group">
              <button
                @click.prevent="updatePost()"
                class="btn btn-primary"
                type="button"
              >
                Enregistrer
              </button>
              <button
                v-if="isDraft"
                @click.prevent="changeStatus(3)"
                class="btn btn-success"
                type="button"
              >
                Enregistrer et Publier
              </button>
              <button
                v-if="isOpen"
                @click.prevent="changeStatus(4)"
                class="btn btn-danger"
                type="button"
              >
                Clôturer
              </button>
              <button
                v-if="!isDraft"
                @click.prevent="changeStatus(2)"
                class="btn btn-warning"
                type="button"
              >
                En brouillon
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <modal
      id="help orga"
      :show="showHelp"
      title="Aide Organisations"
      :resolve="() => (showHelp = false)"
    >
      <div class="row">
        <p>
          Afin de limiter le poid du site, chaque organisation (individuelle ou
          non) n'a le droit d'avoir qu'une seule annonce à l'état de brouillon.
          Vous devez compléter et publier (ou supprimier) l'annonce brouillon
          afin d'en créer une nouvelle.
        </p>
      </div>
    </modal>
  </div>
</template>
<script setup>
import { onBeforeMount, ref, computed, inject } from "vue";
import { storeToRefs } from "pinia";
import { useRouter, useRoute, onBeforeRouteUpdate } from "vue-router";
import Modal from "@/plugins/modal";

import { useAuthStore } from "@/stores/auth";
import { useOrgaStore } from "@/stores/orgas";
import { usePostStore } from "@/stores/posts";
import Multiselect from "@vueform/multiselect";
import Markdown from "@/components/ui/MarkdownComponent.vue";

const showMessage = inject("show");

const showHelpMark = ref(false);
const showHelp = ref(false);

const { authUser } = storeToRefs(useAuthStore());
const orgaStore = useOrgaStore();
const { fetchOrgas } = orgaStore;
const { orgas } = storeToRefs(orgaStore);

const route = useRoute();
const router = useRouter();

const postStore = usePostStore();
const post = ref(null);
const loading = ref(true);

const isDraft = computed(() => post.value.status == 2);
const isOpen = computed(() => post.value.status == 3);
const isClosed = computed(
  () => post.value.status == 4 || post.value.status == 5,
);

const statusDict = ref({
  2: "Brouillon",
  3: "En cours",
  4: "Fermée",
  5: "Expirée",
});

const tags = ref([]);

function addTag(option,select){
  let newtags =  option.value.toLowerCase().replace(' ',',').split(',');
  tags.value.push(...newtags);
  post.value.tags.push(...newtags);
  return false;
}

const editForm = ref();

function checkImageName(file) {
  if (file) {
    const filename = file.name.toLowerCase();
    if (
      [".png", ".jpg", ".jpeg", ".tiff", ".bmp"].some((char) =>
        filename.endsWith(char),
      )
    )
      return true;
    else {
      showMessage({
        content:
          "Seules les images ('.png', '.jpg', '.jpeg', '.tiff', '.bmp') sont acceptées",
      });
    }
  } else {
    return true;
  }
}

const thumbnail = ref();
const thumbF = ref(null);
const thumbProgress = ref(null);
function thumbOnProgressCB(percent) {
  if (percent == 100) thumbProgress.value = "compression image";
  else thumbProgress.value = percent;
}

function changeThumbnail() {
  if (checkImageName(thumbnail.value.files[0])) {
    thumbF.value = thumbnail.value.files[0];
  }
}
async function uploadThumbnail() {
  if (thumbF.value) {
    try {
      const url = await postStore.updateThumbnail(
        post.value.id,
        thumbF.value,
        thumbOnProgressCB,
      );
      post.value.thumbnail = url;
      thumbnail.value.value = null;
      thumbF.value = null;
      thumbProgress.value = null;
    } catch (error) {
      thumbnail.value.value = null;
      thumbF.value = null;
      thumbProgress.value = null;
      if (error.response && error.response.status == 400) {
        showMessage({
          content: "Le fichier image n'est pas valide",
        });
      }
    }
  }
}

const addphotoinput = ref();
const photoF = ref(null);
const photoProgress = ref(null);
function photoOnProgressCB(percent) {
  if (percent == 100) photoProgress.value = "compression image";
  else photoProgress.value = percent;
}
function changePhoto() {
  if (checkImageName(addphotoinput.value.files[0]))
    photoF.value = addphotoinput.value.files[0];
}
async function uploadPhoto() {
  if (photoF.value) {
    try {
      const url = await postStore.addPhoto(
        post.value.id,
        photoF.value,
        photoOnProgressCB,
      );
      post.value.photos.push(url);
      addphotoinput.value.value = null;
      photoF.value = null;
      photoProgress.value = null;
    } catch (error) {
      addphotoinput.value.value = null;
      photoF.value = null;
      photoProgress.value = null;
      if (error.response && error.response.status == 400) {
        showMessage({
          content: "Le fichier image n'est pas valide",
        });
      }
    }
  }
}

async function delPhoto(url) {
  await postStore.deletePhoto(post.value.id, url);
  let index = post.value.photos.indexOf(url);
  if (index != -1) post.value.photos.splice(index, 1);
}

async function updatePost(show = true) {
  if (editForm.value.checkValidity()) {
    try {
      post.value = await postStore.updatePost(post.value);
      if (show)
        router.push({ name: "showpost", params: { postid: post.value.id } });
    } catch (error) {
      console.log(error);
    }
  } else {
    editForm.value.reportValidity();
  }
}

async function changeStatus(status) {
  post.value.status = status;
  if (status == 3) {
    updatePost();
  } else if (status == 4) {
    updatePost(false);
    router.push({ name: "myposts" });
  } else if (status == 2) {
    updatePost(false);
  }
}

async function deletePost() {
  await postStore.deletePost(post.value);
  router.push({ name: "myposts" });
}

onBeforeMount(async () => {
  fetchOrgas({ userid: authUser.value.id });
  tags.value = await postStore.fetchTags();
  try {
    post.value = await postStore.getPost(route.params["postid"]);
    loading.value = false;
  } catch (error) {
    router.push({ name: "myposts" });
  }
});
onBeforeRouteUpdate(async (to) => {
  try {
    post.value = await postStore.getPost(to.params["postid"]);
  } catch (error) {
    router.push({ name: "myposts" });
  }
});
</script>
<style src="@vueform/multiselect/themes/default.css"></style>

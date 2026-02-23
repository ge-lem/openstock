<template>
  <div class="card" v-if="!loading">
	<div class="card-header">
	   <h3 class="float-start">
	     Importer plusieurs annonces
	   </h3>
	</div>
    <div class="card-body">
      <div class="row">
        <div class="col">
          <form ref="editForm">
			<div class="mb-3">
                <label class="form-label">* Fichier tableur CSV</label>
                <div class="input-group">
                  <input
                    id="csv"
                    class="form-control"
                    type="file"
                    @change="updateCSVFile"
                  />
				</div>
				<div style="overflow:scroll;max-height: 400px;">
				  <table id="csvPreview" class="csvPreview">
				  </table>
                </div>
              </div>
			  <div class="mb-3">
	              <label class="form-label">Ignorer la première ligne</label>
				  <input v-model="csvMapping.skipFirstLine" type="checkbox" class="form-checkbox" required/>
	          </div>
              <div class="mb-3">
                <label class="form-label">* Titre (numéro de colonne)</label>
				<select id="titleColumn" v-model="csvMapping.titleColumn" class="form-select" required>
					<ColumnOptions :allColumns="allColumns" :lines="lines"/>
				</select>
              </div>
              <div class="mb-3">
                <label class="form-label">* Organisation (nom ou numéro de colonne)</label>
				<select id="orgColumn" v-model="csvMapping.organization" class="form-select" required>
                  <option v-for="o in orgas" :value="o" :key="o.id">
                    {{ o.name }}
                  </option>
				  <ColumnOptions :allColumns="allColumns" :lines="lines"/>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Résumé (numéro de colonne)</label>
				<select id="abstractColumn" v-model="csvMapping.abstractColumn" class="form-select">
				  <ColumnOptions :allColumns="allColumns" :lines="lines"/>
				</select>
              </div>
              <div class="mb-3">
                <label class="form-label">Expiration (numéro de colonne ou date)</label>
                <div class="input-group mb-3">
                  <input
				    id="expirationColumn"
                    v-model="post.expire_date"
                    class="form-control"
                    type="date"
                  />
                  <button
                    @click.prevent="post.expire_date = null"
                    class="btn btn-outline-secondary"
                    type="button">
                    X
                  </button>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Quantité (numéro de colonne)</label>
				<select id="quantityColumn" v-model="csvMapping.quantityColumn" class="form-select">
					<ColumnOptions :allColumns="allColumns" :lines="lines"/>
				</select>
              </div>
              <div class="mb-3">
                <label class="form-label">Tags (numéro de colonne)</label>
				<select id="tagsColumn" v-model="csvMapping.tagsColumn" class="form-select">
					<ColumnOptions :allColumns="allColumns" :lines="lines"/>
				</select>
              </div>
          <label>Description (numéro de colonne)</label>
		  <select id="descriptionColumn" v-model="csvMapping.descriptionColumn" class="form-select" @change="updatePostsAndErrors">
			<ColumnOptions :allColumns="allColumns" :lines="lines"/>
		  </select>
		  <label>Commentaire privé à l'organisation (numéro de colonne)</label>
  		  <select id="orgCommentColumn" v-model="csvMapping.orgCommentColumn" class="form-select" @change="updatePostsAndErrors">
  			<ColumnOptions :allColumns="allColumns" :lines="lines"/>
  		  </select>
		</form>
		</div>
        <div class="col">
         <h4>Aperçu: {{Object.values(posts).length}} annonces <a v-if="Object.values(errors).length > 0">dont {{Object.keys(errors).length}} avec des ❌ Erreurs</a></h4>
		 <div style="overflow:scroll;max-height: 1000px;">
		 <div v-for="(error, line) in errors">
 			❌ Erreur ligne {{line}} : {{error}}
 		  </div>
          <div v-for="(post, line) in posts">
			<div class="card-header">
				<h5><i>Ligne {{line}}:</i> <strong>{{post.title ? post.title : "❌ Erreur titre manquant"}}</strong> de {{ post.owner ? orgas.find(o => o.id === post.owner).name : "❌ Organisation manquante" }}</h5>
			</div>
			<p>{{post.abstract}}</p>
			<markdown v-if="post.description" :description="post.description" />
			<p v-if="post.quantity > 0">Quantité: {{post.quantity ? post.quantity : "❌ Erreur quantité invalide"}}</p>
			<p v-if="post.creation_date">Créée le: {{post.creation_date}}</p>
			<p v-if="post.expiration_date">Expire le: {{post.expiration_date}}</p>
			<ul class="list-group list-group-horizontal mb-3">
	            <li v-for="tag in post.tags" :key="tag" class="list-group-item">
	              <span>{{ tag }}</span>
	            </li>
            </ul>
		  </div>
          <PostFooter/>
        </div>
		</div>
        <div class="row mt-3">
          <div class="col">
            <div class="btn-group" role="group">
              <button
			   :disabled="Object.keys(posts).length == 0 || Object.keys(errors).length > 0"
                @click.prevent="updatePost(false)"
                class="btn btn-primary"
                type="button"
              >
                Publier
              </button>
              <button
			   :disabled="Object.keys(posts).length == 0 || Object.keys(errors).length > 0"
                @click.prevent="updatePost(true)"
                class="btn btn-warning"
                type="button"
              >
                Enregistrer en brouillons (privés à l'organisation)
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
    </modal>
  </div>
</template>
<script setup>
import { onBeforeMount, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { useRouter, useRoute, onBeforeRouteUpdate } from "vue-router";
import Modal from "@/plugins/modal";

import { useAuthStore } from "@/stores/auth";
import { useOrgaStore } from "@/stores/orgas";
import { usePostStore } from "@/stores/posts";
import ColumnOptions from "@/components/ColumnOptions.vue";
import PostFooter from "@/views/PostFooter.vue";
import Markdown from "@/components/ui/MarkdownComponent.vue";

import Papa from "papaparse";


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

const tags = ref([]);

const csvMapping = ref({
	skipFirstLine: false,
	titleColumn: NaN,
	organization: null, // column number or organization
	quantityColumn: NaN,
	abstractColumn: NaN,
	expireDate: null, // column number or date or null
	tagsColumn: NaN,
	descriptionColumn: NaN,
	orgCommentColumn: NaN,
});
watch(csvMapping, (before, after) => updatePostsAndErrors(), { deep: true });
const allColumns = ref([]);

async function updatePost(draft) {
//  if (editForm.value.checkValidity()) {
    try {
	  const status = draft === false ? 3 /* Open, En Cours */ : 2;
	  const toSubmit = Object.values(posts.value);
	  toSubmit.forEach(post => post.status = status);
      await postStore.createPosts(toSubmit);
	  router.push({ name: "myposts" });
    } catch (error) {
      console.log(error);
    }
//  } else {
//    editForm.value.reportValidity();
//  }
}

var lines = [];
async function updateCSVFile(change) {
	let file = change.target.files[0];
	if (file) {
        Papa.parse(file, {
            complete: function(results) {
				lines = results.data;
				var totalColumns = 0;
				// count columns and update preview
				var tableContents = "";
				for (var i = 0; i < lines.length; i++) {
					var line = lines[i];
					totalColumns = Math.max(totalColumns, line.length);
					tableContents += "<tr class='csvPreview'>";
					tableContents += "<th class='csvPreview'>";
					tableContents += (i + 1);
					tableContents += "</th>"
					for (var c = 0; c < line.length; c++) {
						tableContents += "<td class='csvPreview'>";
						tableContents += line[c];
						tableContents += "</td>";
					}
					tableContents += "</tr>";
				}
				var headers = "<tr>";
				headers += "<th></th>";
				for (var h = 0; h < totalColumns; h++) {
					headers += "<th class='csvPreview'>";
					headers += h + 1;
					headers += "</th>";
				}
				headers += "</tr>";
                document.getElementById('csvPreview').innerHTML = headers + tableContents;
				allColumns.value = Array.from(Array(totalColumns), (e,i)=>i+1);
				updatePostsAndErrors();
            },
            error: function(error) {
                console.error('Error parsing CSV:', error);
            }
        });
    }
}

const errors = ref({});
const posts = ref({});
async function updatePostsAndErrors() {
	var allErrors = {};
	var allPosts = {};
	for (var l = (csvMapping.value.skipFirstLine ? 1 : 0); l < lines.length; l++) {
		var line = lines[l];
		if (line.length > 1 || line[0].length > 0) {
			var converted = toPost(line, csvMapping.value);
			if (converted.errors) {
				allErrors[l + 1] = converted.errors;
			}
			if (converted.post) {
				allPosts[l + 1] = converted.post;
			}
		}
	}
	errors.value = allErrors;
	posts.value = allPosts;
}
function toPost(line, csvMapping) {
	var post = {};
	var error = "";
	if (csvMapping.titleColumn) {
		post.title = line[csvMapping.titleColumn - 1];
	}
	if (!post.title) {
		error += "Un titre doit être spécifié!\n";
	}
	if (csvMapping.abstractColumn) {
		post.abstract = line[csvMapping.abstractColumn - 1];
	}
	var organization;
	if (!isNaN(csvMapping.organization)) {
		var orgName = line[csvMapping.organization - 1];
		organization = orgas.value.find(o => o.name === orgName);
		if (!organization) {
			error += ("Organisation '" + orgName + "' inconnue.");
		}
	} else if (csvMapping.organization) {
		organization = csvMapping.organization;
	}
	if (organization) {
		post.owner = organization.id;
	}
	if (csvMapping.descriptionColumn) {
		post.description = line[csvMapping.descriptionColumn - 1];
	}
	if (csvMapping.orgCommentColumn) {
		post.org_comment = line[csvMapping.orgCommentColumn - 1] 
	}
	if (csvMapping.creation_date) {
		post.creation_date = csvMapping.creation_date;
	}
	if (csvMapping.expiration_date) {
		post.expiration_date = csvMapping.expiration_date;
	}
	if (csvMapping.quantityColumn && line[csvMapping.quantityColumn - 1]) {
		post.quantity = parseInt(line[csvMapping.quantityColumn - 1]);
		if (!post.quantity) {
			error += "La quantité doit être un nombre\n";
		}
	}
	post.tags = [];
	if (csvMapping.tagsColumn && line[csvMapping.tagsColumn - 1]) {
		post.tags = line[csvMapping.tagsColumn - 1].split(',');
	}
	return { post: post, errors: error};
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

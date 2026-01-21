import { ref } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/helpers/api.service";

export const usePostStore = defineStore("posts", () => {
  const posts = ref([]);
  const post = ref({});
  const totalCount = ref(0);

  async function fetchPosts(params) {
    const { data } = await ApiService.query("posts", params);
    posts.value = data.results;
    totalCount.value = data.count;
    return posts.value;
  }
  async function searchPosts(params) {
    const { data } = await ApiService.query("posts/search", params);
    posts.value = data.results;
    totalCount.value = data.count;
    return { posts, totalCount };
  }
  async function showPost(id) {
    let localpost =
      post.value.id == id ? post.value : posts.value.find((p) => p.id == id);
    if (localpost) {
      return localpost;
    } else {
      const { data } = await ApiService.get("posts/search", id);
      return data;
    }
  }
  async function getPost(id) {
    let localpost =
      post.value.id == id ? post.value : posts.value.find((p) => p.id == id);
    if (localpost) {
      return localpost;
    } else {
      const { data } = await ApiService.get("posts", id);
      return data;
    }
  }
  async function getNewPost(param) {
    const { data } = await ApiService.query("posts/get_new", param);
    return data;
  }
  async function updatePost(post) {
    const { data } = await ApiService.update("posts", post.id, post);
    post.value = data;
    return data;
  }
  async function deletePost(post) {
    const { data } = await ApiService.delete("posts", post.id);
    return data;
  }
  async function updateThumbnail(postid, file, onProgressCB) {
    const { data } = await ApiService.postFile(
      "posts/" + postid + "/update_thumbnail",
      file,
      onProgressCB,
    );
    return data.url;
  }
  async function addPhoto(postid, file, onProgressCB) {
    const { data } = await ApiService.postFile(
      "posts/" + postid + "/add_photo",
      file,
      onProgressCB,
    );
    return data.url;
  }
  async function deletePhoto(postid, url) {
    await ApiService.post("posts/" + postid + "/delete_photo", { url });
    return url;
  }
  async function fetchTags() {
    const { data } = await ApiService.get("posts/search/tags");
    return data;
  }
  return {
    posts,
    totalCount,
    fetchPosts,
    searchPosts,
    getPost,
    getNewPost,
    showPost,
    updatePost,
    deletePost,
    updateThumbnail,
    addPhoto,
    deletePhoto,
    fetchTags,
  };
});

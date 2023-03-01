import axios from "axios";

/*
Définition de l'ApiService
*/
const ApiService = {
  init() {
    axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL;
    //axios.defaults.withCredentials = true;
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.xsrfCookieName = "csrftoken";
  },

  setToken(token) {
    if (token)
      axios.defaults.headers.common["Authorization"] = "Token " + token;
    else delete axios.defaults.headers.common["Authorization"];
  },

  async query(resource, params) {
    return axios.get(resource + "/", { params });
  },

  async get(resource, slug = "") {
    return axios.get(resource + "/" + (slug == "" ? "" : slug + "/"));
  },

  async post(resource, params) {
    return axios.post(resource + "/", params);
  },
  async postFile(resource, file) {
    const formData = new FormData();
    formData.append("file", file);
    const headers = { "Content-Type": "multipart/form-data" };
    return axios.post(resource + "/", formData, { headers });
  },

  async update(resource, slug, params) {
    return axios.patch(`${resource}/${slug}/`, params);
  },

  async put(resource, params) {
    return axios.put(resource + "/", params);
  },

  async delete(resource, slug = "") {
    return axios.delete(resource + "/" + (slug == "" ? "" : slug + "/"));
  },
};

export default ApiService;

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import ApiService from "@/helpers/api.service";
import Modal from "./plugins/modal";

ApiService.init();

const app = createApp(App);
app.use(Modal);
var pinia = createPinia();
app.use(pinia);
app.use(router);
app.mount("#app");

import { ref, computed } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/helpers/api.service";

export const useAuthStore = defineStore("auth", () => {
  const authUser = ref(null);
  const firstCheck = ref(false);
  let resolveFC = null;
  let pfc = new Promise(function (resolve) {
    resolveFC = resolve;
  });

  const isAuthenticated = computed(() => authUser.value != null);
  const isStaff = computed(
    () => authUser.value && authUser.value.is_staff != null,
  );

  async function login(username, password) {
    ApiService.setToken(null);
    const { data } = await ApiService.post("auth/login", {
      username: username,
      password: password,
    });
    ApiService.setToken(data["token"]);
    localStorage.setItem("authToken", JSON.stringify(data));
    const { data: datauser } = await ApiService.get("auth/users/me");
    authUser.value = datauser;
  }

  async function casLogin() {
    window.location = import.meta.env.VITE_APP_API_URL + "auth/cas/login/";
  }

  function logout(send = true) {
    if (send) ApiService.post("auth/logout");
    ApiService.setToken(null);
    authUser.value = null;
    localStorage.removeItem("authToken");
    if (send && import.meta.env.VITE_APP_CAS_AUTH == "true") {
      window.location = import.meta.env.VITE_APP_API_URL + "auth/cas/logout/";
    }
  }

  async function waitFirstCheck() {
    await pfc;
  }

  async function checkAuth() {
    const data = JSON.parse(localStorage.getItem("authToken"));
    const date = new Date().toISOString();
    if (data && date < data.expiry) {
      ApiService.setToken(data["token"]);
      const { data: datauser } = await ApiService.get("auth/users/me");
      authUser.value = datauser;
    } else {
      try {
        if (import.meta.env.VITE_APP_CAS_AUTH == "true") {
          await login();
        }
      } catch (e) {
        logout(false);
      }
    }

    if (!firstCheck.value) {
      firstCheck.value = true;
      resolveFC();
    }
  }

  async function getUser(id) {
    const { data } = await ApiService.get("auth/users", id);
    return data;
  }

  async function updateUser(newdata) {
    const { data: datauser } = await ApiService.put("auth/users/me", newdata);
    authUser.value = datauser;
  }

  async function searchUsers(params) {
    const { data } = await ApiService.query("auth/users/search", params);
    return data.results;
  }

  async function inviteUser(email) {
    const { data } = await ApiService.post("invitation/send", { email });
    return data;
  }
  async function registerUser(params) {
    const { data } = await ApiService.post("auth/users", params);
    return data;
  }
  async function activateUser(params) {
    const { data } = await ApiService.post("auth/users/activation", params);
    return data;
  }
  async function resendActivate(params) {
    const { data } = await ApiService.post(
      "auth/users/resend_activation",
      params,
    );
    return data;
  }
  async function resetPassword(email) {
    const { data } = await ApiService.post("auth/users/reset_password", {
      email,
    });
    return data;
  }
  async function resetPasswordConfirm(params) {
    const { data } = await ApiService.post(
      "auth/users/reset_password_confirm",
      params,
    );
    return data;
  }
  return {
    firstCheck,
    waitFirstCheck,
    authUser,
    isAuthenticated,
    isStaff,
    checkAuth,
    updateUser,
    login,
    casLogin,
    logout,
    searchUsers,
    getUser,
    inviteUser,
    registerUser,
    activateUser,
    resendActivate,
    resetPassword,
    resetPasswordConfirm,
  };
});

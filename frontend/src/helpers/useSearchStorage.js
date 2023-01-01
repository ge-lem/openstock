import { watch } from "vue";

export default function useSearchStorage(name, refresh, defaults, currentPage) {
  function ssGetOrDefault(key, defaultValue) {
    return sessionStorage.getItem(key)
      ? JSON.parse(sessionStorage.getItem(key))
      : defaultValue;
  }

  function setWatch(key, theref) {
    watch(theref, () => {
      sessionStorage.setItem(name + "_" + key, JSON.stringify(theref.value));
    });
  }

  let refs = [];

  for (const [key] of Object.entries(defaults)) {
    if ("_set" in defaults[key])
      defaults[key]._set(
        ssGetOrDefault(name + "_" + key, defaults[key].value),
        true
      );
    else
      defaults[key].value = ssGetOrDefault(
        name + "_" + key,
        defaults[key].value
      );
    setWatch(key, defaults[key]);
    refs.push(defaults[key]);
  }
  if (currentPage) {
    currentPage.value = ssGetOrDefault(name + "_page", 1);
    watch(currentPage, () => {
      sessionStorage.setItem(name + "_page", JSON.stringify(currentPage.value));
    });
    watch(refs, () => {
      currentPage.value = 1;
      refresh();
    });
  }
}

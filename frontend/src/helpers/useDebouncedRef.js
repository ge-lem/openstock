import { customRef } from "vue";

export default function useDebouncedRef(value, delay = 300) {
  let timeout;
  return customRef((track, trigger) => {
    return {
      get() {
        track();
        return value;
      },
      set(newValue, force = false) {
        clearTimeout(timeout);
        if (force) {
          value = newValue;
          trigger();
        } else {
          timeout = setTimeout(() => {
            value = newValue;
            trigger();
          }, delay);
        }
      },
    };
  });
}

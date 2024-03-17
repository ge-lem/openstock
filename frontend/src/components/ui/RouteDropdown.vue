<template>
  <component
    :is="isNav ? 'li' : 'div'"
    ref="root"
    :class="{ 'nav-item': isNav, dropdown: isNav, 'btn-group': !isNav }"
    role="group"
    @focusout="hide"
  >
    <a
      :id="'button' + uid"
      href="#"
      class="dropdown-toggle"
      :class="[isNav ? 'nav-link' : 'btn ' + btnStyle, { show: show }]"
      data-bs-toggle="dropdown"
      aria-expanded="false"
      @click.prevent="toogle"
      ><slot>{{ label }}</slot></a
    >
    <ul
      :id="'tooltip' + uid"
      class="dropdown-menu"
      :class="{ show: show, 'dropdown-menu-dark': isBlack }"
      :style="show && absolute ? style : ''"
    >
      <li v-for="item in items" :key="item.label">
        <router-link
          v-if="item.to"
          v-slot="{ href, navigate }"
          :to="item.to"
          custom
        >
          <a
            :href="href"
            class="dropdown-item"
            @click="goto($event, navigate)"
            >{{ item.label }}</a
          >
        </router-link>
        <a v-else href="#" class="dropdown-item" @click.prevent="click(item)">{{
          item.label
        }}</a>
      </li>
    </ul>
  </component>
</template>

<script setup>
import { ref, computed } from "vue";
import { v4 as uuidv4 } from "uuid";

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
  label: {
    type: String,
    required: false,
  },
  isNav: {
    type: Boolean,
    required: false,
    default: false,
  },
  isBlack: {
    type: Boolean,
    required: false,
    default: false,
  },
  absolute: {
    type: Boolean,
    required: false,
    default: true,
  },
  btnStyle: {
    type: String,
    default: "",
  },
});
const uid = uuidv4();
const show = ref(false);

const style = computed(
  () =>
    "position: absolute; inset: 0px auto auto 0px; margin: 0px; transform: translate(0px, " +
    root.value.clientHeight +
    "px);",
);

const toogle = function () {
  show.value = !show.value;
};
const root = ref(null);
function hide(e) {
  if (props.absolute && root.value && !root.value.contains(e.relatedTarget)) {
    show.value = false;
  }
}
const goto = function (event, navigate) {
  show.value = false;
  navigate(event);
};
const click = function (item) {
  show.value = false;
  item.click();
};
</script>

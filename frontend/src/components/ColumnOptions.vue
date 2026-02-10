<script setup>
const { allColumns, lines } = defineProps(['allColumns', 'lines']);
</script>
<template>
<option v-for="i in allColumns" :value="i" :key="i">
    Colonne #{{ i }}  ({{lines.map(l => l[i - 1]).join(", ")}})
</option>
</template>
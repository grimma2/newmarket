<template>
  <ul :style="`width: ${ulWidth}vw`">
    <li v-for="obj in objectsList" :key="obj">
      <img :src="obj.img" v-if="obj?.img">
      <span v-for="text in obj.textElements" :key="text">{{ text }}</span>
    </li>
  </ul>
</template>

<script>
export default {
  name: "DropdownList",
  props: {
    objectsList: {
      type: Array,
      required: true
    },
    ulWidth: {
      type: Number,
      default: 20
    }
  }
}
</script>

<style scoped>

</style>
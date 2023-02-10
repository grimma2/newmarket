<template>
  <button>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: "project-button"
}
</script>

<style scoped>
  button {
    padding: 5px 10px 5px 10px;
    font-size: 1em;
    border: 1px solid;
    border-radius: 5px;
  }

</style>
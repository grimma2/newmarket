<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  created() {
    if (localStorage.getItem('access')) this.$store.dispatch('auth/fetchAuthUser')
  }
}
</script>

<style>

</style>

<template>
  <div class="header">
    <img src="#" class="header-item logo-img">
    <user-select  class="user-select-item"/>
    <search-products
        class="header-item"
        v-model:search-products-list-show="searchShow"
        v-if="$store.state.auth.userSelect === 'Customer'"
    />
    <nav-bar :buttons="$store.getters['auth/getNavButtons']"  class="header-item"/>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar";
import UserSelect from "@/components/UserSelect";
import SearchProducts from "@/components/SearchProducts";

export default {
  name: "hea-der",
  components: {SearchProducts, UserSelect, NavBar},
  data () {
    return {
      searchShow: false,
    }
  },
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-item {
  padding-left: 15px;
}
</style>
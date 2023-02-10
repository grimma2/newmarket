<template>
  <hea-der/>
  <div class="home">
    <div class="customer-page-wrapper" v-if="$store.state.auth.userSelect === 'Customer'">
      <customer-home-page/>
    </div>
    <div class="company-page-wrapper" v-else>
      <p class="hi-text">
        Продавать на нашем маркетплэйсе очень круто :)
      </p>
    </div>
  </div>
</template>

<script>
import CustomerHomePage from "@/components/CustomerHomePage";
import HeaDer from "@/components/HeaDer";

export default {
  components: {HeaDer, CustomerHomePage}
}

</script>

<style scoped>
.hi-text {
  text-align: center;
  font-size: 2em;
}
</style>

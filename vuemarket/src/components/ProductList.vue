<template>
  <div>
    <div class="post" v-for="product in products" :key="product.id">
      <p>{{ product.name }}</p>
      <img :src="product.photo">
      <span>{{ product.price }}</span>
    </div>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "ProductList",
  computed: {
    ...mapState({
      products: state => state.products.productsList,
      fromInput: state => state.products.fromInput,
      toInput: state => state.products.toInput
    })
  }
}
</script>

<style scoped>

</style>
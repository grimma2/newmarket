<template>
  <div class="customer-home-page">
    <div class="objects-wrapper">
      <div v-for="objects in $store.getters['products/getJoinObjects']" :key="objects">
        <div class="products">
          <div v-for="product in objects.products" :key="product.id">
            <span>{{ product.name }}</span>
            <img :src="product.photo">
            <span>{{ product.rating }}</span>
            <span>{{ product.price }}</span>
          </div>
        </div>
        <div class="categories">
          <div v-for="category in objects.categories" :key="category.id">
            <img :src="category.photo">
            <span>{{ category.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CustomerHomePage",
  beforeMount() {
    let productsModule = this.$store.state.products
    if (!(productsModule.targetProducts.length && productsModule.targetCategories.length)) {
      this.$store.dispatch('products/requestTargetObjects')
    }
  },
}
</script>

<style scoped>
.customer-home-page {
  margin: 0;
}
.objects-wrapper {
  min-height: 100vh;
}
.products {
  display: flex;
  flex-wrap: wrap;
}
.products > * {
  margin: 10px;
}
</style>
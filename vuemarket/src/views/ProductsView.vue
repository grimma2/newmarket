<template>
  <hea-der/>
  <div class="products-view">
    <products-bar
        @updateCat="updateCategory"
        @updateCom="updateCompany"
        @updatePrice="updatePriceGap"
    />
    <product-list/>
  </div>
</template>

<script>
import ProductList from "@/components/ProductList";
import ProductsBar from "@/components/ProductsBar";
import {mapState} from 'vuex'
import HeaDer from "@/components/HeaDer";

export default {
  components: {HeaDer, ProductList, ProductsBar},
  methods: {
    updateCompany(value, i) {
      let newCompanies = [...this.companies]
      newCompanies[i].checkValue = value
      this.$store.commit('products/setCompanies', newCompanies)
    },
    updateCategory(value, i) {
      let newCategories = [...this.categories]
      newCategories[i].checkValue = value
      this.$store.commit('products/setCategories', newCategories)
    },
    updatePriceGap(value, placeholder) {
      if (placeholder === 'от') {
        this.$store.commit('products/setFromInput', value)
      } else {
        this.$store.commit('products/setToInput', value)
      }
    },
  },
  computed: {
    ...mapState({
      companies: state => state.products.companies,
      categories: state => state.products.categories,
      productsList: state => state.products.productsList,
      fromInput: state => state.products.fromInput,
      toInput: state => state.products.toInput
    })
  },
  unmounted () {
    this.$store.commit('products/clearProductsData')
  }
}
</script>

<style scoped>

</style>
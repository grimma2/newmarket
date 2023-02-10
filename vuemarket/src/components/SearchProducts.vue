<template>
  <div class="search-products" @click="hideDropdownList">
    <project-input @click.stop type="text" placeholder="Найти нужный продукт" @input="productSearchInput" :value="productSearch"/>
    <ul @click.stop class="dropdown-search" v-show="searchProductsListShow">
      <li
          @click="$router.push('products_detail/', product.pk)"
          v-for="product in $store.state.header.dropdownList.products"
          :key="product.pk"
      >
        <img :src="product.imgUrl" height="20" width="20">
        <span>{{ product.name }}</span>
        <span class="item-price">{{ product.price }}</span>
      </li>
      <li
          @click="productsRedirect({name: 'products/setCategories', payload: [category.pk]})"
          v-for="category in $store.state.header.dropdownList.categories"
          :key="category.pk"
      >
        <span class="cat-text">{{ category.name }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import mixins from "@/mixins/productsRedirect";
import ProjectInput from "@/components/UI/ProjectInput";

export default {
  name: "SearchProducts",
  components: {ProjectInput},
  mixins: [mixins],
  data () {
    return {
      productSearch: ''
    }
  },
  props: {
    searchProductsListShow: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    productSearchInput (event) {
      const inputValue = event.target.value
      this.productSearch = inputValue

      if (inputValue === '') {
        this.$emit('update:search-products-list-show', false)
        return
      }
      this.$store.dispatch('header/productSearchRequest', inputValue)
      this.$emit('update:search-products-list-show', true)
    },
    hideDropdownList () {
      this.$emit('update:search-products-list-show', false)
    }
  },
}
</script>

<style scoped>
.search-products {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

ul {
  padding: 0 0;
  list-style-type: none;
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 7vh;
}

li {
  height: 6vh;
  width: 25vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.item-price {
  justify-content: flex-end;
}
</style>
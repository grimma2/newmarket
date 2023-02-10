<template>
  <form @submit.prevent>
    <div class="checkboxes">
      <div class="categories">
        <div class="category" v-for="(category, i) in categories" :key="category.id">
          <input
              :checked="category.checkValue"
              @input="categoryUpdate($event, i)"
              type="checkbox"
          >{{ category.name }}
        </div>
      </div>
      <div class="companies">
        <div class="company" v-for="(company, i) in companies" :key="company.id">
          <input
              :checked="company.checkValue"
              @input="companyUpdate($event, i)"
              type="checkbox"
          >{{ company.username }}
        </div>
      </div>
    </div>
    <div class="price-inputs">
      <input
          type="number"
          :value="fromInput"
          @input="updatePriceGap"
          placeholder="от"
      />
      <input
          type="number"
          :value="toInput"
          @input="updatePriceGap"
          placeholder="до"
      />
      <button>Применить</button>
    </div>
  </form>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "ProductsBar",
  methods: {
    companyUpdate (event, i) {
      this.$emit('updateCom', event.target.checked, i)
    },
    categoryUpdate (event, i) {
      this.$emit('updateCat', event.target.checked, i)
    },
    updatePriceGap (event) {
      this.$emit('updatePrice', event.target.checked, event.target.placeholder)
    }
  },
  computed: {
    ...mapState({
      categories: state => state.products.categories,
      companies: state => state.products.companies,
      fromInput: state => state.products.fromInput,
      toInput: state => state.products.toInput
    })
  }
}
</script>

<style scoped>

</style>
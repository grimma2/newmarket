<template>
  <hea-der/>
  <div class="product-page">
    <div class="head-part">
      <div class="left-side-header">
        <p>{{ product.name }}</p>
        <img :src="product.photo">
      </div>
      <div class="right-side-header">
        <span>{{ product.price }}</span>
        <span>{{ product.rating }}</span>
      </div>
    </div>
    <div class="content-block">
      <p><strong>Описание</strong></p>
      <p>{{ product.description }}</p>
      <p>
        <span v-for="param in product.params" :key="param[0]">
          <strong>{{ param[0] }}</strong>: {{ param[1] }}
        </span>
      </p>
      <comments-user :comments="comments"/>
    </div>
  </div>
</template>

<script>
import CommentsUser from "@/components/CommentsUser";
import HeaDer from "@/components/HeaDer";

export default {
  name: "ProductPage",
  components: {HeaDer, CommentsUser},
  props: {
    product: {
      type: Object,
      required: true
    },
    comments: {
      type: Array,
      default: []
    }
  }
}
</script>

<style scoped>

</style>
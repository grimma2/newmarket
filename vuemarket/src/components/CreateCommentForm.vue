<template>
  <img :src="$store.state.auth.user.avatar">
  <form @submit.prevent="emitCreateComment">
    <star-rating :value="3"></star-rating>
    <input type="text" placeholder="Напишите ваш отзыв о товаре">
  </form>
</template>

<script>
import StarRating from "@/components/UI/starrating/starElement";

export default {
  name: "CreateCommentForm",
  components: {StarRating},
  methods: {
    emitCreateComment (event) {
      console.log(event)
      this.$emit('createComment', {
        event
      })
    }
  }
}
</script>

<style scoped>

</style>
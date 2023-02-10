<template>
  <div v-if="setCommentOrNull">
    <span>{{ $store.state.auth.user.username }}</span>
    <img :src="$store.state.auth.user.avatar">
    <p v-if="showUpdatingPart">
      <span>{{ userComment.text }}</span>
      <span>{{ userComment.rating }}</span>
    </p>
    <input
        v-else
        type="text"
        placeholder="Введите новый текст отзыва"
        v-model="userComment.text"
        @keydown="emitCommentUpdate"
    >
    <button @click="showUpdatingPart = !showUpdatingPart">Изменить</button>
  </div>
</template>

<script>
export default {
  name: "SingleUserComment",
  props: {
    comments: {
      type: Array,
      default: []
    }
  },
  data () {
    return {
      userComment: {},
      showUpdatingPart: true
    }
  },
  methods: {
    setCommentOrNull () {
      this.userComment = this.$store.getters['auth/getUserCommentOrNull'](this.comments)
    },
    emitCommentUpdate (event) {
      if (event.keyCode === 13) {
        this.$emit('updateComment', this.userComment)
      }
    }
  }
}
</script>

<style scoped>

</style>
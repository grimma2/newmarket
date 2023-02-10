<template>
  <div class="comments-user">
    <div class="special-elements" v-if="$store.state.auth.authData.isAuth">
      <div>
        <single-user-comment
            :comments="comments"
            @updateComment="requestUpdateComment"
        />
      </div>
      <div v-else>
        <create-comment-form
            @createComment="requestCreateComment"
        />
      </div>
    </div>
    <div v-for="comment in comments" :key="comment.id">
      <img :src="comment.user_who_put.avatar">
      <span>{{ comment.user_who_put.username }}</span>
      <span>{{ comment.rating }}</span>
      <span>{{ comment.text }}</span>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import CreateCommentForm from "@/components/CreateCommentForm";
import SingleUserComment from "@/components/SingleUserComment";

export default {
  name: "CommentsUser",
  components: {SingleUserComment, CreateCommentForm},
  props: {
    comments: {
      type: Array,
      default: []
    },
    product: {
      type: Object
    }
  },
  methods: {
    async requestCreateComment (params) {
      await axios.post(`http://${window.location.host}/mainapp/create_comment/`, {params: params})
    },
    async requestUpdateComment (params) {
      params.object_slug = this.product.slug
      params.content_type = 'Product'
      await axios.post('<update_url', {params: params})
    }
  }
}
</script>

<style scoped>

</style>
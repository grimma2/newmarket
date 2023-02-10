<template>
  <li class="user-menu-option" @click.stop="useCallableObject">
    <img :src="option.imgSrc" v-if="option.imgSrc" class="option-img">
    <span class="option-text">{{ option.text }}</span>
  </li>
</template>

<script>
export default {
  name: "UserMenuOption",
  props: {
    option: {
      type: Object,
      required: true
    }
  },
  methods: {
    useCallableObject () {
      let callFunc = this.option.onclick.callableObject
      if (callFunc.name === 'push') this.$store.dispatch('header/closeUserMenu')
      callFunc(...this.option.onclick.objectArgs)
    }
  }
}
</script>

<style scoped>

</style>
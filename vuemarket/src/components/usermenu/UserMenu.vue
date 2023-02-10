<template>
  <div class="user-menu">
    <img
      src="#"
      alt="back button"
      v-if="$store.getters['header/backButtonIsExists']"
      @click.stop="$store.dispatch('header/showPreviousUserMenu')"
    >
    <ul class="options">
      <user-menu-option :option="option" class="option" v-for="option in getUserMenuOptions()" :key="option.textId"/>
    </ul>
  </div>
</template>

<script>
import UserMenuOption from "@/components/usermenu/UserMenuOption";

export default {
  name: "UserMenu",
  components: {UserMenuOption},
  methods: {
    getUserMenuOptions () {
      const userMenu = [
        {
          options: ['favorites', 'myOrders', 'theme', 'findNeededProduct', 'cart']
        },
        {options: ['light', 'dark']}
      ]

      const userMenuOptions = [
        {
          textId: 'favorites',
          text: 'Избранное',
          onclick: {callableObject: this.$router.push, objectArgs: [{path: '/favorites'}]}
        },
        {
          textId: 'myOrders',
          text: 'Мои заказы',
          onclick: {callableObject: this.$router.push, objectArgs: [{path: '/my-orders'}]}
        },
        {
          textId: 'theme',
          text: 'Тема сайта',
          onclick: {callableObject: this.$store.dispatch, objectArgs: ['header/showNextUserMenu', 1]}
        },
        {
          textId: 'findNeededProduct',
          text: 'Подобрать нужный продукт',
          onclick: {callableObject: this.$router.push, objectArgs: [{path: '/find-needed-product'}]}
        },
        {
          textId: 'cart',
          text: 'Корзина',
          onclick: {callableObject: this.$router.push, objectArgs: [{path: '/cart'}]}
        },
        {
          textId: 'light',
          text: 'Светлая',
          onclick: {callableObject: this.$store.dispatch, objectArgs: ['header/turnLightTheme']}
        },
        {
          textId: 'dark',
          text: 'Тёмная',
          onclick: {callableObject: this.$store.dispatch, objectArgs: ['header/turnDarkTheme']}
        },
      ]
      let menu = userMenu[this.$store.state.header.userMenu.showed]
      return userMenuOptions.filter(op => menu.options.includes(op.textId))
    },
    close (e) {
      if (!this.$el.contains(e.target)) {
        this.$store.dispatch('header/closeUserMenu')
      }
    }
  },
  mounted () {
    document.addEventListener('click', this.close)
  },
  beforeUnmount () {
    document.removeEventListener('click', this.close)
  }
}
</script>

<style scoped>

</style>
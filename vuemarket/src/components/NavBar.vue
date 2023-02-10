<template>
  <div class="nav-bar" v-show="buttons">
    <project-button
        v-for="button in buttons"
        :key="button"
        @click="$router.push(button.src)"
        class="nav-bar-item"
    >
      {{ button.name }}
    </project-button>
    <div v-if="$store.state.auth.access" class="nav-bar-item">
      <img src="#" @click.stop="openFirstMenu">
      <user-menu v-if="!(this.$store.state.header.userMenu.showed === false)"/>
    </div>
  </div>
</template>

<script>
import ProjectButton from "@/components/UI/ProjectButton";
import UserMenu from "@/components/usermenu/UserMenu";

export default {
  name: "NavBar",
  components: {UserMenu, ProjectButton},
  props: {
    buttons: {
      type: Array,
    }
  },
  methods: {
    openFirstMenu () {
      this.$store.commit('header/clearHistory')
      this.$store.commit('header/setUserMenuShowed', 0)
    }
  }
}
</script>

<style scoped>
  .nav-bar {
    width: 50vw;
    display: flex;
    justify-content: space-around;
  }
</style>
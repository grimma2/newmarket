<template>
  <div class="user-select">
    <button
        v-for="button in buttons"
        :key="button.id"
        @click="changeUserSelect(button.selectValue)"
        :class="($store.state.auth.userSelect === button.selectValue) ? 'selected' : ''"
    >
      {{ button.name }}
    </button>
  </div>
</template>

<script>

export default {
  name: "UserSelect",
  data () {
    return {
      buttons: [
        {name: 'Продавать', id: 1, selectValue: 'Company'},
        {name: 'Покупать', id: 2, selectValue: 'Customer'}
      ]
    }
  },
  props: {
    redirectAfterClick: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    changeUserSelect (selectValue) {
      this.$store.commit('auth/setUserSelect', selectValue)
      if (this.redirectAfterClick) { this.$router.push({path: '/'}) }
    }
  }
}
</script>

<style scoped>
.selected {
  background-color: #000000;
  color: #ffffff;
}
button {
  border: 1px solid;
  border-radius: 5px;
}

</style>
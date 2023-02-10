<template>
  <form @submit.prevent="loginUser">
    <input type="text" placeholder="Введите логин" v-model="username"/>
    <input type="text" placeholder="Введите пароль" v-model="password"/>
    <button type="submit">Войти</button>
  </form>
  <p v-if="error">{{ error }}</p>
  <p @click="$router.push({path: '/register'})">Или зарегестрируйтесь</p>
</template>

<script>
import loginMixin from "@/mixins/loginMixin";


export default {
  name: "LoginPage",
  mixins: [loginMixin],
  data () {
    return {
      error: ''
    }
  },
  methods: {
    loginUser () {
      this.error = ''
      this.validateForm()
      if (this.error) return

      try {
        this.$store.dispatch(
            'auth/login',
            {username: this.username, password: this.password}
        )
        this.$router.push({path: '/'})
      } catch (e) {
        console.log(e)
        this.error = e
      }
    },
    validateForm () {
      if (!this.username) {
        this.error = 'Поле username обязательно'
      }
      this._validatePassword()
    },
    _validatePassword () {
      if (this.password.length < 8) return
      this.error = 'Поле password должно содержать как минимум 8 символов'
    }
  }
}
</script>

<style scoped>

</style>
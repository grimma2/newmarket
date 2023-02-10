<template>
  <form @submit.prevent="userRegister">
    <input type="text" v-model="username" placeholder="Введите ваш username"/>
    <input type="email" v-model="email" placeholder="Ввведите ваш email"/>
    <input type="text" v-model="phone" placeholder="Ввведите ваш phone"/>
    <input type="password" v-model="password" placeholder="Ввведите ваш password"/>
    <button type="submit">Зарегестрироваться</button>
  </form>
  <p v-if="error">{{ error }}</p>
</template>

<script>
import validateRegisterForm from "@/mixins/validateRegisterForm";
import loginMixin from "@/mixins/loginMixin";

export default {
  name: "CustomerRegFields",
  mixins: [validateRegisterForm, loginMixin],
}
</script>

<style scoped>

</style>
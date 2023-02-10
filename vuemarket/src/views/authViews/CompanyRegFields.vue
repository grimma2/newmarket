<template>
  <form @submit.prevent="userRegister">
    <input type="text" v-model="username" placeholder="Введите название юр. лица"/>
    <input type="text" v-model="password" placeholder="Введите пароль"/>
    <input type="text" v-model="phone" placeholder="Ввведите ваш phone"/>
    <input type="email" v-model="email" placeholder="Введите email"/>
    <button type="submit">Зарегестрироваться</button>
  </form>
  <p v-if="error">{{ error }}</p>
</template>

<script>
import validateRegisterForm from "@/mixins/validateRegisterForm";
import loginMixin from "@/mixins/loginMixin";

export default {
  name: "CompanyRegFields",
  mixins: [validateRegisterForm, loginMixin],
}
</script>

<style scoped>

</style>
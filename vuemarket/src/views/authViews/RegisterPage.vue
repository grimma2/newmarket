<template>
  <div class="register">
    <customer-reg-fields
        v-if="$store.state.auth.userSelect === 'Customer'"
        :error="error"
        @onSubmit="userRegister"
        @changeError="changeErrorValue"
    />
    <company-reg-fields
        v-else
        :error="error"
        @onSubmit="userRegister"
        @changeError="changeErrorValue"
    />
    <p @click="$router.push({path: '/login'})">Войти</p>
    <user-select :redirect-after-click="false"/>
  </div>
</template>

<script>
import UserSelect from "@/components/UserSelect";
import CustomerRegFields from "@/views/authViews/CustomerRegFields";
import CompanyRegFields from "@/views/authViews/CompanyRegFields";

export default {
  name: "CustomerRegister",
  components: {CompanyRegFields, CustomerRegFields, UserSelect},
  data () {
    return {
      error: ''
    }
  },
  methods: {
    userRegister (userData) {
      try {
        this.$store.dispatch('auth/register', {...userData})
        this.$router.push({path: '/'})
      } catch (e) {
        console.log(e)
        this.error = e
      }
    },
    changeErrorValue (value) {
      this.error = value
      console.log('change error call')
    }
  }
}
</script>

<style scoped>

</style>
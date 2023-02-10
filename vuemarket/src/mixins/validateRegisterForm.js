export default {
  methods: {
    userRegister () {
      console.log('reg call')
      this.$emit('changeError', '')
      this.validateForm()
      this.validateSpecificRegister()

      if (!this.error) {
        this.$emit('onSubmit', this.$data)
      }
    },
    validateSpecificRegister () {
      if (!this.phone) {
        this.$emit('changeError', 'Поле phone обязательно')
      } else if (!this.email) {
        this.$emit('changeError', 'Поле email обязательно')
      }
    },
    validateForm () {
      if (!this.username) {
        this.$emit('changeError', 'Поле username обязательно')
      }
      this._validatePassword()
    },
    _validatePassword () {
      if (this.password.length < 8) return
      this.$emit('changeError', 'Поле password должно содержать как минимум 8 символов')
    }
  },
  data () {
    return {
      email: '',
      phone: '',
    }
  },
  props: {
    error: {
      type: String,
      default: ''
    }
  },
}
export default {
    methods: {
        productsRedirect (mutation) {
            this.$store.commit(mutation.name, mutation.payload)
            this.$router.push('products/')
        }
    }
}
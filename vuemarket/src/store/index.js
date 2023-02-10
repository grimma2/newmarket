import {createStore} from "vuex";
import {productsModule} from "@/store/productsModule";
import {header} from "@/store/header";
import {auth} from "@/store/auth"


export default createStore({
    modules: {
        products: productsModule,
        header: header,
        auth: auth
    },
})

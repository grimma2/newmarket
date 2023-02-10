import urls from '@/api/apiUrlPatterns.json'
import {authAxios, defaultAxios} from "@/api/apiData";


const buttonsSelect = {
    Customer: {
        isAuthTrue: [
            {name: 'Избранное', src: 'favorites/'},
            {name: 'Мои заказы', src: 'my_orders/'},
            {name: 'Корзина', src: 'cart/'},
        ],
        isAuthFalse: [
            {name: 'Войти', src: 'login/'},
            {name: 'Регистрация', src: 'register/'},
            {name: 'Избранное', src: 'favorites/'},
            {name: 'Мои заказы', src: 'my_orders/'},
            {name: 'Корзина', src: 'cart/'}
        ]
    },
    Company: {
        isAuthFalse: [
            {name: 'Админка', src: 'admin/company/'},
            {name: 'Подать заявку на регестрацию', src: 'register/'},
            {name: 'Войти как продавец', src: 'login/'}
        ],
        isAuthTrue: []
    }
}

export const auth = {
    state: () => ({
        access: localStorage.getItem('access'),
        userSelect: 'Customer',
        user: {}
    }),
    getters: {
        getNavButtons (state) {
            if (state.access) {
                return buttonsSelect[state.userSelect].isAuthTrue
            } else {
                return buttonsSelect[state.userSelect].isAuthFalse
            }
        },
        getUserCommentOrNull: (state) => (comments) => {
            for (let i = 0; i < comments.length; i++) {
                if (comments[i].user === state.user) {
                    return comments[i]
                }
            }
            return null
        }
    },
    mutations: {
        setUserSelect (state, userSelect) {
            state.userSelect = userSelect
        },
        setAccess (state, access) {
            console.log('mutation set access token...')
            state.access = access
        },
        setUser (state, user) {
            state.user = user
        }
    },
    actions: {
        async login ({commit}, {username, password}) {
            const response = await defaultAxios.post(urls.mainapp.token_pair, {
                username: username,
                password: password
            })

            commit('setUser', response.data.user)
            commit('setAccess', response.data.access)
            localStorage.setItem('access', response.data.access)
            localStorage.setItem('user_id', response.data.user.id.toString())
            authAxios.defaults.headers['Authorization'] = `Bearer ${response.data.access}`
        },
        async logout ({commit}, {username}) {
            await defaultAxios.post(urls.mainapp.logout, {username: username})
            localStorage.removeItem('access')
            localStorage.removeItem('user_id')
            commit('setUser', {})
            commit('setAccess', '')
            authAxios.defaults.headers['Authorization'] = ''
        },
        async register ({dispatch}, registerParams) {
            try {
                const response = await defaultAxios.post(
                  urls.mainapp.register, registerParams
                )
                dispatch('login', response.data)
            } catch (e) {
                console.log(e.message)
            }
        },
        async fetchAuthUser({commit, state}) {
            console.log('fetchAuthUser...')
            let response;
            let reqData = [urls.mainapp.get_auth_user, {user_id: localStorage.getItem('user_id')}]
            try {
                response = await authAxios.post(...reqData)
            } catch (e) {
                if (!state.access) {
                    return
                } else {
                    console.log('access exists in store')
                }
                response = await authAxios.post(...reqData)
            }
            commit('setUser', response.data.user)
        }
    },
    namespaced: true
}
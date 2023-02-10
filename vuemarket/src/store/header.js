import {apiUrl, defaultAxios} from "@/api/apiData";
import urls from '@/api/apiUrlPatterns.json';


export const header = {
  state: () => ({
    dropdownList: {products: [], categories: []},
    userMenu: {
      showed: false,
      history: []
    }
  }),
  getters: {
    backButtonIsExists (state) {
      return state.userMenu.history.length
    }
  },
  mutations: {
    setSearchCategories (state, categories) {
      state.dropdownList.categories = categories
    },
    setSearchProducts (state, products) {
      state.dropdownList.products = products
    },
    setUserMenuShowed(state, userMenuShowed) {
      state.userMenu.showed = userMenuShowed
    },
    addToHistory (state) {
      state.userMenu.history.push(state.userMenu.showed)
    },
    removeFromHistory (state) {
      state.userMenu.history.splice(-1)
    },
    clearHistory (state) {
      state.userMenu.history = []
    }
  },
  actions: {
    async productSearchRequest ({commit}, inputText) {
      let response = await defaultAxios.post(apiUrl + urls.products.product_search, {
        input_text: inputText
      })
      let data = await response.json()
      commit('setSearchCategories', data.categories)
      commit('setSearchProducts', data.products)
    },
    showNextUserMenu ({commit}, userMenu) {
      // add current open menu in history
      commit('addToHistory')
      // update current open menu
      commit('setUserMenuShowed', userMenu)
    },
    showPreviousUserMenu ({state, commit}) {
      // show last userMenu from history
      commit('setUserMenuShowed', state.userMenu.history.slice(-1)[0])
      // remove last userMenu from history
      commit('removeFromHistory')
    },
    closeUserMenu ({commit}) {
      console.log('clear his')
      commit('clearHistory')
      commit('setUserMenuShowed', false)
    },
  },
  namespaced: true
}
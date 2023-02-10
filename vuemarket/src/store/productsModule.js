import urls from '@/api/apiUrlPatterns.json'
import {defaultAxios} from "@/api/apiData";


export const productsModule = {
    state: () => ({
        targetObjects: [],
        targetProducts: [],
        targetCategories: [],
        companies: [
            {
                'id': 1,
                'username': 'company1',
                'checkValue': false
            },
            {
                'id': 2,
                'username': 'company2',
                'checkValue': true
            },
            {
                'id': 3,
                'username': 'company3',
                'checkValue': false
            },
        ],
        categories: [
            {
                'name': 'cat 1',
                'id': 1,
                'checkValue': false
            },
            {
                'name': 'cat 2',
                'id': 2,
                'checkValue': false
            },
            {
                'name': 'cat 3',
                'id': 3,
                'checkValue': true
            },
        ],
        productsList: [
            {
                'id': 1,
                'name': 'prod 1',
                'price': 1200,
                'photo': 'media/products/testimg.ipg'
            },
            {
                'id': 2,
                'name': 'prod 2',
                'price': 2200,
                'photo': 'media/products/testimg.ipg'
            }
        ],
        fromInput: 0,
        toInput: 0
    }),
    getters: {
        productDataToQuery (state) {
          let company_set = '';
          let category_set = '';
          for (let i = 0; i < state.companies.length; i++) {
              if (state.companies[i].checkValue) {
                  company_set = company_set + state.companies[i].id + ','
              }
          }
          for (let i = 0; i < state.categories.length; i++) {
              if (state.categories[i].checkValue) {
                  category_set = category_set + state.companies[i].id + ','
              }
          }
          company_set = company_set.substring(0, company_set.length - 1)
          category_set = category_set.substring(0, category_set.length - 1)
          let query = {
            companies: company_set,
            categories: category_set,
            from: state.fromInput,
            to: state.toInput
          }
          for (let key of Object.keys(query)) {
            if (!query[key]) {
              delete query[key]
            }
          }

          return query
        },
        getJoinObjects: (state) => {
            const PRODUCTS_IN_OBJECT = 10
            const CATEGORIES_IN_OBJECT = 2
            const COMPLEX_OBJECTS_ON_PAGE = 4

            let productsTarget = [...state.targetProducts.slice(0, PRODUCTS_IN_OBJECT * COMPLEX_OBJECTS_ON_PAGE)]
            let categoriesTarget = [...state.targetCategories.slice(0, CATEGORIES_IN_OBJECT * COMPLEX_OBJECTS_ON_PAGE)]

            let objects = [
                {products: [], categories: []}
            ]

            for (let i = 0; i < productsTarget.length; i++) {
                for (let j = 0; j < objects.length; j++) {
                    if (objects[j].products.length < PRODUCTS_IN_OBJECT) {
                        objects[j].products.push(productsTarget[i])
                        continue
                    }
                    let objectIsFilled = objects[j].products.length >= PRODUCTS_IN_OBJECT
                    let objectsElementIsLast = objects.length - 1 == j
                    let productsElementIsLast = productsTarget.length - 1 == i
                    if ((objectIsFilled) && (objectsElementIsLast) && (!productsElementIsLast)) {
                        objects.push({products: [], categories: []})
                    }
                }
            }
            for (let i = 0; i < categoriesTarget.length; i++) {
                for (let j = 0; j < objects.length; j++) {
                    if (objects[j].categories.length < CATEGORIES_IN_OBJECT) {
                        objects[j].categories.push(categoriesTarget[i])
                        continue
                    }
                    let objectIsFilled = objects[j].categories.length >= CATEGORIES_IN_OBJECT
                    let objectsElementIsLast = objects.length - 1 == j
                    let categoriesElementIsLast = categoriesTarget.length - 1 == i
                    if ((objectIsFilled) && (objectsElementIsLast) && (!categoriesElementIsLast)) {
                        objects.push({products: [], categories: []})
                    }
                }
            }

            return objects
        },
    },
    mutations: {
        setProducts (state, productsList) {
            state.productsList = productsList
        },
        setCompanies (state, companies) {
            state.companies = companies
        },
        setCategories (state, categories) {
            state.categories = categories
        },
        setFromInput (state, fromInput) {
            state.fromInput = fromInput
        },
        setToInput (state, toInput) {
            state.toInput = toInput
        },
        clearProductsData (state) {
            state.companies = []
            state.categories = []
            state.fromInput = 0
            state.toInput = 0
            state.productsList = []
        },
        setTargetProducts (state, targetProducts) {
            state.targetProducts = targetProducts
        },
        setTargetCategories (state, targetCategories) {
            state.targetCategories = targetCategories
        },
    },
    actions: {
        // async sendProductQuery ({commit}) {
        //     let response = await fetch(
        //       apiUrl, {
        //           method: 'GET',
        //           headers: defaultHeaders,
        //           body: JSON.stringify({})
        //       }
        //     )
        //     let data = await response.json()
        //
        //     commit('setProducts', data.products)
        //     commit('setCategories', data.response.productBar.categories)
        //     commit('setCompanies', data.response.productBar.companies)
        //     commit('setFromInput', data.response.productBar.from)
        //     commit('setToInput', data.response.productBar.to)
        // },
        async requestTargetObjects ({commit}) {
            const response = await defaultAxios.post(
                urls.products.get_target_products,
                {
                    categories: 'categories',
                    companies: 'companies'
                }
            )
            // 'products' array contains 100 objects or least
            // And 'categories' array contains 50 objects or least
            commit('setTargetProducts', response.data.products)
            commit('setTargetCategories', response.data.categories)
        }
    },
    namespaced: true
}

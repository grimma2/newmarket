import axios from 'axios'
import store from '@/store/index'
import urls from '@/api/apiUrlPatterns.json'


export const apiUrl = 'http://localhost:8000/'
export let defaultAxios = axios.create({
    baseURL: apiUrl,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
})

export let authAxios = axios.create({
    baseURL: apiUrl,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
    }
})

async function authRequestError (error) {
    console.log('error interceptor...')
    if (error.response.status === 401) {
        console.log('error 401...')
        // get a refresh token for current user by user_id
        let resRefresh = await defaultAxios.post(
          urls.mainapp.get_refresh, {user_id: localStorage.getItem('user_id')}
        )

        // get a new access token by refresh
        try {
            let newAccess = await defaultAxios.post(
              urls.mainapp.refresh, {refresh: resRefresh.data.refresh}
            )
            // delete all user data from localStorage and state if refresh token is invalid
            localStorage.setItem('access', newAccess.data.access)
            store.commit('auth/setAccess', newAccess.data.access)
            authAxios.defaults.headers['Authorization'] = `Bearer ${newAccess.data.access}`
            console.log('end block finally')
        } catch {
            localStorage.removeItem('user_id')
            localStorage.removeItem('access')
            authAxios.defaults.headers['Authorization'] = ''
            store.commit('auth/setAccess', '')
            this.$router.push({name: 'login/'})
            console.log('invalid refresh')
        }
    }
    return Promise.reject(error)
}

authAxios.interceptors.response.use(
  (response) => response,
  authRequestError
)
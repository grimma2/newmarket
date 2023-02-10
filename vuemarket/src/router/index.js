import {createRouter, createWebHistory} from 'vue-router'
import ProductsView from "@/views/ProductsView";
import Home from '@/views/HomePage'
import LoginPage from "@/views/authViews/LoginPage";
import RegisterPage from "@/views/authViews/RegisterPage";


const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/products/',
    component: ProductsView
  },
  {
    path: '/login/',
    component: LoginPage
  },
  {
    path: '/register/',
    component: RegisterPage
  }
]

const router = createRouter({
  routes,
  history: createWebHistory()
})

export default router

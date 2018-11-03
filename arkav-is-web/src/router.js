import Vue from 'vue'
import Router from 'vue-router'
import { requireLogin, requireGuest } from './guards.js'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import TeamPage from './views/TeamPage.vue'
import Dashboard from './views/Dashboard.vue'
import Register from './views/Register.vue'
import CreateTeam from './views/CreateTeam'
Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: Home,
      beforeEnter: requireLogin,
      children: [
        {
          path: '',
          name: 'dashboard',
          component: Dashboard
        },
        {
          path: 'teams',
          name: 'teams',
          component: TeamPage,
        },
        {
          path: 'create-team',
          name: 'create-team',
          component: CreateTeam,
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      beforeEnter: requireGuest
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      beforeEnter: requireGuest
    }
  ]
})

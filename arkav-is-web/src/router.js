import Vue from 'vue'
import Router from 'vue-router'
import { requireLogin, requireGuest } from './guards.js'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import TeamPage from './views/TeamPage.vue'

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
          path: 'teams',
          name: 'teams',
          component: TeamPage,
        },
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      // beforeEnter: requireGuest
    },
  ]
})

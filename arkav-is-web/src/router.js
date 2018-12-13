import Vue from 'vue'
import Router from 'vue-router'
import { requireLogin, requireGuest } from './guards.js'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import ForgotPassword from './views/ForgotPassword'
import ResetPassword from './views/ResetPassword'
import ConfirmEmail from './views/ConfirmEmail'
import TeamPage from './views/TeamPage.vue'
import Dashboard from './views/Dashboard.vue'
import Register from './views/Register.vue'
import CreateTeam from './views/CreateTeam'
import CodingClass from './views/CodingClass'
Vue.use(Router)

const router = new Router({
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
          path: 'teams/:id',
          name: 'team',
          component: TeamPage,
        },
        {
          path: 'preevent/codingclass',
          name: 'codingclass',
          component: CodingClass,
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
      beforeEnter: requireGuest,
      meta: {
        title: 'Login Arkavidia 5.0'
      },
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      beforeEnter: requireGuest,
      meta: {
        title: 'Pendaftaran Arkavidia 5.0'
      },
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPassword,
      beforeEnter: requireGuest,
      meta: {
        title: 'Reset Password Arkavidia 5.0'
      },
    },
    {
      path: '/reset-password/:token',
      name: 'reset-password',
      component: ResetPassword,
      beforeEnter: requireGuest,
      meta: {
        title: 'Reset Password Arkavidia 5.0'
      },
    },
    {
      path: '/confirm-email/:token',
      name: 'confirm-email',
      component: ConfirmEmail,
      beforeEnter: requireGuest,
      meta: {
        title: 'Konfirmasi Email Arkavidia 5.0'
      },
    }
  ],
})

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router

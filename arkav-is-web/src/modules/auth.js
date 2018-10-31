import api from '../api'

export default {
  namespaced: true,
  state: {
    errors: [],
    loading: false,
    user: null,
    loginRedirect: null,
  },
  getters: {
    isLoggedIn (state) {
      return !!state.user
    }
  },
  mutations: {
    addError(state, message) {
      state.errors.push(message + '')
    },
    clearError(state) {
      state.errors = []
    },
    setLoading(state, isLoading) {
      state.loading = isLoading
    },
    setUser(state, user) {
      state.user = user
    },
    setLoginRedirect(state, redirectTo) {
      state.loginRedirect = redirectTo
    },
  },
  actions: {
    async login({ commit }, { email, password, router }) {
      try {
        commit('setLoading', true)
        commit('clearError')
        let response = await api.post('/auth/login/', { email, password }, { ignoreUnauthorizedError: true })
        commit('setUser', response.data)

        // Redirect after login
        let redirectTo = this.loginRedirect
        if (!redirectTo) redirectTo = { name: 'dashboard' }
        router.push(redirectTo)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async register({commit}, {full_name, email, password, router}) {
      try {
        commit('setLoading', true)
        commit('clearError')
        let response = await api.post('/auth/register/', {full_name, email, password}, { ignoreUnauthorizedError: true })
        commit ('setUser', response.data)
        //Redirect if Register successful
        let redirectTo = this.loginRedirect;
        if (!redirectTo) redirectTo = {name: 'dashboard'}
        router.push(redirectTo)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async logout({ commit }) {
      try {
        commit('setLoading', true)
        commit('clearError')
        await api.post('/auth/logout/', null, { ignoreUnauthorizedError: true })
        commit('setUser', null)
        // Reset Vuex state by reloading page
        location.reload(true)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    }
  }
}

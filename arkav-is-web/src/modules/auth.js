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
    async login({ commit }, { username, password, router }) {
      try {
        commit('setLoading', true)
        commit('clearError')
        let response = await api.post('/auth/login/', { username, password }, { ignoreUnauthorizedError: true })
        commit('setUser', response.data)

        // Redirect after login
        let redirectTo = this.loginRedirect
        if (!redirectTo) redirectTo = { name: 'teams' }
        router.push(redirectTo)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },

    async logout({ commit }, { router }) {
      try {
        commit('setLoading', true)
        commit('clearError')
        await api.post('/auth/logout/', null, { ignoreUnauthorizedError: true })
        commit('setUser', null)
        // Redirect to login after logout
        router.push({ name: 'login' })
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    }
  }
}

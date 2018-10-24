import api from '../api'

export default {
  namespaced: true,
  state: {
    errors: [],
    loading: false,
    user: null
  },
  getters: {
    isLoggedIn (state) {
      return !!state.user
    }
  },
  mutations: {
    addError (state, message) {
      state.errors.push(message + '')
    },
    clearError (state) {
      state.errors = []
    },
    setLoading (state, isLoading) {
      state.loading = isLoading
    },
    setUser (state, { user }) {
      state.user = user
    }
  },
  actions: {
    async login ({ commit }, { username, password }) {
      try {
        commit('setLoading', true)
        commit('clearError')
        let user = await api.post('/login', { username, password })
        commit('setUser', user);
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
        await api.post('/logout')
        commit('setUser', null);
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    }
  }
}

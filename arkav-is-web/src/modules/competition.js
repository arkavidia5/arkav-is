import api from '../api'

export default {
  namespaced: true,
  state: {
    errors: [],
    loading: false,
    competitions: [],
    teams: [],
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
    setCompetitions(state, competitions) {
      state.competitions = competitions
    },
    setTeams(state, teams) {
      state.teams = teams
    },
  },
  actions: {
    async getCompetitions({ commit }) {
      try {
        commit('setLoading', true)
        commit('clearError')
        let response = await api.get('/competitions/', { ignoreUnauthorizedError: true })
        commit('setCompetitions', response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async getTeams({ commit }) {
      try {
        commit('setLoading', true)
        commit('clearError')
        let response = await api.get('/competitions/teams/', { ignoreUnauthorizedError: true })
        commit('setTeams', response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
  }
}

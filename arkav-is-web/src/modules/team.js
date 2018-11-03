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
  },
  actions: {
    async submitTeam({ commit }, {competition, name, category, school, members}) {
      try {
        commit('setLoading', true)
        commit('clearError')
        // console.log(!competition, !name, !category, !school, !members)
        if(!competition || !name || !category || !school || !members) {
            throw 'Pastikan seluruh data terisi'
        }
        if(members.length < competition.min_team_members || members.length > competition.max_team_members) {
            throw 'Jumlah peserta tidak sesuai'
        }
        members.forEach((member) => {
            if(!member.name || !member.email || !(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(member.email))) {
                throw 'Pastikan seluruh data valid'
            }
        });
        let response = await api.post('/register-team/', {competition}, { ignoreUnauthorizedError: true })
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
  }
}

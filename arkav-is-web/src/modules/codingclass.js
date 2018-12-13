import api from '../api'

export default {
  namespaced: true,
  state: {
    errors: [],
    loading: false,
    isOpen: false,
    registrationData: [],
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
    setRegistrationData(state, data) {
      state.registrationData = data
    },
    setRegistrationOpen(state, status){
      state.isOpen = status
    }
  },
  actions: {
    async getRegistrationOpen({commit}){
      try {
        commit('setLoading', true)
        let response = await api.get('/preevent/ping')
        let open = response.data['coding_class_registration_open']
        commit('setRegistrationOpen', !!open)
      } catch (e) {
          commit('addError', e)
      } finally {
          commit('setLoading', false)
      }
    },
    async getRegistrationData({ commit }) {
      try {
        commit('setLoading', true)
        commit('clearError')
        let response = await api.get('/preevent/codingclass')
        commit('setRegistrationData', response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async register({commit}, data) {
      try {
        commit('setLoading', true);
        commit('clearError');
        let birthday = data.birthday;
        let school = data.school;
        let domicile = data.domicile;
        let grade = data.grade;
        let response = await api.post('/preevent/codingclass',{
          birthday, school, domicile, grade
        })
      } catch(e) {
          console.log(e);
          commit('addError', e);
      } finally {
          commit('setLoading', false)
      }

    }
  }
}

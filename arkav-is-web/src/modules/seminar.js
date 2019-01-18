import api from '../api'

export default {
  namespaced: true,
  state: {
    errors: [],
    success: false,
    loading: false,
    isOpen: false,
    configuration: {},
    registrationData: [],
    quiz: {},
  },
  mutations: {
    addError(state, message) {
      state.errors.push(message + '')
    },
    clearError(state) {
      state.errors = []
    },
    setSuccess(state, isSuccess) {
      state.success = isSuccess;
    },
    setLoading(state, isLoading) {
      state.loading = isLoading
    },
    setRegistrationData(state, data) {
      state.registrationData = data
    },
    setRegistrationOpen(state, status){
      state.isOpen = status
    },
    setQuiz(state, data){
      state.quiz = data
    },
    setSeminarConfiguration(state, data) {
        state.configuration = data
    }
  },
  actions: {
    async getRegistrationOpen({commit}){
      try {
        commit('setLoading', true)
        let response = await api.get('/seminar/ping')
        console.log(response)
        let open = response.data['is_registration_open']
        console.log(open)
      commit('setRegistrationOpen', open)
      } catch (e) {
          commit('addError', e)
      } finally {
          commit('setLoading', false)
      }
    },
    async getConfiguration({commit}){
      try {
        commit('setLoading', true)
        let response = await api.get('/seminar/configuration')
        console.log(response)
        let data = response.data
        console.log(data)
      commit('setSeminarConfiguration', data)
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
        let response = await api.get('/seminar/register')
        commit('setRegistrationData', response.data)
          console.log(response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async register({commit}, data) {
      try {
        commit('setSuccess', false);
        commit('setLoading', true);
        commit('clearError');

        await api.post('/seminar/register/',data);
        commit('setSuccess', true);
          location.reload();
      } catch(e) {
          console.log(e);
          if(e.response)
          commit('addError', e.response.data);
          else
          commit('addError', e)
      } finally {
          commit('setLoading', false)
      }

    },
     async uploadPaymentReceipt({commit}, data) {
      try {
        commit('setSuccess', false);
        commit('setLoading', true);
        commit('clearError');

        await api.post('/seminar/pay/',{payment_receipt: data});
        commit('setSuccess', true);
          location.reload();
      } catch(e) {
          console.log(e);
          if(e.response)
          commit('addError', e.response.data);
          else
          commit('addError', e)
      } finally {
          commit('setLoading', false)
      }

    },


  }
}

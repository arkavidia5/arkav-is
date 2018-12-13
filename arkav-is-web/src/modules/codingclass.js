import api from '../api'

export default {
  namespaced: true,
  state: {
    errors: [],
    success: false,
    loading: false,
    isOpen: false,
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
    }
  },
  actions: {
    async getRegistrationOpen({commit}){
      try {
        commit('setLoading', true)
        let response = await api.get('/preevent/ping')
        console.log(response)
        let open = response.data['coding_class_registration_open']
        console.log(open)
          commit('setRegistrationOpen', open)
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
        commit('setSuccess', false);
        commit('setLoading', true);
        commit('clearError');
        let birthday = data.birthday;
        let school = data.school;
        let domicile = data.domicile;
        let grade = data.grade;
        await api.post('/preevent/codingclass',{
          birthday, school, domicile, grade
        });

        commit('setSuccess', true);
          location.reload();
      } catch(e) {
          console.log(e);
          commit('addError', e);
      } finally {
          commit('setLoading', false)
      }

    },
    async  getQuiz({commit}) {
      try {
        commit('setLoading', true);
        commit('clearError');
        let response = await api.get('/quiz/coding-class/latest')
        commit('setQuiz', response.data);
      } catch(e) {
        commit('addError', e);
      } finally {
        commit('setLoading', false);
      }
    },
    async quickSave({commit}, data) {
      try {
        await api.post('/quiz/coding-class/latest/quicksave', data)
      } catch (e) {
        console.log(e)
      }
    },
    async finish({commit}, data) {
        try {
            commit('setLoading', true);
            commit('clearError');
            await api.post('/quiz/coding-class/latest/finish', data)
            location.reload()
        } catch (e) {
            commit('addError', e);
        } finally {
            commit('setLoading', false);
        }
    }
  }
}

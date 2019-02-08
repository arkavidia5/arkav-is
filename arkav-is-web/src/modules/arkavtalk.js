import api from '../api'

export default {
  namespaced: true,
  state: {
    errors: [],
    success: false,
    loading: false,
    authorized: false,
    configuration: {},
    userData: {},
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
    setAuthorized(state, authorized) {
        state.authorized = authorized
    },
    setUserData(state, data) {
      state.userData = data
    },

  },
  actions: {
    async ping({commit}) {
        console.log('Pinging server...')
        try {
            commit('setLoading', true)
            let response = await api.get('/seminar/gate/')
            commit('setAuthorized', response.data)
        }
        catch (e) {
            console.log(e)
        }
        finally {
            commit('setLoading', false)
        }
    },
    async checkUser({commit}, data){
        try {
            commit('clearError')
            commit('setLoading', true)

            let response = await api.post('/seminar/gate/', data)
            if(response.data.error) {
                throw Error(response.data.message)
            } else {
                console.log(response.data)
                commit('setUserData', response.data)
            }
        }
        catch (e) {
            commit('addError', e.message)
        }
        finally {
            commit('setLoading', false)
        }
    }
  }

}

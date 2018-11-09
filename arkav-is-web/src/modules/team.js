import api from '../api'

export default {
  namespaced: true,
  state: {
    errors: [],
    loading: false,
    team: '',
    saving: false,
  },
  mutations: {
    addError(state, message) {
      state.errors.push(message + '')
    },
    setTeam(state, team) {
      state.team = team
    },
    clearError(state) {
      state.errors = []
    },
    setLoading(state, isLoading) {
      state.loading = isLoading
    },
    setSaving(state, isSaving) {
      state.saving = isSaving
    }
  },
  actions: {
    async submitTeam({ commit }, { router, competition_id, name, category, institution }) {
      try {
        commit('setLoading', true)
        commit('clearError')
        if (!competition_id || !name || !category || !institution) {
            throw 'Pastikan seluruh data terisi'
        }

        let response = await api.post('/competitions/register-team/', { competition_id, name, category, institution })
        router.push({ name: 'team', params: { id: response.data.id } })

      } catch (err) {
          if (err.response) {
              commit('addError', err.response.data)
          } else {
            commit('addError', err)
          }
      } finally {
        commit('setLoading', false)
      }
    },
    async getTeam({ commit }, { team_id }) {
      try {
        commit('setLoading', true)
        let response  = await api.get('/competitions/teams/' + team_id + '/')
        commit('setTeam', response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async editTeam({ commit }, { team_id, name, institution }) {
      try {
        commit('setLoading', true)
        let response = await api.patch('/competitions/teams/' + team_id + '/', { name, institution })
        commit('setTeam', response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async deleteTeam({ commit }, { team_id, router }) {
      try {
        commit('setLoading', true)
        await api.delete('/competitions/teams/' + team_id + '/')
        router.push({ name: 'dashboard' })
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async setTeamLeader({ commit }, { team_id, email }) {
      try {
        commit('setLoading', true)
        let response = await api.patch('/competitions/teams/' + team_id + '/', { team_leader_email: email })
        commit('setTeam', response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async addTeamMember({ commit }, { team_id, full_name, email }) {
      try {
        commit('setLoading', true)
        await api.post('/competitions/teams/' + team_id + '/members/', { full_name, email })
        let response = await api.get('/competitions/teams/' + team_id + '/')
        commit('setTeam', response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async removeTeamMember({ commit }, { team_id, team_member_id }) {
      try {
        commit('setLoading', true)
        await api.delete('/competitions/teams/' + team_id + '/members/' + team_member_id + '/')
        let response = await api.get('/competitions/teams/' + team_id + '/')
        commit('setTeam', response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setLoading', false)
      }
    },
    async submitTask({commit}, {task, data}) {
      try {
        commit('setSaving', true)
        let team = this.state.team.team
        if(task.widget == 'file_upload') {
          let formData = new FormData();
          formData.append('file' , data);
          formData.append('description', "File for " + task.name + " from team " + team.name)
          let file_response = await api.post('upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          data = file_response.data.id
        }
        let postData = {
            "team_id": team.id,
            "response": data
        }
        await api.post('competitions/teams/' + team.id + '/tasks/' + task.id + '/', postData)
        let response = await api.get('/competitions/teams/' + team.id + '/')
        commit('setTeam', response.data)
      } catch (err) {
        commit('addError', err)
      } finally {
        commit('setSaving', false)
      }
    }
  }
}

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
    async submitTeam({ commit }, {router, competition, name, category, school, members}) {
      try {
        commit('setLoading', true)
        commit('clearError')
        // console.log(!competition, !name, !category, !school, !members)
        if(!competition || !name || !category || !school || !members) {
            throw 'Pastikan seluruh data terisi'
        }
        let categories = competition.categories.map(a => a.name)
        if(!(categories.includes(category))) {
            throw 'Kategori tidak sesuai'
        }
        if(members.length < competition.min_team_members || members.length > competition.max_team_members) {
            throw 'Jumlah peserta tidak sesuai'
        }
        members.forEach((member) => {
            if(!member.name || !member.email || !(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(member.email))) {
                throw 'Pastikan seluruh data valid'
            }
        });
        let postData = {
            competition_id: competition.id,
            team_name: name,
            team_category: category,
            team_school: school,
            members: members
        };
        let response = await api.post('/competitions/register-team/', postData, {ignoreUnauthorizedError: false});
        router.push({name: 'dashboard'})
      } catch (err) {
          if(err.response) {
              commit('addError', err.response.data)
          } else {
            commit('addError', err)
          }
        
      } finally {
        commit('setLoading', false)
      }
    },
    async getTeam({commit}, {team_id}) {
        try {
            commit('setLoading', true)

            let response  = await api.get('/competitions/teams/'+team_id+'/');
            commit('setTeam', response.data)
        } catch (err) {
           commit('addError',err)
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
                formData.append('description', "File for "+ task.name +" from team " + team.name)
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
            let response = await api.post('competitions/teams/'+team.id+'/tasks/'+task.id+'/', postData)
            location.reload(true)
        } catch (err) {
            console.log(err)
            commit('addError', err)
        } finally {
            commit('setSaving', false)
        }
    }
  }
}

import api from "../api";


export default {
    namespaced: true,
    state: {
        competitions: {}
    },
    mutations: {
        setCompetition(state, competitions) {
            state.competitions = competitions
        }
    },
    actions: {
        async fetch_competitions ({commit}) {
            let result = await api.get('competitions/')
            console.log(result)
            commit('setCompetition', result.data)   
        }
    }
}

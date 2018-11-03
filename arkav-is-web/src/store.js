import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import competition from './modules/competition'
import team from './modules/team'
import teamControl from './modules/team'
Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    auth,
    competition,
    team,
    teamControl
  }
})

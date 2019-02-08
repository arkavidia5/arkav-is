import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import competition from './modules/competition'
import codingclass from './modules/codingclass'
import team from './modules/team'
import seminar from './modules/seminar'
import arkavtalk from './modules/arkavtalk'
Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    auth,
    competition,
    team,
    codingclass,
    seminar,
      arkavtalk
  }
})

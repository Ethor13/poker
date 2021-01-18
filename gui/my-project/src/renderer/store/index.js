import Vue from 'vue'
import Vuex from 'vuex'

// import { createPersistedState } from 'vuex-electron'

// import modules from './modules'
import gameState from './modules/gameState'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    gameState
  },
  plugins: [
    // createPersistedState()
    // createSharedMutations()
  ],
  strict: process.env.NODE_ENV !== 'production'
})

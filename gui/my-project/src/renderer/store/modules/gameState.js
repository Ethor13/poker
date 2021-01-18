const tableState = {
  pov: -1,
  betSize: 0,
  colors: ['#3D9970', '#0074D9', 'lightcoral', '#001f3f', '#39CCCC', '#F012BE', '#FF851B', '#FF4136']
}

const initGameStateTemplate = {
  players: [null, null, null, null, null, null, null, null],
  blinds: [null, null],
  stack: null,
  dealer: -1
}

const initGameState = initGameStateTemplate

const gameStateTemplate = {
  max_players: 8,
  players: [null, null, null, null, null, null, null, null],
  deck: null,
  dealer: -1,
  sb: -1,
  bb: -1,
  blinds: [1, 2],
  board: [],
  pot: 0,
  onTable: 0,
  action_order: [],
  action_index: -1,
  turn: -1,
  valid_moves: [],
  valid_raise_amts: [0, 0],
  to_go: 0,
  stage: 0,
  last_decision: 'Start'
}

const gameState = gameStateTemplate

const state = {
  tableState,
  gameState,
  initGameState
}

const getters = {
  tableState: (state) => state.tableState,
  gameState: (state) => state.gameState,
  initGameState: (state) => state.initGameState
}

const actions = {
  resetGameState ({ commit }) {
    commit('setGameState', gameStateTemplate)
  },
  sendDecision ({ commit }, {action, amount, init}) {
    const python = require('python-shell')

    if (init) {
      const initBlinds = this.getters.initGameState.blinds
      const initStack = this.getters.initGameState.stack

      // set blinds and stack in initGameState
      if (initBlinds[0] == null) {
        if (initBlinds[1] == null) {
          if (initStack == null) {
            commit('setInitSB', 1)
            commit('setInitBB', 2)
            commit('setInitStack', 100)
          } else {
            const bb = Math.ceil(initStack / 50)
            const sb = Math.ceil(bb / 2)
            commit('setInitSB', sb)
            commit('setInitBB', bb)
          }
        } else {
          const sb = Math.ceil(initBlinds[1] / 2)
          commit('setInitSB', sb)
          if (initStack == null) {
            const stack = initBlinds[1] * 50
            commit('setInitStack', stack)
          }
        }
      } else {
        if (initBlinds[1] == null) {
          const bb = initBlinds[0] * 2
          commit('setInitBB', bb)
          if (initStack == null) commit('setInitStack', bb * 50)
        } else {
          if (initStack == null) commit('setInitStack', initBlinds[1] * 50)
        }
      }

      if (initStack == null) {
        const stack = this.getters.initGameState.stack
        for (let i = 0; i < 8; i++) {
          const p = this.getters.initGameState.players[i]
          if (p != null) {
            commit('setInitPlayer', { index: i, player_info: { name: p.name, stack: stack, cards: [] } })
          }
        }
      }

      let tempGameState = { ...this.getters.gameState }
      tempGameState.players = this.getters.initGameState.players
      tempGameState.dealer = this.getters.initGameState.dealer
      tempGameState.blinds = this.getters.initGameState.blinds

      commit('setGameState', tempGameState)

      if (this.getters.tableState.pov === -1) {
        for (let i = 0; i < 8; i++) {
          if (this.getters.gameState.players[i] != null) {
            commit('setPOV', i)
            break
          }
        }
      }

      commit('setInitGameState', initGameStateTemplate)
    }

    let decision = action

    const min = this.getters.gameState.valid_raise_amts[0]

    if (decision === 'Raise') {
      if (amount == null || amount < min) {
        const betText = document.querySelector('#bet-text')
        commit('setBetSize', min)
        betText.style.borderColor = 'red'
        betText.style.color = 'red'
        setTimeout(() => {
          betText.style.borderColor = 'white'
          betText.style.color = 'white'
        }, 300)
        return
      } else {
        decision = 'Raise ' + amount
      }
    }

    const formattedGameState = JSON.stringify(this.getters.gameState)
    console.log(formattedGameState)

    var options = {
      scriptPath: 'C:/Users/ethor/OneDrive - Cornell University/PythonDocs/poker/engine',
      args: [formattedGameState, decision]
    }

    var test = python.PythonShell.run('vue_interface.py', options, function (err, results) {
      if (err) {
        console.log(err)
        throw err
      }
    })

    test.on('message', function (message) {
      console.log(message)
      const newGameState = JSON.parse(message)
      commit('setGameState', newGameState)
      commit('setBetSize', newGameState.valid_raise_amts[0])
    })
  },
  updateBetSize ({ commit }, amount) {
    const max = this.getters.gameState.valid_raise_amts[1]
    if (amount < 0) {
      commit('setBetSize', 0)
    } else if (amount > max) {
      commit('setBetSize', max)
      const betText = document.querySelector('#bet-text')
      betText.style.borderColor = 'red'
      betText.style.color = 'red'
      setTimeout(() => { betText.style.borderColor = 'white'; betText.style.color = 'white' }, 300)
    }
  },
  updateInitStack ({ commit }) {
    const amount = parseInt(document.querySelector('#starting-stack').value)
    if (!isNaN(amount)) {
      commit('setInitStack', amount)
      for (let i = 0; i < this.getters.initGameState.players.length; i++) {
        let player = this.getters.initGameState.players[i]
        if (player != null) {
          commit('setInitPlayer', {index: i, player_info: { name: player.name, stack: amount, cards: [] }})
        }
      }
    }
  }
}

const mutations = {
  setGameState: (state, gameState) => (state.gameState = gameState),
  setBetSize: (state, betSize) => (state.tableState.betSize = betSize),
  setInitSB: (state, sb) => (state.initGameState.blinds = [sb, state.initGameState.blinds[1]]),
  setInitBB: (state, bb) => (state.initGameState.blinds = [state.initGameState.blinds[0], bb]),
  setInitStack: (state, stack) => (state.initGameState.stack = stack),
  setInitDealer: (state, dealer) => (state.initGameState.dealer = dealer),
  setInitPlayer: (state, obj) => (state.initGameState.players =
    state.initGameState.players.slice(0, obj.index).concat([obj.player_info], state.initGameState.players.slice(obj.index + 1))),
  setPOV: (state, pov) => (state.tableState.pov = pov),
  setInitGameState: (state, initGameState) => (state.initGameState = initGameState)
}

export default {
  state,
  getters,
  actions,
  mutations
}

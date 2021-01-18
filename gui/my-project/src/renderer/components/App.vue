<template>
  <div class="game-container">
    <router-link to="/" class="set-up-router"></router-link>
    <div class="table">
      <div class="card-place">
        <Card v-for="(card, i) in gameState.board" :card="card" :key="i" />
      </div>
      <div class="pot">
        <div id="collected">{{ gameState.pot }}</div>
        <div id="uncollected">{{ gameState.onTable }}</div>
      </div>
      <div class="players">
        <Player
          v-for="(player, index) in gameState.players"
          class="player"
          :class="['player-' + (index + 1)]"
          :key="index"
          :player="player"
          :index="index"
        />
      </div>
    </div>
    <div class="decisions" :color="tableState.colors[gameState.turn]">
      <div class="raise-container" v-if="gameState.valid_moves.includes('Raise')">
        <div class="bet-sizing">
          <input
            type="number"
            id="bet-text"
            v-on:input="updateBetSize(amount)"
            v-model="amount"
            :max="gameState.valid_raise_amts[1]"
          />
          <input
            class="rs-range"
            id="rs-range-line"
            type="range"
            step="1"
            v-model="amount"
            :min="gameState.valid_raise_amts[0]"
            :max="gameState.valid_raise_amts[1]"
          />
        </div>
        <button id="button-1" v-on:click="sendDecision({action: 'Raise', amount: amount, init: false })">Raise</button>
      </div>
      <button id="button-2" v-if="gameState.valid_moves.includes('Call')" v-on:click="sendDecision({action: 'Call', amount: null, init: false })">Call</button>
      <button id="button-3" v-if="gameState.valid_moves.length > 0" v-on:click="sendDecision({action: gameState.valid_moves[0], amount: null, init: false })">{{ gameState.valid_moves[0] }}</button>
    </div>
    <div class="game-info">
      <div class="blinds">{{ gameState.blinds[0] }}/{{ gameState.blinds[1] }}</div>
    </div>
  </div>
</template>

<script>
import Card from './Card.vue'
import Player from './Player.vue'
import { mapGetters, mapActions } from 'vuex'
import less from 'less'

export default {
  name: 'App',
  components: {
    Card,
    Player
  },
  computed: {
    ...mapGetters(['tableState', 'gameState']),
    amount: {
      set (amount) {
        this.$store.commit('setBetSize', amount)
      },
      get () {
        return this.tableState.betSize
      }
    }
  },
  methods: {
    ...mapActions(['sendDecision', 'updateBetSize'])
  },
  created () {
    this.sendDecision({ action: 'Start', amount: null, init: true })
  },
  mounted () {
    const decisions = document.querySelector('.decisions')

    function changeButtonColors () {
      let color = decisions.getAttribute('color')
      if (color !== null) {
        less.modifyVars({
          '@button-color': color
        })
      }
    }

    try {
      var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
          if (mutation.type === 'attributes') {
            changeButtonColors()
          }
        })
      })

      observer.observe(decisions, {
        attributes: true // configure it to listen to attribute changes
      })
    } catch (error) {
      // do nothing
    }
  }
}
</script>
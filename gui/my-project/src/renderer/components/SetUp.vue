<template>
  <div class="game-container">
    <div class="table">
      <div class="card-place">
      </div>
      <div class="players">
        <SetUpPlayer
          v-for="index in 8"
          class="player"
          :class="['player-' + index]"
          :key="index"
          :index="index"
        />
      </div>
    </div>
    <div class="game-info">
      <div class="blinds">
        <input type="number" placeholder="SB" id="small-blind" v-on:input="updateSB">
        <p>/</p>
        <input type="number" placeholder="BB" id="big-blind" v-on:input="updateBB">
      </div>
      <div class="starting-stack">
        <input type="number" placeholder="Stack" id="starting-stack" v-on:input="updateInitStack()">
      </div>
      <div class="dealer">
        <input type="number" placeholder="Dealer" min="1" max="8" id="dealer" v-on:input="updateDealer">
      </div>
      <div class="pov">
        <input type="number" placeholder="POV" min="1" max="8" id="pov" v-on:input="updatePOV">
      </div>
    </div>
    <router-link to="/app" class="start-button" v-if="showRouter"></router-link>
  </div>
</template>


<script>
import SetUpPlayer from './SetUpPlayer.vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'SetUp',
  components: {
    SetUpPlayer
  },
  computed: {
    ...mapGetters(['initGameState', 'tableState']),
    showRouter () {
      let count = 0
      let player
      for (player of this.initGameState.players) {
        if (player != null) count++
      }
      return count >= 2
    }
  },
  methods: {
    ...mapActions(['updateInitStack', 'resetGameState']),
    updateSB () {
      let sb = parseInt(document.querySelector('#small-blind').value)
      if (isNaN(sb)) sb = null
      this.$store.commit('setInitSB', sb)
    },
    updateBB () {
      let bb = parseInt(document.querySelector('#big-blind').value)
      if (isNaN(bb)) bb = null
      this.$store.commit('setInitBB', bb)
    },
    updateStack () {
      let stack = parseInt(document.querySelector('#starting-stack').value)
      if (isNaN(stack)) stack = null
      this.$store.commit('setInitStack', stack)
    },
    updateDealer () {
      let dealer = parseInt(document.querySelector('#dealer').value)
      if (isNaN(dealer)) dealer = null
      this.$store.commit('setInitDealer', dealer)
    },
    updatePOV () {
      let pov = parseInt(document.querySelector('#pov').value)
      if (isNaN(pov)) pov = 0
      this.$store.commit('setPOV', pov)
    }
  },
  created () {
    this.resetGameState()
  }
}
</script>

<style lang='less' scoped>
  @import './../../../static/setup.less';
</style>
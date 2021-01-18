<template>
  <div class="player">
    <label class="switch" :class="['switch-' + index]">
      <input type="checkbox" v-model="playing" v-on:click="updatePlaying" checked>
      <span class="slider"></span>
    </label>
    <div class="stack" v-if="playing">
      <div class="stack-value" v-if="initGameState.stack != null && initGameState.stack > 0">{{ initGameState.stack }}</div>
      <div
        class="chips v-10"
        v-if="initGameState.stack >= 10"
      ></div>
      <div
        class="chips v-2"
        v-if="
          initGameState.stack >= 2 &&
          initGameState.stack != 10 &&
          initGameState.stack != 11
        "
      ></div>
      <div
        class="chips v-1"
        v-if="
          initGameState.stack >= 1 &&
          initGameState.stack != 2 &&
          initGameState.stack != 10 &&
          initGameState.stack != 12
        "
      ></div>
    </div>
    <input class="avatar" :placeholder="'Player ' + index" type="text" v-model="name" :style="{background: playing ? tableState.colors[index - 1] : 'grey' }" v-on:input="setPlayerProfile"/>
    <div class="dealer" v-if="index === initGameState.dealer">D</div>
    <div class="pov" v-if="index === tableState.pov">P</div>
  </div>
</template>

<script>
import Card from './Card.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'SetUpPlayer',
  data () {
    return {
      name: null,
      stack: 100,
      playing: true
    }
  },
  components: {
    Card
  },
  computed: mapGetters(['initGameState', 'tableState', 'gameState']),
  props: {
    index: Number
  },
  created () {
    this.setPlayerProfile()
  },
  methods: {
    setPlayerProfile () {
      let name
      if (this.name == null) name = 'Player ' + this.index
      else name = this.name
      this.$store.commit('setInitPlayer', { index: this.index - 1, player_info: { name: name, stack: this.initGameState.stack, cards: [] } })
    },
    updatePlaying () {
      // this.playing doesn't change value until after this function is called
      if (!this.playing) this.setPlayerProfile()
      else this.$store.commit('setInitPlayer', { index: this.index - 1, player_info: null })
    }
  }
}
</script>

<style lang="less" scoped>
  @import './../../../static/setupplayer.less';
</style>
<template>
    <div class='start-container'>
        <input class="num-player-range" type="range" v-model="num_players" min="2" max="8"/>
        <div class='left-form'>

        </div>
        <div class='middle-form'>
          <div class='player-form' v-for='n in players' :key='n'>
            <input class="player_name" :placeholder="'Player ' + n" type="text" :style='[{background: tableState.colors[n - 1]}]'/>
          </div>
        </div>
        <div class='right-form'>
          <div class='cards'></div>
          <div class='stack'>
            <input class="starting-stack" type="number" value="1000">
          </div>
          <div class='chipsOnTable'></div>
          <div class='committed'></div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Start',
  data () {
    return {
      num_players: 2
    }
  },
  computed: {
    ...mapGetters(['tableState', 'gameState']),
    players () {
      let arr = []
      for (let i = 1; i <= this.num_players; i++) {
        arr.push(i)
      }
      return arr
    }
  }
}
</script>

<style lang='less' scoped>
  @import './../../../static/start.less';
</style>
<template>
  <div class="player" v-if="player != null">
    <div class="stack">
      <div class="stack-value">{{ player.stack }}</div>
      <div
        class="chips v-10"
        v-if="player.stack >= 10"
      ></div>
      <div
        class="chips v-2"
        v-if="
          player.stack >= 2 &&
          player.stack != 10 &&
          player.stack != 11
        "
      ></div>
      <div
        class="chips v-1"
        v-if="
          player.stack >= 1 &&
          player.stack != 2 &&
          player.stack != 10 &&
          player.stack != 12
        "
      ></div>
    </div>
    <div
      class="avatar"
      :style="{
        background: player.cards.length != 0 ? tableState.colors[index] : 'grey',
      }"
    >
      {{ player.name }}
    </div>
    <div class="hand">
      <Card
        v-for="(card, i) in player.cards"
        :card="card"
        :hidden="index !== tableState.pov - 1"
        :key="i"
      />
    </div>
    <div class="dealer" v-if="index === gameState.dealer">D</div>
    <div class="bet">
      <div class="bet-value" v-if="player.chipsOnTable > 0">
        {{ player.chipsOnTable }}
      </div>
      <div class="chip-10" v-if="player.chipsOnTable >= 10">
        <div
          class="chips v-10"
          v-for="(n, i) in (player.chipsOnTable / 10) | 0"
          :style="{ top: -2 + i * 5 + 'px' }"
          :key="i"
        ></div>
      </div>
      <div class="chip-2" v-if="player.chipsOnTable % 10 >= 2">
        <div
          class="chips v-2"
          v-for="(n, i) in ((player.chipsOnTable % 10) / 2) | 0"
          :style="{ top: -2 + i * 5 + 'px' }"
          :key="i"
        ></div>
      </div>
      <div class="chip-1">
        <div
          class="chips v-1"
          style="top: -2px"
          v-if="player.chipsOnTable % 2"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
import Card from './Card.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'Player',
  components: {
    Card
  },
  computed: mapGetters(['tableState', 'gameState']),
  props: {
    player: Object,
    index: Number
  }
}
</script>
<template>
  <div
    class="card"
    :class="['figures-' + card.f, 'values-' + card.v]"
    v-if="!hidden"
  >
    <h1>{{ card.v }}</h1>
    <div class="figures" :class="card.f"></div>
    <h1>{{ card.v }}</h1>
  </div>
  <div class="card" v-else>
    <img
      src="static/bicycle-card.jpg"
      class="card-cover"
    />
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    card: Object,
    hidden: Boolean
  }
}
</script>
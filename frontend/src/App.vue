<template>
  <div id="app">
    <h1>Trade Statistics</h1>
    <TradeStatistics />
    <TradeDetails />
  </div>
</template>

<script>
import TradeStatistics from './components/TradeStatistics.vue';
import TradeDetails from './components/TradeDetails.vue';

export default {
  components: {
    TradeStatistics,
    TradeDetails
  }
};
</script>

<style scoped></style>

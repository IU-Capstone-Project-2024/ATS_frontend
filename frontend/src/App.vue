<template>
  <div id="app">
    <DecisionDisplay />
    <RealTimeChart />
    <TradeStatistics />
    <TradeDetails />
  </div>
</template>

<script>
import DecisionDisplay from './components/DecisionDisplay.vue'
import RealTimeChart from './components/RealTimeChart.vue';
import TradeStatistics from './components/TradeStatistics.vue';
import TradeDetails from './components/TradeDetails.vue';

export default {
  components: {
    TradeStatistics,
    TradeDetails,
    RealTimeChart,
    DecisionDisplay
  }
};
</script>

<style scoped></style>

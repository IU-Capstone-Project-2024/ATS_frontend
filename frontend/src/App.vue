<template>
  <div id="app">
    <DecisionDisplay />
    <div class="charts-row">
      <!-- TODO: different chart with different parameters? Can be divided in separate modules btw-->
      <RealTimeChart />
      <RealTimeChart />
    </div>
    <TradeStatistics />
    <TradeDetails />
  </div>
</template>

<script>
import TradeStatistics from './components/TradeStatistics.vue';
import TradeDetails from './components/TradeDetails.vue';
import RealTimeChart from './components/RealTimeChart.vue';
import DecisionDisplay from './components/DecisionDisplay.vue';

export default {
  components: {
    TradeStatistics,
    TradeDetails,
    RealTimeChart,
    DecisionDisplay
  }
};
</script>

<style scoped>
#app {
  background-color: #f0f0f0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  padding: 20px;
}

.charts-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.charts-row>div {
  flex: 1;
  margin-right: 20px;
}

.charts-row>div:last-child {
  margin-right: 0;
}
</style>

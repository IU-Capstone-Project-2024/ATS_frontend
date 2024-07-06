<template>
  <div id="app">
    <h1>Trade Statistics</h1>
    <div v-if="trades.length">
      <table>
        <tr>
          <th>ID</th>
          <th>Trade Type</th>
          <th>Symbol</th>
          <th>Quantity</th>
          <th>Price</th>
          <th>Timestamp</th>
        </tr>
        <tr v-for="trade in trades" :key="trade.id"
          :class="{ 'buy': trade.trade_type === 'Buy', 'sell': trade.trade_type === 'Sell' }">

          <td>{{ trade.id }}</td>
          <td>{{ trade.trade_type }}</td>
          <td>{{ trade.symbol }}</td>
          <td>{{ trade.quantity }}</td>
          <td>{{ trade.price }}</td>
          <td>{{ trade.timestamp }}</td>
        </tr>
      </table>
    </div>
    <div v-else>
      Loading trades...
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const trades = ref([]);

    onMounted(() => {
      console.log('Mounted');
      axios.get('http://localhost:5000/api/trades')
        .then(response => {
          console.log('API response:', response.data);
          trades.value = response.data.map(trade => ({
            id: trade[0],
            trade_type: trade[1],
            symbol: trade[2],
            quantity: trade[3],
            price: trade[4],
            timestamp: trade[5]
          }));
        })
        .catch(error => {
          console.error("There was an error!", error);
        });

    });

    return { trades };
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.buy {
  background-color: lightgreen;
}

.sell {
  background-color: tomato;
}
</style>

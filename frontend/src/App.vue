<<template>
  <div id="app">
    <h1>Trade Statistics</h1>
    <div v-if="stats">
      <h2>Statistics</h2>
      <ul>
        <li>Total Buys: {{ stats.total_buys }}</li>
        <li>Total Sells: {{ stats.total_sells }}</li>
        <li>Average Buy Price: {{ stats.avg_buy_price.toFixed(2) }}</li>
        <li>Average Sell Price: {{ stats.avg_sell_price.toFixed(2) }}</li>
        <li>Total Profit: {{ stats.total_profit.toFixed(2) }}</li>
      </ul>
    </div>
    <div v-if="trades.length">
      <h2>Trade Details</h2>
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
      const stats = ref(null);

      onMounted(() => {
        console.log('Mounted');
        axios.get('http://localhost:5000/api/trades')
          .then(response => {
            console.log('Trades API response:', response.data);
            trades.value = response.data;
          })
          .catch(error => {
            console.error("There was an error!", error);
          });

        axios.get('http://localhost:5000/api/stats')
          .then(response => {
            console.log('Stats API response:', response.data);
            stats.value = response.data;
          })
          .catch(error => {
            console.error("There was an error!", error);
          });
      });

      return { trades, stats };
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
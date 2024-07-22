<template>
    <div class="trade-details">
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
    name: 'TradeDetails',
    setup() {
        const trades = ref([]);

        const fetchTrades = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/trades');
                trades.value = response.data;
            } catch (error) {
                console.error("There was an error!", error);
            }
        };

        onMounted(() => {
            fetchTrades();
            setInterval(fetchTrades, 1000)
        });

        return { trades };
    }
};
</script>

<style scoped>
.trade-details {
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

.trade-details h2 {
    color: #2c3e50;
}

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
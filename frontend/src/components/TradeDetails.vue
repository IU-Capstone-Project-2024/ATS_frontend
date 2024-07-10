<template>
    <div>
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

        const fetchTrades = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/trades');
                console.log('Trades API response:', response.data);
                trades.value = response.data;
            } catch (error) {
                console.error("There was an error!", error);
            }
        };

        onMounted(() => {
            fetchTrades();
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
<template>
    <div class="trade-statistics" v-if="stats">
        <h2>Statistics</h2>
        <ul>
            <li>Total Buys: {{ stats.total_buys }} BTC</li>
            <li>Total Sells: {{ stats.total_sells }} BTC</li>
            <li>Average Buy Price: {{ stats.avg_buy_price.toFixed(2) }}$</li>
            <li>Average Sell Price: {{ stats.avg_sell_price.toFixed(2) }}$</li>
            <li>Total Profit: {{ stats.total_profit.toFixed(2) }}$</li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
    name: 'TradeStatistics',
    setup() {
        const stats = ref(null);

        const fetchStats = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/stats');
                stats.value = response.data;
            } catch (error) {
                console.error("There was an error!", error);
            }
        };

        onMounted(() => {
            fetchStats();
            setInterval(fetchStats, 5000) // TODO: test update every second
        });

        return { stats };
    }
};
</script>

<style scoped>
.trade-statistics {
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    text-align: center;
}

.trade-statistics h2 {
    color: #2c3e50;
}

.trade-statistics ul {
    list-style-type: none;
    padding: 0;
}

.trade-statistics li {
    margin: 5px 0;
}
</style>
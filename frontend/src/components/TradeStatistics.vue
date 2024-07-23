<template>
    <div class="trade-statistics" v-if="stats">
        <h2>Statistics</h2>
        <ul>
            <li>
                <span class="label">Total Buys: </span>
                <span class="value red">{{ stats.total_buys }} BTC</span>
            </li>
            <li>
                <span class="label">Total Sells: </span>
                <span class="value green">{{ stats.total_sells }} BTC</span>
            </li>
            <li>
                <span class="label">Average Buy Price: </span>
                <span class="value black">{{ stats.avg_buy_price.toFixed(2) }}$</span>
            </li>
            <li>
                <span class="label">Average Sell Price: </span>
                <span class="value black">{{ stats.avg_sell_price.toFixed(2) }}$</span>
            </li>
            <li>
                <span class="label">Total Profit: </span>
                <span class="value green">{{ stats.total_profit.toFixed(2) }}$</span>
            </li>
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
            setInterval(fetchStats, 5000); // Update every 5 seconds
        });

        return { stats };
    }
};
</script>

<style scoped>
.trade-statistics {
    background-color: #fff;
    padding: 0px;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    text-align: center;
}

.trade-statistics h2 {
    color: #2c3e50;
    font-size: 2em;
    margin-bottom: 0px;
}

.trade-statistics ul {
    list-style-type: none;
    padding: 0;
}

.trade-statistics li {
    margin: 0px 0;
    font-size: 1.2em;
}

.trade-statistics .label {
    font-weight: bold;
    color: #34495e;
}

.trade-statistics .value {
    font-weight: bold;
    font-size: 1.5em;
}

.trade-statistics .value.red {
    color: #e74c3c;
}

.trade-statistics .value.green {
    color: #27ae60;
}

.trade-statistics .value.black {
    color: #2c3e50;
}
</style>

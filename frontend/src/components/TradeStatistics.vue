<template>
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
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
    setup() {
        const stats = ref(null);

        const fetchStats = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/stats');
                console.log('Stats API response:', response.data);
                stats.value = response.data;
            } catch (error) {
                console.error("There was an error!", error);
            }
        };

        onMounted(() => {
            fetchStats();
        });

        return { stats };
    }
};
</script>

<style scoped>
/* Add any styles specific to TradeStatistics.vue */
</style>
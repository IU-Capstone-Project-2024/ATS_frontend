<template>
    <div class="chart-container">
        <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import ApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
    name: 'ProfitChart',
    components: {
        apexchart: ApexCharts,
    },
    setup() {
        const MAX_POINTS = 1000; // Limit the number of points displayed on the chart
        const initialBalance = 1000; // Starting balance in USD
        const series = ref([{
            name: 'Profit Over Time',
            data: [] // Start with empty data
        }]);

        const chartOptions = ref({
            chart: {
                id: 'profit',
                animations: {
                    enabled: true,
                    easing: 'linear',
                    dynamicAnimation: {
                        speed: 1
                    }
                },
                toolbar: {
                    show: false
                },
                zoom: {
                    enabled: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            title: {
                text: 'Profit Over Time',
                align: 'left'
            },
            markers: {
                size: 0
            },
            xaxis: {
                type: 'datetime'
            },
            yaxis: {
                labels: {
                    formatter: function (value) {
                        return `$${value.toFixed(2)}`;
                    }
                }
            },
            legend: {
                show: false
            },
            tooltip: {
                x: {
                    format: 'dd MMM yyyy HH:mm:ss'
                }
            }
        });

        const fetchData = async () => {
            try {
                const [tradesResponse, priceResponse] = await Promise.all([
                    axios.get('http://localhost:5000/api/trades'),
                    axios.get('http://localhost:5000/api/btc_price')
                ]);

                const trades = tradesResponse.data;
                const btcPrice = priceResponse.data.price;

                let balance = initialBalance;
                let btcHoldings = 0;
                const newData = trades.reduce((acc, trade) => {
                    const timestamp = new Date(trade.timestamp).getTime();
                    const quantity = parseFloat(trade.quantity);
                    const price = parseFloat(trade.price);

                    if (trade.trade_type.toLowerCase() === 'buy') {
                        btcHoldings += quantity;
                        balance -= quantity * price;
                    } else if (trade.trade_type.toLowerCase() === 'sell') {
                        btcHoldings -= quantity;
                        balance += quantity * price;

                        const currentProfit = (balance + btcHoldings * btcPrice) - initialBalance;
                        acc.push({
                            x: timestamp,
                            y: currentProfit
                        });
                    }

                    return acc;
                }, []);

                // Limit the number of points
                series.value[0].data = newData.slice(-MAX_POINTS);
            } catch (error) {
                console.error("There was an error fetching the data!", error);
            }
        };

        onMounted(() => {
            fetchData();
            setInterval(fetchData, 15000); // Update data every 15 seconds
        });

        return {
            series,
            chartOptions
        };
    },
};
</script>

<style scoped>
.chart-container {
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>

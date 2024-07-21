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
    name: 'BalanceChart',
    components: {
        apexchart: ApexCharts,
    },
    setup() {
        const MAX_POINTS = 100; // Limit the number of points displayed on the chart
        const initialBalance = 1000; // Starting balance
        const series = ref([{
            name: 'Balance Over Time',
            data: [] // Start with empty data
        }]);

        const chartOptions = ref({
            chart: {
                id: 'balance',
                animations: {
                    enabled: true,
                    easing: 'linear',
                    dynamicAnimation: {
                        speed: 1000
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
                text: 'Balance Over Time',
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
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    inverseColors: false,
                    opacityFrom: 1,
                    opacityTo: 1,
                    stops: []
                }
            },
            colors: ['#00E396'] // Set initial color
        });

        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/trades');
                const trades = response.data;

                let balance = initialBalance;
                const initialTimestamp = new Date(trades[0].timestamp).getTime() - (60 * 1000);
                const newData = trades.map(trade => {
                    const timestamp = new Date(trade.timestamp).getTime();
                    const quantity = parseFloat(trade.quantity);
                    const price = parseFloat(trade.price);

                    if (trade.trade_type.toLowerCase() === 'buy') {
                        balance -= quantity * price;
                    } else if (trade.trade_type.toLowerCase() === 'sell') {
                        balance += quantity * price;
                    }

                    return {
                        x: timestamp,
                        y: balance
                    };
                });

                // Prepend the initial balance point and limit the number of points
                series.value[0].data = [{ x: initialTimestamp, y: initialBalance }, ...newData].slice(-MAX_POINTS);

                // Generate gradient stops
                const gradientStops = series.value[0].data.map((point, index, array) => {
                    const color = point.y >= initialBalance ? '#00E396' : '#FF4560';
                    const percentage = (index / (array.length - 1)) * 100;
                    return {
                        offset: percentage,
                        color: color,
                        opacity: 1
                    };
                });

                chartOptions.value.fill.gradient.stops = gradientStops;
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

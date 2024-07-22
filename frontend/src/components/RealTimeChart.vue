<template>
    <div class="chart-container">
        <apexchart type="scatter" height="350" :options="chartOptions" :series="series"></apexchart>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import ApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
    name: 'RealTimeChart',
    components: {
        apexchart: ApexCharts,
    },
    setup() {
        const MAX_POINTS = 800; // Limit the number of points displayed on the chart
        const series = ref([{
            name: 'Real-time Data',
            data: []
        }]);

        // Define weights for each model
        const modelWeights = {
            'Algorithms': 0.5,
            'Knife': 1,
            'Sparse': 1
        };

        const chartOptions = ref({
            chart: {
                id: 'realtime',
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
            markers: {
                size: 5, // Adjust the size of the dots as needed
                shape: 'circle',
                colors: ['#FF4560', '#00E396', '#008FFB'], // Customize marker colors
            },
            xaxis: {
                type: 'datetime'
            },
            yaxis: {
                min: -1,
                max: 1,
                tickAmount: 2,
                labels: {
                    formatter: function (value) {
                        const actionMapping = {
                            '-1': 'Sell',
                            '0': 'Hold',
                            '1': 'Buy'
                        };
                        return actionMapping[value.toString()];
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
                const response = await axios.get('http://localhost:5000/api/decisions');
                const data = response.data;

                // Aggregate data by timestamp and apply weights
                const aggregatedData = {};
                data.forEach(d => {
                    const timestamp = new Date(d.timestamp).getTime();
                    if (!aggregatedData[timestamp]) {
                        aggregatedData[timestamp] = 0;
                    }
                    aggregatedData[timestamp] += modelWeights[d.model] * d.action;
                });

                // Convert aggregated data to the desired format
                const newData = Object.keys(aggregatedData).map(timestamp => {
                    const sum = aggregatedData[timestamp];
                    let action;
                    if (sum > 0) {
                        action = 1; // Buy
                    } else if (sum < 0) {
                        action = -1; // Sell
                    } else {
                        action = 0; // Hold
                    }
                    return {
                        x: parseInt(timestamp),
                        y: action
                    };
                });

                // Append new data to the series and limit the number of points
                series.value[0].data = [...series.value[0].data, ...newData].slice(-MAX_POINTS);
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

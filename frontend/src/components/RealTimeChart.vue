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
        const MAX_POINTS = 300; // Limit the number of points displayed on the chart
        const series = ref([{
            name: 'Real-time Data',
            data: []
        }]);

        const chartOptions = ref({
            chart: {
                id: 'realtime',
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

                // Convert data to the desired format
                const newData = data.map(d => ({
                    x: new Date(d.timestamp).getTime(),
                    y: d.action
                }));

                // Append new data to the series and limit the number of points
                series.value[0].data = [...series.value[0].data, ...newData].slice(-MAX_POINTS);
            } catch (error) {
                console.error("There was an error fetching the data!", error);
            }
        };

        onMounted(() => {
            fetchData();
            setInterval(fetchData, 3000); // Update data every 15 seconds
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

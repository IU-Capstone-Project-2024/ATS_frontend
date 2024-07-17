<template>
    <div class="chart-container">
        <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
    </div>
</template>


<<script>
import { ref, onMounted } from 'vue';
import ApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
    name: 'RealTimeChart',
    components: {
        apexchart: ApexCharts,
    },
    setup() {
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
                text: 'Real-time Line Chart',
                align: 'left'
            },
            markers: {
                size: 0
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
            }
        });

        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/decisions');
                const data = response.data.map(d => ({
                    x: new Date(d.timestamp).getTime(),
                    y: d.action
                }));
                series.value = [{ name: 'Real-time Data', data }];
            } catch (error) {
                console.error("There was an error fetching the data!", error);
            }
        };

        onMounted(() => {
            fetchData();
            setInterval(fetchData, 10000); // Update data every 10 seconds
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

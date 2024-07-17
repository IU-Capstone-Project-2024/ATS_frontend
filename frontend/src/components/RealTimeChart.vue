<template>
    <div class="chart-container">
        <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import ApexCharts from 'vue3-apexcharts';

export default {
    name: 'RealTimeChart',
    components: {
        apexchart: ApexCharts,
    },
    setup() {
        const series = ref([{
            name: 'Real-time Data',
            data: Array.from({ length: 100 }, () => Math.floor(Math.random() * 100))
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
                type: 'numeric',
                range: 10
            },
            yaxis: {
                max: 100
            },
            legend: {
                show: false
            }
        });

        onMounted(() => {
            setInterval(() => {
                if (series.value[0].data.length >= 10) {
                    series.value[0].data.shift();
                }
                const newData = Math.floor(Math.random() * 100);
                series.value[0].data.push(newData);
            }, 1000);
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
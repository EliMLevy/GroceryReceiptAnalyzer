<template>
  <Bar
    id="my-chart-id"
    :options="chartOptions"
    :data="{
      labels: Object.keys(data),
      datasets: [{ data: Object.values(data) }],
    }"
  />
</template>

<script>
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  name: 'BarChart',
  components: { Bar },
  data() {
    return {
      chartData: {
        labels: ['January', 'February', 'March'],
        datasets: [{ data: [40, 20, 12] }],
      },
      chartOptions: {
        responsive: true,
        plugins: {
            legend: {
                display: false
            },
        }
      },
    };
  },

  props: {
    data: {
      type: Object,
      default: () => {
        return { "January": 4000, "February": 20, "March": 12 };
      },
    },
  },
};
</script>

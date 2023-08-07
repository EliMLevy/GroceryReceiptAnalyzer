<template>
  <LineChart
    :data="{
      labels: Object.keys(data),
      datasets: [{ data: Object.values(data) },{ data: Object.values(data).map(elem => dataMean), borderDash: [10,5], pointRadius: 0 }],
    }"
    :options="{
      responsive: true,
      plugins: {
            legend: {
                display: false
            },
        },
    }"
  />
</template>

<script lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line as LineChart } from 'vue-chartjs';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: 'App',
  components: {
    LineChart,
  },
  data() {
    return {
      chartData: {
        labels: ['January', 'February', 'March'],
        datasets: [{ data: [40, 20, 12] }],
      },
      chartConfig: {
        
        labels: [
          'January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
        ],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [40, 39, 10, 40, 39, 80, 40],
          },
        ],
      },
    };
  },
  props: {
    data: {
      type: Object,
      default: () => {return {'January':40, 'February':20, 'March':12}}
    }
  },
  computed: {

    dataMean() {
      let sum = 0;
      Object.values(this.data).forEach(elem => sum += elem);
      return sum / Object.keys(this.data).length
    }

  }
};
</script>

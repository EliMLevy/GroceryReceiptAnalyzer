<template>
  <div class="container q-ma-lg">
    <div class="row">
      <div class="col row justify-center q-ma-md">
        <div class="title text-h5">Expenses by Tag</div>
        <MyBarChart :data="byTag" ref="expensesbytagchart" />
      </div>
    </div>
    <div class="row">
      <div class="col row justify-center q-ma-md">
        <div class="title text-h5">Expenses by Week</div>
        <MyLineChart :data="byWeek" />
      </div>
    </div>
    <div class="row">
      <div class="col row justify-center q-ma-md">
        <div class="title text-h5">Top Ten Food Expenses</div>
        <MyBarChart :data="topTenFoods" />
      </div>
    </div>
    <div class="row">
      <div class="col column items-center q-ma-md">
        <div class="title text-h5">More data</div>
        <div class="container">
          <div>Total spending this month:</div>
          <div>Percent of budget remaining this month:</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import MyBarChart from 'src/components/MyBarChart.vue';
import {
  getExpensesByTag,
  getExpensesByWeek,
  getTopTenExpenses,
} from 'src/components/APICaller';
import MyLineChart from 'src/components/MyLineChart.vue';

export default defineComponent({
  components: {
    MyBarChart,
    MyLineChart,
  },

  mounted() {
    getExpensesByTag().then((result) => {
      this.byTag = result;
    });
    getExpensesByWeek().then((result) => (this.byWeek = result));
    getTopTenExpenses().then((result) => (this.topTenFoods = result));
  },

  data() {
    return {
      byTag: {},
      byWeek: {},
      topTenFoods: {},
    };
  },
});
</script>

<template>
    <div class="container q-ma-lg">
        <div class="row">
            <div class="col row justify-center">
                <div class="title text-h5">Expenses by Tag</div>
                <MyBarChart :data="byTag" />
            </div>
            <div class="col row justify-center">
                <div class="title text-h5">Expenses by Week</div>
                <!-- <MyBarChart :data="byWeek"/> -->
                <MyLineChart />
            </div>
        </div>
        <div class="row">
            <div class="col">
                <div class="title">Top Ten Food Expenses</div>
                <MyBarChart />
            </div>
            <div class="col">
                <div class="title">More data</div>
                <MyBarChart />
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue';
import MyBarChart from 'src/components/MyBarChart.vue';
import { getExpensesByTag, getExpensesByWeek } from 'src/components/APICaller';
import MyLineChart from 'src/components/MyLineChart.vue';


export default defineComponent({

    components: {
    MyBarChart,
    MyLineChart
},

    mounted() {
        getExpensesByTag().then(result => this.byTag = result)
        getExpensesByWeek().then(result => this.byWeek = result )
    },

    data() {
        return {
            byTag: {},
            byWeek: {}
        }
    }

})

</script>

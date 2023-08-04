<template>
  <q-page class="q-ma-md column items-center">
    <div class="q-pa-md" style="max-width: 100%">
      <HistoryTable :rows="data" v-if="data" />
    <q-spinner color="primary" size="3em" v-else />

    </div>
  </q-page>
</template>

<script>
import HistoryTable from '../components/HistoryTable.vue';

export default {
  components: {
    HistoryTable,
  },
  async mounted() {

    var requestOptions = {
      method: 'GET',
      redirect: 'follow',
    };
    console.log(process.env.API + '/data')
    try {
      let response = await fetch(process.env.API + '/data', requestOptions)
      let result = await response.json();
      this.data = result.map(elem => {
        elem.id = Math.random() * 1000
        return elem
      } )
    } catch (error) {
      console.log(error)
    }
  },
  data() {
    return {
      data: undefined,
    };
  },
};
</script>

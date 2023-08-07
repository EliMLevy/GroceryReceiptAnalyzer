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
import { getData } from '../components/APICaller'
export default {
  components: {
    HistoryTable,
  },
  async mounted() {

    this.data = await getData();
    
  },
  data() {
    return {
      data: undefined,
    };
  },
};
</script>

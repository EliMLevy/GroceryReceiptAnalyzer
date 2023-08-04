<template>
  <q-page class="q-ma-md column items-center" v-if="!loading">
    <div class="q-mr-md" v-if="successfulUpload">
      <q-chip  color="teal" text-color="white" icon="check">
        Successful Upload
      </q-chip>
    </div>
    <div class="input-container q-my-md row items-center">
      <h2 class="q-mr-md text-h5">Grocery Store:</h2>
      <q-input outlined v-model="groceryStoreName" label="name" />
    </div>
    <div
      :class="{
        'uploader column items-center': true,
        'fade-in': groceryStoreName,
      }"
      v-if="groceryStoreName"
    >
      <q-uploader
        :url="import.meta.env.VUE_APP_API_ENDPOINT + ':' + import.meta.env.VUE_APP_API_PORT +'/upload?store=' + groceryStoreName"
        style="max-width: 300px"
        @uploaded="uploadComplete"
      />
    </div>

    <div
      :class="{ 'table-container': true, 'fade-in': ocrResult || true }"
      style="max-width: 100%"
      v-if="ocrResult"
    >
      <my-table
        :data="edittedList"
        :setData="(data: any) => edittedList = data"
        :handleSubmit="submitEdittedList"
      />
    </div>
  </q-page>
  <q-page class="q-ma-md column items-center" v-else>
    <q-spinner color="primary" size="3em" />
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import MyTable from '../components/EditableTable.vue';

export default defineComponent({
  name: 'IndexPage',
  methods: {
    uploadComplete(e: any) {
      console.log(JSON.parse(e.xhr.response));
      this.ocrResult = JSON.parse(e.xhr.response);
      this.edittedList = JSON.parse(e.xhr.response);
    },
    async submitEdittedList() {
      console.log(
        JSON.stringify(this.ocrResult),
        JSON.stringify(this.edittedList)
      );
      var raw = JSON.stringify({
        old: this.ocrResult,
        new: this.edittedList,
      });

      var requestOptions: RequestInit = {
        method: 'POST',
        body: raw,
        redirect: 'follow',
      };

      try {
        this.loading = true;
        let response = await fetch(
          import.meta.env.VUE_APP_API_ENDPOINT + ':' + import.meta.env.VUE_APP_API_PORT +'/storelist',
          requestOptions
        );
        let result = await response.text();
        console.log(result);

        this.resetPage();
        this.successfulUpload = true;
      } catch (error) {
        console.log(error);
        this.successfulUpload = false
      }
      this.loading = false;
    },
    resetPage() {
      this.groceryStoreName = undefined;
      this.ocrResult = undefined;
      this.edittedList = undefined;
    },
  },
  data() {
    return {
      groceryStoreName: undefined,
      // ocrResult: [{"index":0,"food":"Sparkling Apple Cider","price":5.79,"store":"Key Food"},{"index":1,"food":"RICE SELECT SUSHI","price":9.79,"store":"Key Food"},{"index":2,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"},{"index":3,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"}],
      // edittedList: [{"index":0,"food":"Sparkling Apple Cider","price":5.79,"store":"Key Food"},{"index":1,"food":"RICE SELECT SUSHI","price":9.79,"store":"Key Food"},{"index":2,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"},{"index":3,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"}],
      ocrResult: undefined,
      edittedList: undefined,
      loading: false,
      successfulUpload: false
    };
  },
  components: {
    MyTable,
  },
});
</script>

<style scoped>
.fade-in {
  animation-duration: 1s;
  animation-name: fadein;
  animation-direction: normal;
  opacity: 1;
}

@keyframes fadein {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
</style>

<template>
  <q-page class="q-ma-md column items-center" v-if="!loading">
    <div class="q-mr-md" v-if="successfulUpload">
      <q-chip color="teal" text-color="white" icon="check">
        Successful Upload
      </q-chip>
    </div>
    <div class="input-container row" style="width: 100%" v-if="true">
      <div class="col">
        <h2 class="text-h6">Grocery Store:</h2>
      </div>
      <div class="col-6">
        <addable-select
          style="width: 100%"
          :storeOptions="['Trader Joe\'s', 'Key Food']"
          :setSelection="(store: any) => groceryStoreName=store"
        />
      </div>
    </div>
    <div class="input-container row" style="width: 100%">
      <div class="col">
        <h2 class="text-h6">Date:</h2>
      </div>
      <div class="col">
        <my-date-picker :setDate="(date: any) => shoppingDate = date" />
      </div>
    </div>
    <div
      :class="{
        'uploader column items-center': true,
        'fade-in': groceryStoreName,
      }"
      v-if="groceryStoreName && shoppingDate"
    >
      <q-uploader
        :url="APIHostname + '/upload?store=' + groceryStoreName"
        style="max-width: 300px"
        @uploaded="uploadComplete"
        @failed="uploadFailed"
      />
    </div>

    <div
      :class="{ 'table-container': true, 'fade-in': ocrResult }"
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
import AddableSelect from 'src/components/AddableSelect.vue';
import MyDatePicker from 'src/components/MyDatePicker.vue';
import { useQuasar } from 'quasar';

export default defineComponent({
  name: 'IndexPage',
  setup() {
    const $q = useQuasar();
    return {
      uploadFailed(e: any) {
        console.log(JSON.parse(e.xhr.response));
        $q.notify({
          message: JSON.parse(e.xhr.response).msg,
          color: 'negative',
          icon: 'warning',
        });
      },
    };
  },
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
          process.env.API + '/storelist?' + 'date=' + this.shoppingDate,
          requestOptions
        );
        let result = await response.text();
        console.log(result);

        this.resetPage();
        this.successfulUpload = true;
      } catch (error) {
        console.log(error);
        this.successfulUpload = false;
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
      shoppingDate: undefined,
      // ocrResult: [{"index":0,"food":"Sparkling Apple Cider","price":5.79,"store":"Key Food"},{"index":1,"food":"RICE SELECT SUSHI","price":9.79,"store":"Key Food"},{"index":2,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"},{"index":3,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"}],
      // edittedList: [{"index":0,"food":"Sparkling Apple Cider","price":5.79,"store":"Key Food"},{"index":1,"food":"RICE SELECT SUSHI","price":9.79,"store":"Key Food"},{"index":2,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"},{"index":3,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"}],
      ocrResult: undefined,
      edittedList: undefined,
      loading: false,
      successfulUpload: false,
      APIHostname: process.env.API,
    };
  },
  components: {
    MyTable,
    AddableSelect,
    MyDatePicker,
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

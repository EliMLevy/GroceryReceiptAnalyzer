<template>
  <q-page class="q-ma-md column items-center" v-if="!loading">
    <div class="input-container row" style="width: 100%" v-if="true">
      <div class="col">
        <h2 class="text-h6">Grocery Store:</h2>
      </div>
      <div class="col-6">
        <addable-select
          style="width: 100%"
          :storeOptions="['Trader Joe\'s', 'Key Food']"
          :setSelection="(store) => (groceryStoreName = store)"
        />
      </div>
    </div>
    <div class="input-container row" style="width: 100%">
      <div class="col">
        <h2 class="text-h6">Date:</h2>
      </div>
      <div class="col">
        <my-date-picker :setDate="(date) => (shoppingDate = date)" />
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
        :setData="(data) => (edittedList = data)"
        :handleSubmit="submitEdittedList"
      />
    </div>
  </q-page>
  <q-page class="q-ma-md column items-center" v-else>
    <q-spinner color="primary" size="3em" />
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';
import MyTable from '../components/EditableTable.vue';
import AddableSelect from 'src/components/AddableSelect.vue';
import MyDatePicker from 'src/components/MyDatePicker.vue';
import { useQuasar } from 'quasar';
import { storeNewList } from '../components/APICaller';

export default defineComponent({
  name: 'IndexPage',
  setup() {
    const $q = useQuasar();
    return {
      uploadFailed(e) {
        console.log(JSON.parse(e.xhr.response));
        $q.notify({
          message: JSON.parse(e.xhr.response).msg,
          color: 'negative',
          icon: 'warning',
        });
      },
      notify: $q.notify,
    };
  },
  methods: {
    uploadComplete(e) {
      console.log(JSON.parse(e.xhr.response));
      this.ocrResult = JSON.parse(e.xhr.response);
      this.edittedList = JSON.parse(e.xhr.response);
      this.notify({
        message: 'Success!',
        color: 'positive',
        icon: 'check',
      });
    },
    async submitEdittedList() {
      console.log(
        JSON.stringify(this.ocrResult),
        JSON.stringify(this.edittedList)
      );

      if (this.edittedList != undefined) {
        this.edittedList.forEach((elem) => {
          elem.price = Number(elem.price);
        });
      }

      this.loading = true;
      let result = await storeNewList(
        {
          old: this.ocrResult,
          new: this.edittedList,
        },
        this.shoppingDate
      );
      if (result) {
        this.resetPage();
        this.notify({
          message: 'Success!',
          color: 'positive',
          icon: 'check',
        });
      } else {
        this.notify({
          message: 'Failed to upload data',
          color: 'negative',
          icon: 'warning',
        });
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
      ocrResult: undefined,
      edittedList: undefined,
      loading: false,
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

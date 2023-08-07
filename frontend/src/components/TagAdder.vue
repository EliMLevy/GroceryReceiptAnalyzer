<template>
    <div class="q-pa-md">
      <div class="q-gutter-y-md">
  
        <q-select
          filled
          v-model="model"
          use-input
          use-chips
          multiple
          hide-dropdown-icon
          input-debounce="0"
          new-value-mode="add-unique"
          style="width: 250px"
          @add="(e) => addTag(e.value)"
          @remove="(e) => removeTag(e.value)"
        />
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue'
  
  export default {
    setup () {
      return {
        model: ref(null),
      }
    },
    mounted() {
      this.model = this.data
    },
    props: {
      data: {
        type: Array,
        default: () => []
      },
      addTag: {
        type: Function,
        default: () => console.log("not implemented")
      },
      removeTag: {
        type: Function,
        default: () => console.log("not implemented")
      }
    }
  }
  </script>
  
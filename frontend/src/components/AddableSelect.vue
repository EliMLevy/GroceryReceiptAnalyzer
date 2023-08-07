<template>
  <q-select
    filled
    v-model="model"
    use-input
    input-debounce="0"
    :options="filterOptions"
    @filter="filterFn"
    style="width: 250px"
    @update:model-value="() => setSelection(model)"
  />
</template>

<script>
import { ref , toRefs} from 'vue';


export default {
  setup(props) {
    const { storeOptions } = toRefs(props)
    const filterOptions = ref([...storeOptions.value]);

    return {
      model: ref(null),
      filterOptions,
      filterFn(val, update) {
        update(() => {
          if (val === '') {
            filterOptions.value = [...storeOptions.value];
          } else {
            const needle = val.toLowerCase();
            filterOptions.value = [...storeOptions.value].filter(
              (v) => v.toLowerCase().indexOf(needle) > -1
            );
          }
        });
      },
    };
  },
  props: {
    setSelection: {
        type: Function,
        default: () => console.log("Not implemented")
    },
    storeOptions: {
        type: Array,
        default: () => []
    }
  }
};
</script>

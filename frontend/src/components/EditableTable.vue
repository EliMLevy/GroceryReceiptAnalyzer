<template>
  <div class="q-pa-md scroll">
    <q-table :rows="data" :columns="columns" row-key="food" dense :pagination="{rowsPerPage: 0}" hide-bottom>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="food" :props="props">
            {{ props.row.food }}
            <q-popup-edit v-model="props.row.food" title="Update calories" buttons v-slot="scope">
              <q-input type="text" v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="price" :props="props">
            {{ props.row.price }}
            <q-popup-edit v-model="props.row.price" buttons v-slot="scope">
              <q-input v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="store" :props="props">
            {{ props.row.store }}
            <q-popup-edit v-model="props.row.store" buttons v-slot="scope">
              <q-input v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="delete" :props="props" >
            <q-icon name="delete" size="20px" class="clickable-icon" @click="() => deleteEntry(props.row)"/>
          
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <q-btn color="primary" label="Confirm" @click="handleSubmit" />
  </div>
</template>

<script>
const columns = [
  {
    name: 'food',
    required: true,
    label: 'Food',
    align: 'left',
    field: (row) => row.food,
  },
  {
    name: 'price',
    required: true,
    label: 'Price',
    align: 'left',
    field: (row) => row.price,
    format: (val) => `$${val}`,
  },
  {
    name: 'store',
    required: true,
    label: 'Store',
    align: 'left',
    field: (row) => row.store,
  },
  {
    name: 'delete',
    label: 'Delete',
    align: 'right',
    field: () => 'X',
  },
];

// const rows = [
//   { food: 'Sparkling Apple Cider', price: 5.79, store: 'Key Food', id: 0 },
//   { food: 'RICE SELECT SUSHI', price: 9.79, store: 'Key Food', id: 1 },
//   { food: 'Shredded Mozerella Cheese', price: 4.99, store: 'Key Food', id: 2 },
//   { food: 'Shredded Mozerella Cheese', price: 4.99, store: 'Key Food', id: 3 },
// ];

export default {
  props: {
    data: {
      type: Array,
      default: () => [],
    },
    setData: {
        type: Function
    },
    handleSubmit: {
        type: Function,
        default: () => console.log('Not Implemented')
    }
  },
  setup() {
    return {
      columns,
    };
  },
  methods: {
    deleteEntry(row) {
        this.setData(this.data.filter(elem => elem.index != row.index))
    }
  },
};
</script>


<style scoped>
.clickable-icon:hover {
    background-color: lightgray;
    border-radius: 3px;
}
</style>
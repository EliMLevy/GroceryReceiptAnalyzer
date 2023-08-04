<template>
    <q-table
        title="Grocery History"
        :rows="rows"
        :columns="columns"
        row-key="id"
        :pagination="{ rowsPerPage: 0 }"
        hide-bottom
      >
        <template v-slot:top-right>
          <q-btn
            color="primary"
            icon-right="archive"
            label="Export to csv"
            no-caps
            @click="() => exportTable(rows)"
          /> </template
      ></q-table>
</template>

<script>
import { exportFile, useQuasar } from 'quasar'
const columns = [
  {
    name: 'food',
    required: true,
    label: 'Food',
    align: 'left',
    field: (row) => row.food,
    sortable: true,
  },
  {
    name: 'price',
    required: true,
    label: 'Price',
    align: 'left',
    field: (row) => row.price,
    format: (val) => `$${val}`,
    sortable: true,
  },
  {
    name: 'store',
    required: true,
    label: 'Store',
    align: 'left',
    field: (row) => row.store,
    sortable: true,
  },
  {
    name: 'date',
    required: true,
    label: 'Date',
    align: 'left',
    field: (row) => row.date,
    sortable: true,
  },
];


export default {
  setup() {
    const $q = useQuasar();
    function wrapCsvValue(val, formatFn, row) {
      let formatted = val;

      formatted =
        formatted === void 0 || formatted === null ? '' : String(formatted);

      formatted = formatted.split('"').join('""');
      /**
       * Excel accepts \n and \r in strings, but some other CSV parsers do not
       * Uncomment the next two lines to escape new lines
       */
      // .split('\n').join('\\n')
      // .split('\r').join('\\r')

      return `"${formatted}"`;
    }
    return {
      columns,
      exportTable(rows) {
        // naive encoding to csv format
        const content = [columns.map((col) => wrapCsvValue(col.label))]
          .concat(
            rows.map((row) =>
              columns
                .map((col) =>
                  wrapCsvValue(
                    typeof col.field === 'function'
                      ? col.field(row)
                      : row[col.field === void 0 ? col.name : col.field],
                    col.format,
                    row
                  )
                )
                .join(',')
            )
          )
          .join('\r\n');

        const status = exportFile('grocery-export.csv', content, 'text/csv');

        if (status !== true) {
          $q.notify({
            message: 'Browser denied file download...',
            color: 'negative',
            icon: 'warning',
          });
        }
      },
    };
  },
  props: {
    rows: {
        type: Array,
        default: () => []
    }
  },
  methods: {},
};
</script>

<template>
    <q-input filled v-model="date" mask="date" :rules="['date']" >
      <template v-slot:append>
        <q-icon name="event" class="cursor-pointer">
          <q-popup-proxy cover transition-show="scale" transition-hide="scale">
            <q-date v-model="date" @update:model-value="() => setDate(date)">
              <div class="row items-center justify-end">
                <q-btn v-close-popup label="Close" color="primary" flat />
              </div>
            </q-date>
          </q-popup-proxy>
        </q-icon>
      </template>
    </q-input>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const todayDate = new Date()
    const monthFormatted = todayDate.getMonth() + 1 > 9 ? todayDate.getMonth() + 1 : '0' + (todayDate.getMonth()  + 1)
    const dateFormatted = todayDate.getDate() + 1 > 9 ? todayDate.getDate() + 1 : '0' + (todayDate.getDate()  + 1)
    const today = `${todayDate.getFullYear()}/${monthFormatted}/${dateFormatted}`
    return {
      date: ref(today),
    };
  },
  mounted() {
    this.setDate(this.date)
  },    
  props: {
    setDate: {
        type: Function,
        default: () => console.log("Not implemented")
    }
  }
};
</script>

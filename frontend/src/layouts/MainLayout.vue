<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat @click="drawer = !drawer" round dense icon="menu" />

        <q-toolbar-title> Grocery Analyzer </q-toolbar-title>

        <div>By Eli Levy</div>
      </q-toolbar>
    </q-header>
    <q-drawer
      v-model="drawer"
      show-if-above
      :width="200"
      :breakpoint="700"
      elevated
      class="bg-primary text-white"
    >
      <q-scroll-area class="fit">
        <q-list bordered separator>
          <q-item clickable v-ripple href="/">
            <q-item-section>Receipt Uploader</q-item-section>
          </q-item>
          <q-item clickable v-ripple href="/history">
            <q-item-section>History</q-item-section>
          </q-item>
          <q-item clickable v-ripple href="/analysis">
            <q-item-section>Analysis</q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'MainLayout',
  data() {
    return {
      drawer: false,
    };
  },
});
</script>


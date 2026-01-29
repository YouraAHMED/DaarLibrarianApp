<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style>
body {
  margin: 0;
  background: #121212;
  color: white;
  font-family: Arial, Helvetica, sans-serif;
}

#app {
  min-height: 100vh;
}
</style>

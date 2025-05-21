<script setup>
// App.vue agora é apenas um container para o router-view
</script>

<template>
  <router-view></router-view>
</template>

<style>
:root {
  --primary: #2E7D32;
  --secondary: #A5D6A7;
  --background: #F5F5F5;
  --text: #424242;
}

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: var(--background);
}
</style>

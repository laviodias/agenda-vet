<script setup>
import { onMounted } from 'vue'
import { useBrand } from './composables/useBrand.js'

// Inicializar configurações de marca
const { loadBrandConfig } = useBrand()

onMounted(() => {
  // Carregar configurações de marca na inicialização da aplicação
  loadBrandConfig()
})
</script>

<template>
  <router-view></router-view>
</template>

<style>
:root {
  /* Cores padrão que serão sobrescritas pelo brandService */
  --primary-color: #00d1b2;
  --secondary-color: #363636;
  --accent-color: #3273dc;
  --background-color: #f5f5f5;
  
  /* Manter compatibilidade com o sistema anterior */
  --primary: var(--primary-color);
  --secondary: var(--secondary-color);
  --background: var(--background-color);
  --text: var(--secondary-color);
  
  /* Preview de cores para o formulário */
  --preview-primary: var(--primary-color);
  --preview-secondary: var(--secondary-color);
  --preview-accent: var(--accent-color);
  --preview-background: var(--background-color);
}

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: var(--background-color);
}

/* Sobrescrever cores do Bulma com nossas variáveis */
.navbar.is-primary {
  background-color: var(--primary-color) !important;
}

.button.is-primary {
  background-color: var(--primary-color) !important;
  border-color: var(--primary-color) !important;
}

.button.is-primary:hover {
  background-color: var(--primary-color) !important;
  filter: brightness(0.9);
}

.button.is-info {
  background-color: var(--accent-color) !important;
  border-color: var(--accent-color) !important;
}

.title {
  color: var(--secondary-color) !important;
}

.subtitle {
  color: var(--secondary-color) !important;
  opacity: 0.8;
}

/* Classes de preview para o formulário */
.preview-primary {
  background-color: var(--preview-primary) !important;
}

.preview-secondary {
  background-color: var(--preview-secondary) !important;
}

.preview-accent {
  background-color: var(--preview-accent) !important;
}

.preview-background {
  background-color: var(--preview-background) !important;
}
</style>

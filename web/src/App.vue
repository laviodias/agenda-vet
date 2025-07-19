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
  
  /* Cores de status e feedback */
  --success-color: #48c774;
  --danger-color: #f14668;
  --warning-color: #ffdd57;
  --info-color: #3298dc;
  
  /* Cores de interface */
  --text-color: #363636;
  --border-color: #dbdbdb;
  --shadow-color: #000000;
  
  /* Manter compatibilidade com o sistema anterior */
  --primary: var(--primary-color);
  --secondary: var(--secondary-color);
  --background: var(--background-color);
  --text: var(--text-color);
  
  /* Preview de cores para o formulário */
  --preview-primary: var(--primary-color);
  --preview-secondary: var(--secondary-color);
  --preview-accent: var(--accent-color);
  --preview-background: var(--background-color);
  --preview-success: var(--success-color);
  --preview-danger: var(--danger-color);
  --preview-warning: var(--warning-color);
  --preview-info: var(--info-color);
}

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: var(--background-color);
  color: var(--text-color);
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
  background-color: var(--info-color) !important;
  border-color: var(--info-color) !important;
}

.button.is-success {
  background-color: var(--success-color) !important;
  border-color: var(--success-color) !important;
}

.button.is-danger {
  background-color: var(--danger-color) !important;
  border-color: var(--danger-color) !important;
}

.button.is-warning {
  background-color: var(--warning-color) !important;
  border-color: var(--warning-color) !important;
  color: #333 !important;
}

.title {
  color: var(--text-color) !important;
}

.subtitle {
  color: var(--text-color) !important;
  opacity: 0.8;
}

/* Tags de status */
.tag.is-success {
  background-color: var(--success-color) !important;
  color: white !important;
}

.tag.is-danger {
  background-color: var(--danger-color) !important;
  color: white !important;
}

.tag.is-warning {
  background-color: var(--warning-color) !important;
  color: #333 !important;
}

.tag.is-info {
  background-color: var(--info-color) !important;
  color: white !important;
}

/* Notificações */
.notification.is-success {
  background-color: var(--success-color) !important;
  color: white !important;
}

.notification.is-danger {
  background-color: var(--danger-color) !important;
  color: white !important;
}

.notification.is-warning {
  background-color: var(--warning-color) !important;
  color: #333 !important;
}

.notification.is-info {
  background-color: var(--info-color) !important;
  color: white !important;
}

/* Classes de preview para o formulário */
.preview-primary {
  background-color: var(--preview-primary) !important;
}

.preview-secondary {
  background-color: var(--preview-secondary) !important;
}

.preview-success {
  background-color: var(--preview-success) !important;
}

.preview-danger {
  background-color: var(--preview-danger) !important;
}

.preview-warning {
  background-color: var(--preview-warning) !important;
}

.preview-info {
  background-color: var(--preview-info) !important;
}
</style>

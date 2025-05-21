<script setup>
import AgendamentoForm from '../components/AgendamentoForm.vue';
</script>

<template>
  <div class="home-container">
    <div class="header">
      <span class="logo-vet">🐾</span>
      <h1 class="title is-2 has-text-primary mb-4">AgendaVet</h1>
      <p class="subtitle">Facilite o agendamento de consultas para o seu pet!</p>
    </div>
    <div class="actions">
      <button class="button is-primary is-fullwidth mt-4">Agendar Consulta</button>
    </div>
    <div class="illustration">
      <img src="https://cdn-icons-png.flaticon.com/512/616/616408.png" alt="Veterinário" />
    </div>
  </div>
  <AgendamentoForm />
</template>

<style scoped>
.home-container {
  min-height: 100vh;
  background: var(--background, #F5F5F5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}
.header {
  text-align: center;
  margin-bottom: 2rem;
}
.logo-vet {
  font-size: 3rem;
  display: block;
  margin-bottom: 0.5rem;
}
h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}
.subtitle {
  color: var(--text, #424242);
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}
.actions {
  margin-bottom: 2rem;
}
.btn-primary {
  background: var(--primary, #2E7D32);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 2rem;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-primary:hover {
  background: var(--secondary, #A5D6A7);
  color: var(--primary, #2E7D32);
}
.illustration img {
  width: 120px;
  margin-top: 2rem;
  filter: drop-shadow(0 4px 12px rgba(46, 125, 50, 0.15));
}
</style> 
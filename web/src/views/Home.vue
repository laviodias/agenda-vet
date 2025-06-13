<script setup>
import { useRouter } from 'vue-router'
import AgendamentoForm from '../components/AgendamentoForm.vue';

const router = useRouter()

const goToAuth = () => {
  router.push('/auth')
}
</script>

<template>
  <div class="home-container">
    <div class="header">
      <span class="logo-vet">🐾</span>
      <h1 class="title is-2 has-text-primary mb-4">AgendaVet</h1>
      <p class="subtitle">Facilite o agendamento de consultas para o seu pet!</p>
    </div>
    <div class="actions">
      <button @click="goToAuth" class="button is-primary is-fullwidth mt-4">
        <span class="icon">
          <i class="fas fa-sign-in-alt"></i>
        </span>
        <span>Entrar / Cadastrar</span>
      </button>
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
.button {
  border-radius: 8px;
  font-weight: 600;
  height: 3rem;
  transition: all 0.2s;
}
.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
.illustration img {
  width: 120px;
  margin-top: 2rem;
  filter: drop-shadow(0 4px 12px rgba(46, 125, 50, 0.15));
}
</style> 
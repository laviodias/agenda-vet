<template>
  <div class="agendamento-container">
    <h1 class="title is-2 has-text-primary mb-4">Agendamento</h1>
    <form @submit.prevent="handleSubmit" class="agendamento-form box">
      <WeeklyCalendar v-model="agendamento.dateTime" />
      <div class="field mt-4">
        <label for="profissional" class="label">Profissional</label>
        <div class="control">
          <div class="select is-fullwidth is-light">
            <select id="profissional" v-model="agendamento.profissional" required>
              <option value="">Selecione um profissional</option>
              <option value="Dr. Silva">Dr. Silva</option>
              <option value="Dra. Santos">Dra. Santos</option>
              <option value="Dr. Costa">Dr. Costa</option>
            </select>
          </div>
        </div>
      </div>
      <div class="field">
        <label for="servico" class="label">Serviço</label>
        <div class="control">
          <div class="select is-fullwidth is-light">
            <select id="servico" v-model="agendamento.servico" required>
              <option value="">Selecione um serviço</option>
              <option value="Consulta">Consulta</option>
              <option value="Vacina">Vacina</option>
              <option value="Banho e Tosa">Banho e Tosa</option>
            </select>
          </div>
        </div>
      </div>
      <div class="field">
        <label for="pet" class="label">Pet</label>
        <div class="control">
          <div class="select is-fullwidth is-light">
            <select id="pet" v-model="agendamento.pet" required>
              <option value="">Selecione um pet</option>
              <option value="Cachorro">Cachorro</option>
              <option value="Gato">Gato</option>
              <option value="Outro">Outro</option>
            </select>
          </div>
        </div>
      </div>
      <div class="field">
        <div class="control">
          <button type="submit" class="button is-primary is-fullwidth mt-4">Confirmar Agendamento</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import WeeklyCalendar from './WeeklyCalendar.vue';

const agendamento = reactive({
  dateTime: { date: '', time: '' },
  profissional: '',
  servico: '',
  pet: ''
});

function handleSubmit() {
  console.log('Agendamento enviado:', agendamento);
}
</script>

<style scoped>
.agendamento-container {
  min-height: 100vh;
  background: var(--background, #F5F5F5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}
.agendamento-form {
  width: 100%;
  max-width: 800px;
  background: var(--scheme-main, #FFFFFF);
  padding: 2rem;
  border-radius: 8px;
  box-shadow: var(--shadow-md, 0 4px 6px rgba(0, 0, 0, 0.1));
}

.agendamento-form .label {
  color: #333;
}
</style> 
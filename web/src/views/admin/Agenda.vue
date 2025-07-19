<script setup>
import { ref, onMounted } from 'vue'
import DisponibilidadeProfissional from '../../components/DisponibilidadeProfissional.vue'
import authService from '../../services/authService.js'

const profissionais = ref([])
const selectedProfissional = ref('')
const loading = ref(false)
const error = ref(null)

const carregarProfissionais = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await authService.getProfissionais()
    profissionais.value = Array.isArray(response) ? response : []
  } catch (err) {
    console.error('Erro ao carregar profissionais:', err)
    error.value = 'Erro ao carregar profissionais. Tente novamente.'
  } finally {
    loading.value = false
  }
}

const carregarDisponibilidades = () => {
  // Será chamado quando um profissional for selecionado
  // O componente DisponibilidadeProfissional cuidará de carregar os dados
}

onMounted(() => {
  carregarProfissionais()
})
</script>

<template>
  <div class="agenda-container">
    <div class="header-section">
      <h1 class="title is-2 mb-4">Gerenciamento de Disponibilidade</h1>
      <p class="subtitle is-6 has-text-grey">
        Configure a disponibilidade dos profissionais por dia da semana
      </p>
    </div>

    <!-- Error state -->
    <div v-if="error" class="notification is-danger is-light mb-4">
      <button class="delete" @click="error = null"></button>
      {{ error }}
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="has-text-centered">
      <span class="icon is-large">
        <i class="fas fa-spinner fa-spin"></i>
      </span>
      <p class="mt-3">Carregando profissionais...</p>
    </div>

    <!-- Seleção de Profissional -->
    <div v-else class="box mb-6">
      <h2 class="title is-4 mb-4">Selecionar Profissional</h2>
      <div class="field">
        <label class="label">Profissional</label>
        <div class="control">
          <div class="select is-fullwidth">
            <select v-model="selectedProfissional" @change="carregarDisponibilidades">
              <option value="">Selecione um profissional</option>
              <option 
                v-for="prof in profissionais" 
                :key="prof.id" 
                :value="prof.id"
              >
                {{ prof.nome }} - {{ prof.especialidade || 'Sem especialidade' }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Gerenciamento de Disponibilidade -->
    <div v-if="selectedProfissional" class="disponibilidade-section">
      <DisponibilidadeProfissional :profissional-id="selectedProfissional" />
    </div>

    <!-- Mensagem quando nenhum profissional está selecionado -->
    <div v-else class="no-selection">
      <div class="no-selection-content">
        <i class="fas fa-user-md"></i>
        <h3>Selecione um Profissional</h3>
        <p>Escolha um profissional acima para gerenciar sua disponibilidade</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.agenda-container {
  padding: 20px;
}

.header-section {
  margin-bottom: 20px;
}

.header-section h1 {
  color: #333;
  margin-bottom: 10px;
}

.subtitle {
  margin-bottom: 0;
}

.box {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
}

.field {
  margin-bottom: 1rem;
}

.label {
  font-weight: 500;
  color: #333;
  margin-bottom: 0.5rem;
}

.select select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.select select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.disponibilidade-section {
  margin-top: 20px;
}

.no-selection {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.no-selection-content {
  text-align: center;
  color: #666;
}

.no-selection-content i {
  font-size: 48px;
  margin-bottom: 15px;
  color: #ddd;
}

.no-selection-content h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.no-selection-content p {
  margin: 0;
  font-size: 14px;
}

.notification {
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.notification.is-danger {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.delete {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  float: right;
  color: #721c24;
}

.icon {
  margin-right: 0.5rem;
}
</style> 
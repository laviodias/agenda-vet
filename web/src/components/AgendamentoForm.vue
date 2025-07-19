<template>
  <div class="agendamento-container">
    <h1 class="title is-2 has-text-primary mb-4">Agendamento</h1>
    
    <!-- Loading state -->
    <div v-if="loading" class="has-text-centered">
      <span class="icon is-large">
        <i class="fas fa-spinner fa-spin"></i>
      </span>
      <p class="mt-3">Carregando dados...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="notification is-danger is-light">
      <button class="delete" @click="error = null"></button>
      {{ error }}
    </div>

    <!-- Form -->
    <form v-else @submit.prevent="handleSubmit" class="agendamento-form box">
      <div class="field">
        <label for="data" class="label">Data</label>
        <div class="control">
          <input 
            type="date" 
            id="data"
            class="input" 
            v-model="agendamento.data"
            :min="today"
            @change="carregarProfissionaisDisponiveis"
            required
          />
        </div>
      </div>

      <div class="field">
        <label for="hora" class="label">Horário</label>
        <div class="control">
          <input 
            type="time" 
            id="hora"
            class="input" 
            v-model="agendamento.hora"
            @change="filtrarProfissionaisPorHorario"
            required
          />
        </div>
      </div>
      
      <div class="field">
        <label for="profissional" class="label">Profissional</label>
        <div class="control">
          <div class="select is-fullwidth is-light">
            <select id="profissional" v-model="agendamento.profissional" required>
              <option value="">Selecione um profissional</option>
              <option 
                v-for="profissional in profissionaisDisponiveis" 
                :key="profissional.id" 
                :value="profissional.id"
              >
                {{ profissional.nome }} ({{ profissional.especialidade || 'Sem especialidade' }})
                - {{ profissional.hora_inicio }} às {{ profissional.hora_fim }}
              </option>
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
              <option 
                v-for="servico in servicos" 
                :key="servico.id" 
                :value="servico.id"
              >
                {{ servico.nome }} - R$ {{ servico.preco }}
              </option>
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
              <option 
                v-for="pet in pets" 
                :key="pet.id" 
                :value="pet.id"
              >
                {{ pet.nome }} ({{ pet.especie }})
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="field">
        <label for="observacoes" class="label">Observações</label>
        <div class="control">
          <textarea 
            id="observacoes"
            class="textarea" 
            v-model="agendamento.observacoes"
            placeholder="Alguma observação importante sobre o agendamento..."
            rows="3"
          ></textarea>
        </div>
      </div>
      
      <div class="field">
        <div class="control">
          <div class="buttons is-fullwidth mt-4">
            <button 
              type="submit" 
              class="button is-primary is-fullwidth"
              :disabled="submitting"
            >
              <span v-if="submitting" class="icon">
                <i class="fas fa-spinner fa-spin"></i>
              </span>
              <span>{{ submitting ? 'Criando...' : 'Confirmar Agendamento' }}</span>
            </button>
            <button type="button" class="button is-light is-fullwidth" @click="handleClose">Cancelar</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, onMounted, ref, computed } from 'vue';
import authService from '../services/authService.js';

// Props
const props = defineProps({
  pets: {
    type: Array,
    default: () => []
  },
  petSelecionado: {
    type: Object,
    default: null
  }
});

// Emits
const emit = defineEmits(['close', 'agendamento-criado']);

// Estados
const loading = ref(false)
const error = ref(null)
const submitting = ref(false)
const servicos = ref([])
const profissionaisDisponiveis = ref([])

const agendamento = reactive({
  data: '',
  hora: '',
  profissional: '',
  servico: '',
  pet: '',
  observacoes: ''
});

// Computed
const today = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

const diaSemana = computed(() => {
  if (!agendamento.data) return null
  const date = new Date(agendamento.data)
  return date.getDay() // 0 = Domingo, 1 = Segunda, etc.
})

// Carregar dados na montagem
onMounted(async () => {
  await loadData()
  
  // Se um pet foi selecionado, definir como padrão
  if (props.petSelecionado) {
    agendamento.pet = props.petSelecionado.id;
  }
});

// Função para carregar dados
const loadData = async () => {
  try {
    loading.value = true
    error.value = null
    
    // Carregar serviços
    const servicosData = await authService.getServicos()
    servicos.value = Array.isArray(servicosData) ? servicosData : []
    
  } catch (err) {
    console.error('Erro ao carregar dados:', err)
    error.value = 'Erro ao carregar dados. Tente novamente.'
  } finally {
    loading.value = false
  }
}

// Carregar profissionais disponíveis para o dia selecionado
const carregarProfissionaisDisponiveis = async () => {
  if (!agendamento.data || !diaSemana.value) return
  
  try {
    const response = await authService.getProfissionaisDisponiveis(diaSemana.value)
    profissionaisDisponiveis.value = response.data || []
    agendamento.profissional = '' // Reset seleção
  } catch (err) {
    console.error('Erro ao carregar profissionais disponíveis:', err)
    error.value = 'Erro ao carregar profissionais disponíveis'
  }
}

// Filtrar profissionais por horário
const filtrarProfissionaisPorHorario = () => {
  if (!agendamento.hora) return
  
  const horaSelecionada = agendamento.hora
  profissionaisDisponiveis.value = profissionaisDisponiveis.value.filter(prof => {
    return horaSelecionada >= prof.hora_inicio && horaSelecionada <= prof.hora_fim
  })
  
  agendamento.profissional = '' // Reset seleção
}

async function handleSubmit() {
  try {
    // Validar dados obrigatórios
    if (!agendamento.data) {
      error.value = 'Selecione uma data'
      return
    }
    
    if (!agendamento.hora) {
      error.value = 'Selecione um horário'
      return
    }
    
    if (!agendamento.profissional) {
      error.value = 'Selecione um profissional'
      return
    }
    
    if (!agendamento.servico) {
      error.value = 'Selecione um serviço'
      return
    }
    
    if (!agendamento.pet) {
      error.value = 'Selecione um pet'
      return
    }
    
    submitting.value = true
    error.value = null
    
    // Criar data/hora completa
    const dataHora = `${agendamento.data}T${agendamento.hora}:00`
    
    const agendamentoData = {
      data_hora: dataHora,
      profissional: agendamento.profissional,
      servico: agendamento.servico,
      pet: agendamento.pet,
      observacoes: agendamento.observacoes
    }
    
    const response = await authService.createAgendamento(agendamentoData)
    
    // Emitir evento de sucesso
    emit('agendamento-criado', response.data)
    
    // Limpar formulário
    agendamento.data = ''
    agendamento.hora = ''
    agendamento.profissional = ''
    agendamento.servico = ''
    agendamento.pet = ''
    agendamento.observacoes = ''
    
    // Fechar modal
    handleClose()
    
  } catch (err) {
    console.error('Erro ao criar agendamento:', err)
    error.value = err.response?.data?.error || 'Erro ao criar agendamento. Tente novamente.'
  } finally {
    submitting.value = false
  }
}

function handleClose() {
  emit('close')
}
</script>

<style scoped>
.agendamento-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.agendamento-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.field {
  margin-bottom: 1rem;
}

.label {
  font-weight: 500;
  color: #333;
  margin-bottom: 0.5rem;
}

.input, .select select, .textarea {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  width: 100%;
}

.input:focus, .select select:focus, .textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.button.is-primary {
  background: #007bff;
  color: white;
}

.button.is-primary:hover:not(:disabled) {
  background: #0056b3;
}

.button.is-light {
  background: #f8f9fa;
  color: #333;
  border: 1px solid #ddd;
}

.button.is-light:hover {
  background: #e9ecef;
}

.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.buttons {
  display: flex;
  gap: 10px;
}

.buttons .button {
  flex: 1;
}
</style> 
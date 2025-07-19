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
      <WeeklyCalendar 
        v-model="agendamento.dateTime" 
        :profissional="agendamento.profissional"
      />
      
      <div class="field mt-4">
        <label for="profissional" class="label">Profissional</label>
        <div class="control">
          <div class="select is-fullwidth is-light">
            <select id="profissional" v-model="agendamento.profissional" required>
              <option value="">Selecione um profissional</option>
              <option 
                v-for="profissional in profissionais" 
                :key="profissional.id" 
                :value="profissional.id"
              >
                {{ profissional.nome }} ({{ profissional.especialidade || 'Sem especialidade' }})
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
import { reactive, onMounted, ref } from 'vue';
import WeeklyCalendar from './WeeklyCalendar.vue';
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
const profissionais = ref([])
const servicos = ref([])

const agendamento = reactive({
  dateTime: { date: '', time: '' },
  profissional: '',
  servico: '',
  pet: '',
  observacoes: ''
});

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
    
    // Carregar profissionais e serviços em paralelo
    const [profissionaisData, servicosData] = await Promise.all([
      authService.getProfissionais(),
      authService.getServicos()
    ])
    
    profissionais.value = Array.isArray(profissionaisData) ? profissionaisData : []
    servicos.value = Array.isArray(servicosData) ? servicosData : []
    
  } catch (err) {
    console.error('Erro ao carregar dados:', err)
    error.value = 'Erro ao carregar dados. Tente novamente.'
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  try {
    // Validar dados obrigatórios
    if (!agendamento.dateTime.date || !agendamento.dateTime.time) {
      error.value = 'Selecione uma data e horário'
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

    // Preparar dados para a API
    const agendamentoData = {
      data_hora: `${agendamento.dateTime.date}T${agendamento.dateTime.time}:00`,
      responsavel: agendamento.profissional,
      servico: agendamento.servico,
      animal: agendamento.pet,
      observacoes: agendamento.observacoes || ''
    }

    // Chamar API para criar agendamento
    const novoAgendamento = await authService.createAgendamento(agendamentoData)
    
    console.log('Agendamento criado:', novoAgendamento)
    emit('agendamento-criado', novoAgendamento)
    emit('close')
    
  } catch (err) {
    console.error('Erro ao criar agendamento:', err)
    error.value = 'Erro ao criar agendamento. Tente novamente.'
  } finally {
    submitting.value = false
  }
}

function handleClose() {
  emit('close');
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
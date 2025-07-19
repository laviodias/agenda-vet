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
      
      <!-- Calendário Semanal -->
      <div class="field">
        <label class="label">Selecione Data e Horário</label>
        <CalendarioSemanal 
          v-model="agendamento.dataHora"
          @update:modelValue="handleDataHoraChange"
        />
      </div>
      
      <div class="field">
        <label for="servico" class="label">Serviço</label>
        <div class="control">
          <div class="select is-fullwidth">
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
          <div class="select is-fullwidth">
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
import authService from '../services/authService.js';
import CalendarioSemanal from './CalendarioSemanal.vue';

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

const agendamento = reactive({
  dataHora: { date: '', time: '' },
  servico: '',
  pet: '',
  observacoes: ''
});

// Funções
const handleDataHoraChange = (dataHora) => {
  agendamento.dataHora = dataHora;
};

const carregarServicos = async () => {
  try {
    const servicosData = await authService.getServicos();
    servicos.value = servicosData;
  } catch (err) {
    console.error('Erro ao carregar serviços:', err);
    error.value = 'Erro ao carregar serviços. Tente novamente.';
  }
};

const handleSubmit = async () => {
  if (!agendamento.dataHora.date || !agendamento.dataHora.time) {
    error.value = 'Por favor, selecione uma data e horário.';
    return;
  }

  if (!agendamento.servico) {
    error.value = 'Por favor, selecione um serviço.';
    return;
  }

  if (!agendamento.pet) {
    error.value = 'Por favor, selecione um pet.';
    return;
  }

  try {
    submitting.value = true;
    error.value = null;

    // Combinar data e hora
    const dataHora = `${agendamento.dataHora.date}T${agendamento.dataHora.time}:00`;

    const agendamentoData = {
      data_hora: dataHora,
      servico: agendamento.servico,
      animal: agendamento.pet,
      observacoes: agendamento.observacoes
    };

    const resultado = await authService.createAgendamento(agendamentoData);

    // Limpar formulário
    agendamento.dataHora = { date: '', time: '' };
    agendamento.servico = '';
    agendamento.pet = '';
    agendamento.observacoes = '';

    // Emitir evento de sucesso
    emit('agendamento-criado', resultado);

  } catch (err) {
    console.error('Erro ao criar agendamento:', err);
    error.value = 'Erro ao criar agendamento. Tente novamente.';
  } finally {
    submitting.value = false;
  }
};

const handleClose = () => {
  emit('close');
};

// Carregar dados na montagem
onMounted(async () => {
  loading.value = true;
  try {
    await carregarServicos();
  } catch (err) {
    console.error('Erro ao carregar dados:', err);
    error.value = 'Erro ao carregar dados. Tente novamente.';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.agendamento-container {
  max-width: 1200px;
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
  background: var(--danger-color);
  color: white;
  border: 1px solid var(--danger-color);
}

.notification.is-info {
  background: var(--info-color);
  color: white;
  border: 1px solid var(--info-color);
}

.delete {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  float: right;
  color: inherit;
}

.delete:hover {
  opacity: 0.7;
}
</style> 
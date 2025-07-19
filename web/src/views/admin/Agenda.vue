<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import authService from '../../services/authService.js'

const funcionarios = ref([])
const servicos = ref([])
const horariosDisponiveis = ref([])
const loading = ref(false)
const error = ref(null)
const submitting = ref(false)

const novoHorario = ref({
  funcionarioId: '',
  servicoId: '',
  data: '',
  horaInicio: '',
  horaFim: ''
})

// Carregar dados
const loadData = async () => {
  try {
    loading.value = true
    error.value = null
    
    const [funcionariosData, servicosData] = await Promise.all([
      authService.getProfissionais(),
      authService.getServicos()
    ])
    
    funcionarios.value = Array.isArray(funcionariosData) ? funcionariosData : []
    servicos.value = Array.isArray(servicosData) ? servicosData : []
    
  } catch (err) {
    console.error('Erro ao carregar dados:', err)
    error.value = 'Erro ao carregar dados. Tente novamente.'
  } finally {
    loading.value = false
  }
}

const servicosPorFuncionario = computed(() => {
  const servicosDisponiveis = {}
  funcionarios.value.forEach(funcionario => {
    servicosDisponiveis[funcionario.id] = servicos.value.filter(servico => {
      if (!servico.especialidades) return true
      const especialidadesServico = servico.especialidades.split(',').map(esp => esp.trim())
      return especialidadesServico.length === 0 || 
             especialidadesServico.includes(funcionario.especialidade)
    })
  })
  return servicosDisponiveis
})

const horariosPorFuncionario = computed(() => {
  const horarios = {}
  funcionarios.value.forEach(funcionario => {
    horarios[funcionario.id] = horariosDisponiveis.value.filter(
      h => h.funcionarioId === funcionario.id
    )
  })
  return horarios
})

const atualizarHorarioFim = () => {
  if (novoHorario.value.servicoId && novoHorario.value.horaInicio) {
    const servico = servicos.value.find(s => s.id === novoHorario.value.servicoId)
    if (servico) {
      const inicio = new Date(`2000-01-01T${novoHorario.value.horaInicio}`)
      const fim = new Date(inicio.getTime() + servico.duracao * 60000)
      novoHorario.value.horaFim = fim.toTimeString().slice(0, 5)
    }
  }
}

const adicionarHorario = async () => {
  try {
    if (!novoHorario.value.funcionarioId || !novoHorario.value.servicoId || 
        !novoHorario.value.data || !novoHorario.value.horaInicio || !novoHorario.value.horaFim) {
      error.value = 'Por favor, preencha todos os campos'
      return
    }

    submitting.value = true
    error.value = null

    const horarioData = {
      responsavel_id: novoHorario.value.funcionarioId,
      servico_id: novoHorario.value.servicoId,
      data: novoHorario.value.data,
      hora_inicio: novoHorario.value.horaInicio,
      hora_fim: novoHorario.value.horaFim
    }

    await authService.createHorarioDisponivel(horarioData)
    
    // Recarregar dados
    await loadData()
    
    // Limpar formulário
    novoHorario.value = {
      funcionarioId: '',
      servicoId: '',
      data: '',
      horaInicio: '',
      horaFim: ''
    }
    
  } catch (err) {
    console.error('Erro ao adicionar horário:', err)
    error.value = 'Erro ao adicionar horário. Tente novamente.'
  } finally {
    submitting.value = false
  }
}

const removerHorario = async (id) => {
  if (!confirm('Tem certeza que deseja remover este horário?')) {
    return
  }

  try {
    await authService.deleteHorarioDisponivel(id)
    await loadData()
  } catch (err) {
    console.error('Erro ao remover horário:', err)
    error.value = 'Erro ao remover horário. Tente novamente.'
  }
}

const formatarData = (data) => {
  return new Date(data).toLocaleDateString('pt-BR')
}

const getServicoNome = (servicoId) => {
  const servico = servicos.value.find(s => s.id === servicoId)
  return servico ? servico.nome : 'Serviço não encontrado'
}

// Carregar dados na montagem
onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="agenda-container">
    <div class="header-section">
      <h1 class="title is-2 mb-4">Gerenciamento de Agenda</h1>
      <RouterLink to="/admin/agendamentos" class="button is-info">
        <span class="icon">
          <i class="fas fa-list"></i>
        </span>
        <span>Ver Todos os Agendamentos</span>
      </RouterLink>
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
      <p class="mt-3">Carregando dados...</p>
    </div>

    <!-- Formulário de Horários -->
    <div v-else class="box mb-6">
      <h2 class="title is-4 mb-4">Adicionar Horário Disponível</h2>
      <div class="columns is-multiline">
        <div class="column is-6">
          <div class="field">
            <label class="label">Funcionário *</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select 
                  v-model="novoHorario.funcionarioId" 
                  required
                  @change="novoHorario.servicoId = ''"
                >
                  <option value="">Selecione um funcionário</option>
                  <option 
                    v-for="funcionario in funcionarios" 
                    :key="funcionario.id" 
                    :value="funcionario.id"
                  >
                    {{ funcionario.nome }} - {{ funcionario.especialidade || 'Sem especialidade' }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="field">
            <label class="label">Serviço *</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select 
                  v-model="novoHorario.servicoId" 
                  required
                  :disabled="!novoHorario.funcionarioId"
                  @change="atualizarHorarioFim"
                >
                  <option value="">Selecione um serviço</option>
                  <option 
                    v-for="servico in servicosPorFuncionario[novoHorario.funcionarioId] || []" 
                    :key="servico.id" 
                    :value="servico.id"
                  >
                    {{ servico.nome }} ({{ servico.duracao }}min)
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-4">
          <div class="field">
            <label class="label">Data *</label>
            <div class="control">
              <input 
                v-model="novoHorario.data"
                class="input" 
                type="date" 
                required
              >
            </div>
          </div>
        </div>

        <div class="column is-4">
          <div class="field">
            <label class="label">Hora Início *</label>
            <div class="control">
              <input 
                v-model="novoHorario.horaInicio"
                class="input" 
                type="time" 
                required
                @change="atualizarHorarioFim"
              >
            </div>
          </div>
        </div>

        <div class="column is-4">
          <div class="field">
            <label class="label">Hora Fim *</label>
            <div class="control">
              <input 
                v-model="novoHorario.horaFim"
                class="input" 
                type="time" 
                required
              >
            </div>
          </div>
        </div>

        <div class="column is-12">
          <div class="field">
            <div class="control">
              <button 
                @click="adicionarHorario"
                class="button is-primary is-fullwidth"
                :disabled="submitting"
              >
                <span v-if="submitting" class="icon">
                  <i class="fas fa-spinner fa-spin"></i>
                </span>
                <span v-else class="icon">
                  <i class="fas fa-plus"></i>
                </span>
                <span>{{ submitting ? 'Adicionando...' : 'Adicionar Horário' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista de Horários -->
    <div class="box">
      <h2 class="title is-4 mb-4">Horários Disponíveis</h2>
      
      <div v-if="funcionarios.length === 0" class="has-text-centered py-6">
        <span class="icon is-large has-text-grey-light">
          <i class="fas fa-calendar"></i>
        </span>
        <p class="mt-3 has-text-grey">Nenhum funcionário cadastrado</p>
      </div>

      <div v-else>
        <div v-for="funcionario in funcionarios" :key="funcionario.id" class="mb-6">
          <h3 class="title is-5 mb-3">{{ funcionario.nome }}</h3>
          
          <div v-if="horariosPorFuncionario[funcionario.id]?.length > 0" class="table-container">
            <table class="table is-fullwidth is-striped">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Serviço</th>
                  <th>Hora Início</th>
                  <th>Hora Fim</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="horario in horariosPorFuncionario[funcionario.id]" :key="horario.id">
                  <td>{{ formatarData(horario.data) }}</td>
                  <td>{{ getServicoNome(horario.servicoId) }}</td>
                  <td>{{ horario.horaInicio }}</td>
                  <td>{{ horario.horaFim }}</td>
                  <td>
                    <button 
                      @click="removerHorario(horario.id)"
                      class="button is-danger is-small"
                    >
                      <span class="icon">
                        <i class="fas fa-trash"></i>
                      </span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-else class="has-text-centered py-4">
            <span class="icon has-text-grey-light">
              <i class="fas fa-calendar-times"></i>
            </span>
            <p class="mt-2 has-text-grey">Nenhum horário cadastrado para este funcionário</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.agenda-container {
  padding: 1rem;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.table-container {
  overflow-x: auto;
}

.buttons {
  margin: 0;
}

.button .icon {
  margin-right: 0;
}

.tag {
  min-width: 100px;
  justify-content: center;
}
</style> 
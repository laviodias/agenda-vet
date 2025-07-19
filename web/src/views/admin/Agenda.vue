<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'

const funcionarios = ref([
  { id: 1, nome: 'Dr. João Silva', especialidade: 'Clínico Geral' },
  { id: 2, nome: 'Dra. Maria Santos', especialidade: 'Dermatologia' }
])

const servicos = ref([
  { 
    id: 1, 
    nome: 'Consulta Clínica', 
    duracao: 30,
    especialidades: ['Clínico Geral']
  },
  { 
    id: 2, 
    nome: 'Banho e Tosa', 
    duracao: 60,
    especialidades: []
  }
])

const horariosDisponiveis = ref([
  { 
    id: 1, 
    funcionarioId: 1, 
    servicoId: 1,
    data: '2025-03-20', 
    horaInicio: '09:00', 
    horaFim: '09:30', 
    disponivel: true 
  },
  { 
    id: 2, 
    funcionarioId: 1, 
    servicoId: 1,
    data: '2025-03-20', 
    horaInicio: '10:00', 
    horaFim: '10:30', 
    disponivel: true 
  },
  { 
    id: 3, 
    funcionarioId: 2, 
    servicoId: 2,
    data: '2025-03-20', 
    horaInicio: '14:00', 
    horaFim: '15:00', 
    disponivel: true 
  }
])

const novoHorario = ref({
  funcionarioId: '',
  servicoId: '',
  data: '',
  horaInicio: '',
  horaFim: ''
})

const servicosPorFuncionario = computed(() => {
  const servicosDisponiveis = {}
  funcionarios.value.forEach(funcionario => {
    servicosDisponiveis[funcionario.id] = servicos.value.filter(servico => 
      servico.especialidades.length === 0 || 
      servico.especialidades.includes(funcionario.especialidade)
    )
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

const adicionarHorario = () => {
  if (!novoHorario.value.funcionarioId || !novoHorario.value.servicoId || 
      !novoHorario.value.data || !novoHorario.value.horaInicio || !novoHorario.value.horaFim) {
    alert('Por favor, preencha todos os campos')
    return
  }

  // Validar se o horário não conflita com outros horários
  const conflito = horariosDisponiveis.value.some(h => 
    h.funcionarioId === novoHorario.value.funcionarioId &&
    h.data === novoHorario.value.data &&
    ((novoHorario.value.horaInicio >= h.horaInicio && novoHorario.value.horaInicio < h.horaFim) ||
     (novoHorario.value.horaFim > h.horaInicio && novoHorario.value.horaFim <= h.horaFim))
  )

  if (conflito) {
    alert('Este horário conflita com outro horário já cadastrado')
    return
  }

  horariosDisponiveis.value.push({
    id: horariosDisponiveis.value.length + 1,
    ...novoHorario.value,
    disponivel: true
  })

  novoHorario.value = {
    funcionarioId: '',
    servicoId: '',
    data: '',
    horaInicio: '',
    horaFim: ''
  }
}

const removerHorario = (id) => {
  if (confirm('Tem certeza que deseja remover este horário?')) {
    horariosDisponiveis.value = horariosDisponiveis.value.filter(h => h.id !== id)
  }
}

const formatarData = (data) => {
  return new Date(data).toLocaleDateString('pt-BR')
}

const getServicoNome = (servicoId) => {
  const servico = servicos.value.find(s => s.id === servicoId)
  return servico ? servico.nome : 'Serviço não encontrado'
}
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

    <!-- Formulário de Horários -->
    <div class="box mb-6">
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
                    {{ funcionario.nome }} - {{ funcionario.especialidade }}
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

        <div class="column is-6">
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

        <div class="column is-6">
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

        <div class="column is-6">
          <div class="field">
            <label class="label">Hora Fim *</label>
            <div class="control">
              <input 
                v-model="novoHorario.horaFim"
                class="input" 
                type="time" 
                required
                readonly
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
              >
                <span class="icon">
                  <i class="fas fa-plus"></i>
                </span>
                <span>Adicionar Horário</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2 class="title is-4 mb-4">Horários Disponíveis</h2>
      
      <div v-for="funcionario in funcionarios" :key="funcionario.id" class="mb-5">
        <h3 class="title is-5 mb-3">{{ funcionario.nome }}</h3>
        <div class="table-container">
          <table class="table is-fullwidth is-striped">
            <thead>
              <tr>
                <th>Data</th>
                <th>Horário</th>
                <th>Serviço</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="horario in horariosPorFuncionario[funcionario.id]" :key="horario.id">
                <td>{{ formatarData(horario.data) }}</td>
                <td>{{ horario.horaInicio }} - {{ horario.horaFim }}</td>
                <td>{{ getServicoNome(horario.servicoId) }}</td>
                <td>
                  <span class="tag" :class="horario.disponivel ? 'is-success' : 'is-danger'">
                    {{ horario.disponivel ? 'Disponível' : 'Ocupado' }}
                  </span>
                </td>
                <td>
                  <div class="buttons are-small">
                    <button 
                      @click="removerHorario(horario.id)"
                      class="button is-danger"
                    >
                      <span class="icon">
                        <i class="fas fa-trash"></i>
                      </span>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!horariosPorFuncionario[funcionario.id]?.length">
                <td colspan="5" class="has-text-centered">
                  Nenhum horário cadastrado
                </td>
              </tr>
            </tbody>
          </table>
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
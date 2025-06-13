<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AgendamentoForm from '../components/AgendamentoForm.vue'

const router = useRouter()

const user = ref({
  nome: 'João Silva',
  email: 'joao@email.com'
})

const animais = ref([
  {
    id: 1,
    nome: 'Rex',
    especie: 'Cão',
    raca: 'Labrador',
    idade: '3 anos'
  },
  {
    id: 2,
    nome: 'Luna',
    especie: 'Gato',
    raca: 'Persa',
    idade: '2 anos'
  }
])

const agendamentos = ref([
  {
    id: 1,
    data: '2025-06-25',
    hora: '14:00',
    servico: 'Consulta Clínica',
    animal: 'Rex',
    status: 'confirmado'
  },
  {
    id: 2,
    data: '2025-06-28',
    hora: '10:30',
    servico: 'Vacinação',
    animal: 'Luna',
    status: 'pendente'
  }
])

const showAgendamentoForm = ref(false)

const logout = () => {
  // TODO: Implementar logout
  router.push('/auth')
}

const cancelarAgendamento = (id) => {
  if (confirm('Tem certeza que deseja cancelar este agendamento?')) {
    agendamentos.value = agendamentos.value.filter(a => a.id !== id)
  }
}

const formatarData = (data) => {
  return new Date(data).toLocaleDateString('pt-BR')
}

const getStatusColor = (status) => {
  return status === 'confirmado' ? 'is-success' : 'is-warning'
}

const getStatusText = (status) => {
  return status === 'confirmado' ? 'Confirmado' : 'Pendente'
}
</script>

<template>
  <div class="cliente-dashboard">
    <!-- Header -->
    <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <div class="navbar-item">
          <span class="icon-text">
            <span class="icon">
              <i class="fas fa-paw"></i>
            </span>
            <span>AgendaVet - Cliente</span>
          </span>
        </div>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item" @click="showAgendamentoForm = true">
            <span class="icon">
              <i class="fas fa-calendar-plus"></i>
            </span>
            <span>Novo Agendamento</span>
          </a>
        </div>

        <div class="navbar-end">
          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              <span class="icon">
                <i class="fas fa-user"></i>
              </span>
              <span>{{ user.nome }}</span>
            </a>

            <div class="navbar-dropdown is-right">
              <a class="navbar-item">
                <span class="icon">
                  <i class="fas fa-user-edit"></i>
                </span>
                <span>Meu Perfil</span>
              </a>
              <a class="navbar-item">
                <span class="icon">
                  <i class="fas fa-paw"></i>
                </span>
                <span>Meus Pets</span>
              </a>
              <hr class="navbar-divider">
              <a class="navbar-item" @click="logout">
                <span class="icon">
                  <i class="fas fa-sign-out-alt"></i>
                </span>
                <span>Sair</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-4">
      <!-- Welcome Section -->
      <div class="welcome-section mb-6">
        <h1 class="title is-2">Bem-vindo, {{ user.nome }}!</h1>
        <p class="subtitle">Gerencie seus agendamentos e pets</p>
      </div>

      <!-- Stats Cards -->
      <div class="columns mb-6">
        <div class="column">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <div class="stat-icon">
                    <i class="fas fa-calendar-check"></i>
                  </div>
                </div>
                <div class="media-content">
                  <p class="title is-4">{{ agendamentos.length }}</p>
                  <p class="subtitle is-6">Agendamentos</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <div class="stat-icon">
                    <i class="fas fa-paw"></i>
                  </div>
                </div>
                <div class="media-content">
                  <p class="title is-4">{{ animais.length }}</p>
                  <p class="subtitle is-6">Pets</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <div class="stat-icon">
                    <i class="fas fa-clock"></i>
                  </div>
                </div>
                <div class="media-content">
                  <p class="title is-4">{{ agendamentos.filter(a => a.status === 'pendente').length }}</p>
                  <p class="subtitle is-6">Pendentes</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Meus Pets -->
      <div class="section">
        <h2 class="title is-3 mb-4">Meus Pets</h2>
        <div class="columns is-multiline">
          <div 
            v-for="animal in animais" 
            :key="animal.id"
            class="column is-4"
          >
            <div class="card">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <div class="pet-avatar">
                      <i class="fas fa-paw"></i>
                    </div>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">{{ animal.nome }}</p>
                    <p class="subtitle is-6">{{ animal.especie }} - {{ animal.raca }}</p>
                    <p class="help">{{ animal.idade }}</p>
                  </div>
                </div>
              </div>
              <footer class="card-footer">
                <a class="card-footer-item">
                  <span class="icon">
                    <i class="fas fa-edit"></i>
                  </span>
                  <span>Editar</span>
                </a>
                <a class="card-footer-item">
                  <span class="icon">
                    <i class="fas fa-calendar-plus"></i>
                  </span>
                  <span>Agendar</span>
                </a>
              </footer>
            </div>
          </div>
        </div>
      </div>

      <!-- Próximos Agendamentos -->
      <div class="section">
        <h2 class="title is-3 mb-4">Próximos Agendamentos</h2>
        <div class="table-container">
          <table class="table is-fullwidth is-striped">
            <thead>
              <tr>
                <th>Data</th>
                <th>Horário</th>
                <th>Serviço</th>
                <th>Pet</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="agendamento in agendamentos" :key="agendamento.id">
                <td>{{ formatarData(agendamento.data) }}</td>
                <td>{{ agendamento.hora }}</td>
                <td>{{ agendamento.servico }}</td>
                <td>{{ agendamento.animal }}</td>
                <td>
                  <span class="tag" :class="getStatusColor(agendamento.status)">
                    {{ getStatusText(agendamento.status) }}
                  </span>
                </td>
                <td>
                  <div class="buttons are-small">
                    <button class="button is-info">
                      <span class="icon">
                        <i class="fas fa-eye"></i>
                      </span>
                    </button>
                    <button 
                      @click="cancelarAgendamento(agendamento.id)"
                      class="button is-danger"
                    >
                      <span class="icon">
                        <i class="fas fa-times"></i>
                      </span>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!agendamentos.length">
                <td colspan="6" class="has-text-centered">
                  Nenhum agendamento encontrado
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de Agendamento -->
    <div v-if="showAgendamentoForm" class="modal is-active">
      <div class="modal-background" @click="showAgendamentoForm = false"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Novo Agendamento</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="showAgendamentoForm = false"
          ></button>
        </header>
        <section class="modal-card-body">
          <AgendamentoForm />
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cliente-dashboard {
  min-height: 100vh;
  background: #f5f5f5;
}

.welcome-section {
  text-align: center;
  padding: 2rem 0;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2E7D32, #A5D6A7);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.pet-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #e8f5e8;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2E7D32;
  font-size: 1.25rem;
}

.card {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.modal-card {
  max-width: 800px;
  width: 90%;
}

.modal-card-body {
  max-height: 80vh;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .columns {
    margin: 0;
  }
  
  .column {
    padding: 0.5rem;
  }
  
  .table-container {
    overflow-x: auto;
  }
}
</style> 
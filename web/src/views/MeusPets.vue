<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBrand } from '../composables/useBrand.js'
import authService from '../services/authService.js'
import AgendamentoForm from '../components/AgendamentoForm.vue'

const router = useRouter()
const { brandConfig } = useBrand()

const animais = ref([])
const loading = ref(false)
const error = ref(null)
const success = ref(null)

const showAdicionarPetForm = ref(false)
const showEditarPetForm = ref(false)
const showAgendamentoForm = ref(false)
const petSelecionado = ref(null)
const novoPet = ref({
  nome: '',
  especie: 'Cão',
  raca: '',
  data_nascimento: '',
  peso: '',
  observacoes: ''
})

const especies = [
  'Cão', 'Gato', 'Ave', 'Réptil', 'Peixe', 'Hamster', 'Coelho', 'Outro'
]

// Carregar dados na montagem do componente
onMounted(async () => {
  await loadAnimais()
})

// Função para carregar animais da API
const loadAnimais = async () => {
  try {
    loading.value = true
    error.value = null
    
    const animaisData = await authService.getPets()
    animais.value = Array.isArray(animaisData) ? animaisData : []
    
  } catch (err) {
    console.error('Erro ao carregar animais:', err)
    error.value = 'Erro ao carregar animais. Tente novamente.'
    animais.value = []
  } finally {
    loading.value = false
  }
}

const adicionarPet = async () => {
  try {
    // Validar dados obrigatórios
    if (!novoPet.value.nome || !novoPet.value.especie) {
      error.value = 'Nome e espécie são obrigatórios'
      return
    }

    // Preparar dados para a API
    const petData = {
      nome: novoPet.value.nome,
      especie: novoPet.value.especie,
      raca: novoPet.value.raca || '',
      data_nascimento: novoPet.value.data_nascimento || null,
      peso: novoPet.value.peso || '',
      observacoes: novoPet.value.observacoes || ''
    }

    // Chamar API para criar pet
    const novoPetCriado = await authService.createPet(petData)
    
    // Adicionar à lista local
    animais.value.push(novoPetCriado)
    
    // Limpar formulário
    novoPet.value = {
      nome: '',
      especie: 'Cão',
      raca: '',
      data_nascimento: '',
      peso: '',
      observacoes: ''
    }
    
    showAdicionarPetForm.value = false
    error.value = null
    success.value = 'Pet adicionado com sucesso!'
    
    // Limpar mensagem de sucesso após 3 segundos
    setTimeout(() => {
      success.value = null
    }, 3000)
  } catch (err) {
    console.error('Erro ao adicionar pet:', err)
    error.value = 'Erro ao adicionar pet. Tente novamente.'
  }
}

const editarPet = (animal) => {
  petSelecionado.value = { ...animal }
  showEditarPetForm.value = true
}

const salvarPet = async () => {
  try {
    // Validar dados obrigatórios
    if (!petSelecionado.value.nome || !petSelecionado.value.especie) {
      error.value = 'Nome e espécie são obrigatórios'
      return
    }

    // Preparar dados para a API
    const petData = {
      nome: petSelecionado.value.nome,
      especie: petSelecionado.value.especie,
      raca: petSelecionado.value.raca || '',
      data_nascimento: petSelecionado.value.data_nascimento || null,
      peso: petSelecionado.value.peso || '',
      observacoes: petSelecionado.value.observacoes || ''
    }

    // Chamar API para atualizar pet
    const petAtualizado = await authService.updatePet(petSelecionado.value.id, petData)
    
    // Atualizar na lista local
    const index = animais.value.findIndex(a => a.id === petSelecionado.value.id)
    if (index !== -1) {
      animais.value[index] = petAtualizado
    }
    
    showEditarPetForm.value = false
    petSelecionado.value = null
    error.value = null
    success.value = 'Pet atualizado com sucesso!'
    
    // Limpar mensagem de sucesso após 3 segundos
    setTimeout(() => {
      success.value = null
    }, 3000)
  } catch (err) {
    console.error('Erro ao salvar pet:', err)
    error.value = 'Erro ao salvar pet. Tente novamente.'
  }
}

const removerPet = async (id) => {
  if (confirm('Tem certeza que deseja remover este pet?')) {
    try {
      // Chamar API para deletar pet
      await authService.deletePet(id)
      
      // Remover da lista local
      animais.value = animais.value.filter(a => a.id !== id)
      error.value = null
      success.value = 'Pet removido com sucesso!'
      
      // Limpar mensagem de sucesso após 3 segundos
      setTimeout(() => {
        success.value = null
      }, 3000)
    } catch (err) {
      console.error('Erro ao remover pet:', err)
      error.value = 'Erro ao remover pet. Tente novamente.'
    }
  }
}

const cancelarEdicaoPet = () => {
  showEditarPetForm.value = false
  petSelecionado.value = null
}

const cancelarAdicaoPet = () => {
  showAdicionarPetForm.value = false
  novoPet.value = {
    nome: '',
    especie: 'Cão',
    raca: '',
    data_nascimento: '',
    peso: '',
    observacoes: ''
  }
}

const voltar = () => {
  router.push('/cliente')
}

const agendarParaPet = (animal) => {
  petSelecionado.value = animal
  showAgendamentoForm.value = true
}

const fecharModalAgendamento = () => {
  showAgendamentoForm.value = false
  petSelecionado.value = null
}

const handleAgendamentoCriado = (agendamento) => {
  console.log('Agendamento criado:', agendamento)
  // Aqui você pode adicionar lógica adicional, como mostrar uma mensagem de sucesso
  fecharModalAgendamento()
}

const calcularIdade = (dataNascimento) => {
  if (!dataNascimento) return 'Idade não informada'
  
  const hoje = new Date()
  const nascimento = new Date(dataNascimento)
  const diffTime = Math.abs(hoje - nascimento)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  const anos = Math.floor(diffDays / 365)
  const meses = Math.floor((diffDays % 365) / 30)
  
  if (anos > 0) {
    return `${anos} ano${anos > 1 ? 's' : ''}${meses > 0 ? ` e ${meses} mes${meses > 1 ? 'es' : ''}` : ''}`
  } else {
    return `${meses} mes${meses > 1 ? 'es' : ''}`
  }
}
</script>

<template>
  <div class="meus-pets-page">
    <!-- Header -->
    <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <div class="navbar-item">
          <span class="icon-text">
            <span class="icon">
              <i class="fas fa-paw"></i>
            </span>
            <span>{{ brandConfig?.nome_estabelecimento || 'AgendaVet' }} - Meus Pets</span>
          </span>
        </div>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item" @click="voltar">
            <span class="icon">
              <i class="fas fa-arrow-left"></i>
            </span>
            <span>Voltar</span>
          </a>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-4">
      <!-- Header da página -->
      <div class="welcome-section mb-6">
        <div class="columns is-vcentered">
          <div class="column">
            <h1 class="title is-2">Meus Pets</h1>
            <p class="subtitle">Gerencie seus animais de estimação</p>
          </div>
          <div class="column is-narrow">
            <div class="buttons">
              <button 
                class="button is-primary is-medium"
                @click="showAdicionarPetForm = true"
              >
                <span class="icon">
                  <i class="fas fa-plus"></i>
                </span>
                <span>Adicionar Pet</span>
              </button>
              <button 
                class="button is-info is-medium"
                @click="router.push('/perfil')"
              >
                <span class="icon">
                  <i class="fas fa-user"></i>
                </span>
                <span>Meu Perfil</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Mensagens de feedback -->
      <div v-if="error" class="notification is-danger is-light mb-4">
        <button class="delete" @click="error = null"></button>
        {{ error }}
      </div>

      <div v-if="success" class="notification is-success is-light mb-4">
        <button class="delete" @click="success = null"></button>
        {{ success }}
      </div>

      <!-- Lista de Pets -->
      <div v-if="loading" class="loading-state">
        <div class="has-text-centered">
          <span class="icon is-large">
            <i class="fas fa-spinner fa-spin"></i>
          </span>
          <p class="mt-3">Carregando pets...</p>
        </div>
      </div>

      <div v-else-if="error" class="error-state">
        <div class="has-text-centered">
          <span class="icon is-large has-text-danger">
            <i class="fas fa-exclamation-triangle"></i>
          </span>
          <p class="mt-3">{{ error }}</p>
          <button class="button is-primary mt-3" @click="loadAnimais">
            Tentar Novamente
          </button>
        </div>
      </div>

      <div v-else>
        <div class="columns is-multiline">
          <div 
            v-for="animal in animais" 
            :key="animal.id"
            class="column is-4"
          >
            <div class="card pet-card">
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
                    <p class="help">{{ calcularIdade(animal.data_nascimento) }} • {{ animal.peso }}</p>
                    <p v-if="animal.observacoes" class="help mt-2">
                      <strong>Observações:</strong> {{ animal.observacoes }}
                    </p>
                  </div>
                </div>
              </div>
              
              <footer class="card-footer">
                <a class="card-footer-item" @click="editarPet(animal)">
                  <span class="icon">
                    <i class="fas fa-edit"></i>
                  </span>
                  <span>Editar</span>
                </a>
                <a class="card-footer-item" @click="agendarParaPet(animal)">
                  <span class="icon">
                    <i class="fas fa-calendar-plus"></i>
                  </span>
                  <span>Agendar</span>
                </a>
                <a 
                  class="card-footer-item has-text-danger" 
                  @click="removerPet(animal.id)"
                >
                  <span class="icon">
                    <i class="fas fa-trash"></i>
                  </span>
                  <span>Remover</span>
                </a>
              </footer>
            </div>
          </div>
        </div>

        <!-- Mensagem quando não há pets -->
        <div v-if="!loading && !error && !animais.length" class="has-text-centered mt-6">
          <div class="empty-state">
            <span class="icon is-large">
              <i class="fas fa-paw"></i>
            </span>
            <h3 class="title is-4 mt-4">Nenhum pet cadastrado</h3>
            <p class="subtitle is-6">Adicione seu primeiro pet para começar a agendar consultas</p>
            <button 
              class="button is-primary mt-4"
              @click="showAdicionarPetForm = true"
            >
              <span class="icon">
                <i class="fas fa-plus"></i>
              </span>
              <span>Adicionar Primeiro Pet</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Adicionar Pet -->
    <div v-if="showAdicionarPetForm" class="modal is-active">
      <div class="modal-background" @click="cancelarAdicaoPet"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Adicionar Novo Pet</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="cancelarAdicaoPet"
          ></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Nome do Pet</label>
            <div class="control">
              <input 
                class="input" 
                type="text" 
                v-model="novoPet.nome"
                placeholder="Nome do pet"
              >
            </div>
          </div>
          
          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Espécie</label>
                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="novoPet.especie">
                      <option v-for="especie in especies" :key="especie" :value="especie">
                        {{ especie }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="column is-6">
              <div class="field">
                <label class="label">Raça</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="novoPet.raca"
                    placeholder="Raça do pet"
                  >
                </div>
              </div>
            </div>
          </div>
          
          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Data de Nascimento</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="date" 
                    v-model="novoPet.data_nascimento"
                  >
                </div>
              </div>
            </div>
            
            <div class="column is-6">
              <div class="field">
                <label class="label">Peso</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="novoPet.peso"
                    placeholder="Ex: 25 kg"
                  >
                </div>
              </div>
            </div>
          </div>
          
          <div class="field">
            <label class="label">Observações</label>
            <div class="control">
              <textarea 
                class="textarea" 
                v-model="novoPet.observacoes"
                placeholder="Alguma observação importante sobre o pet..."
                rows="3"
              ></textarea>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="adicionarPet">Adicionar Pet</button>
          <button class="button" @click="cancelarAdicaoPet">Cancelar</button>
        </footer>
      </div>
    </div>

    <!-- Modal de Edição de Pet -->
    <div v-if="showEditarPetForm" class="modal is-active">
      <div class="modal-background" @click="cancelarEdicaoPet"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Editar Pet</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="cancelarEdicaoPet"
          ></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Nome do Pet</label>
            <div class="control">
              <input 
                class="input" 
                type="text" 
                v-model="petSelecionado.nome"
                placeholder="Nome do pet"
              >
            </div>
          </div>
          
          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Espécie</label>
                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="petSelecionado.especie">
                      <option v-for="especie in especies" :key="especie" :value="especie">
                        {{ especie }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="column is-6">
              <div class="field">
                <label class="label">Raça</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="petSelecionado.raca"
                    placeholder="Raça do pet"
                  >
                </div>
              </div>
            </div>
          </div>
          
          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Data de Nascimento</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="date" 
                    v-model="petSelecionado.data_nascimento"
                  >
                </div>
              </div>
            </div>
            
            <div class="column is-6">
              <div class="field">
                <label class="label">Peso</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="petSelecionado.peso"
                    placeholder="Ex: 25 kg"
                  >
                </div>
              </div>
            </div>
          </div>
          
          <div class="field">
            <label class="label">Observações</label>
            <div class="control">
              <textarea 
                class="textarea" 
                v-model="petSelecionado.observacoes"
                placeholder="Alguma observação importante sobre o pet..."
                rows="3"
              ></textarea>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="salvarPet">Salvar</button>
          <button class="button" @click="cancelarEdicaoPet">Cancelar</button>
        </footer>
      </div>
    </div>

    <!-- Modal de Agendamento -->
    <div v-if="showAgendamentoForm" class="modal is-active">
      <div class="modal-background" @click="fecharModalAgendamento"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Agendar Atendimento para {{ petSelecionado?.nome }}</p>
          <button 
            class="delete" 
            aria-label="close"
            @click="fecharModalAgendamento"
          ></button>
        </header>
        <section class="modal-card-body">
          <AgendamentoForm
            :petSelecionado="petSelecionado"
            :pets="animais"
            @close="fecharModalAgendamento"
            @agendamentoCriado="handleAgendamentoCriado"
          />
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.meus-pets-page {
  min-height: 100vh;
  background: #f8f9fa;
}

.welcome-section {
  text-align: center;
  padding: 2rem 0;
}

.pet-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #e9ecef;
}

.pet-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.table-container {
  background: var(--background-color);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.table {
  background: white;
}

.table thead th {
  background: var(--background-color);
  color: var(--text-color);
  font-weight: 600;
  border-bottom: 2px solid var(--border-color);
}

.table tbody tr:hover {
  background-color: var(--background-color);
}

.pet-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--info-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}

.pet-info {
  color: var(--text-color);
}

.pet-link {
  color: var(--primary-color);
  text-decoration: none;
}

.pet-link:hover {
  text-decoration: underline;
}

.card-footer-item {
  cursor: pointer;
  transition: background-color 0.2s;
  color: #495057;
}

.card-footer-item:hover {
  background-color: #f8f9fa;
  color: #007bff;
}

.card-footer-item:active {
  background-color: #e9ecef;
}

.card-footer-item.has-text-danger:hover {
  color: #dc3545 !important;
}

.empty-state {
  padding: 4rem 2rem;
  color: #6c757d;
}

.empty-state .icon {
  color: #dee2e6;
  font-size: 1rem;
}

.modal-card {
  max-width: 800px;
  width: 95%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-card-body {
  max-height: 80vh;
  overflow-y: auto;
}

.modal-card-foot {
  padding: 1rem 1.5rem;
  background: var(--background-color);
  border-top: 1px solid var(--border-color);
}

.modal-card-foot .button {
  margin-right: 0.5rem;
}

.modal-card-foot .button:last-child {
  margin-right: 0;
}

/* Melhorias nos botões */
.button.is-primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.button.is-primary:hover {
  background-color: var(--primary-color);
  filter: brightness(0.9);
}

.button.is-info {
  background-color: var(--info-color);
  border-color: var(--info-color);
}

.button.is-info:hover {
  background-color: var(--info-color);
  filter: brightness(0.9);
}

.button.is-success {
  background-color: var(--success-color);
  border-color: var(--success-color);
}

.button.is-success:hover {
  background-color: var(--success-color);
  filter: brightness(0.9);
}

.button.is-danger {
  background-color: var(--danger-color);
  border-color: var(--danger-color);
}

.button.is-danger:hover {
  background-color: var(--danger-color);
  filter: brightness(0.9);
}

/* Melhorias nos campos de formulário */
.input, .select select, .textarea {
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

.input:focus, .select select:focus, .textarea:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Melhorias nos labels */
.label {
  color: var(--text-color);
  font-weight: 600;
}

/* Melhorias na navbar */
.navbar.is-primary {
  background-color: var(--primary-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.loading-state, .error-state {
  padding: 4rem 0;
  background-color: var(--background-color);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.loading-state .icon, .error-state .icon {
  color: var(--border-color);
  font-size: 4rem;
}

.loading-state p, .error-state p {
  color: var(--text-color);
  font-size: 1.1rem;
}

.loading-state .button, .error-state .button {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.loading-state .button:hover, .error-state .button:hover {
  background-color: var(--primary-color);
  filter: brightness(0.9);
}

@media (max-width: 768px) {
  .columns {
    margin: 0;
  }
  
  .column {
    padding: 0.5rem;
  }
  
  .modal-card-foot .button {
    margin-bottom: 0.5rem;
    width: 100%;
  }
  
  .modal-card-foot .button:last-child {
    margin-bottom: 0;
  }
}
</style> 
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBrand } from '../composables/useBrand.js'

const router = useRouter()
const { brandConfig } = useBrand()

const animais = ref([
  {
    id: 1,
    nome: 'Rex',
    especie: 'Cão',
    raca: 'Labrador',
    idade: '3 anos',
    peso: '25 kg',
    observacoes: 'Alérgico a alguns alimentos'
  },
  {
    id: 2,
    nome: 'Luna',
    especie: 'Gato',
    raca: 'Persa',
    idade: '2 anos',
    peso: '4 kg',
    observacoes: 'Gosta de brincar com bolinhas'
  }
])

const showAdicionarPetForm = ref(false)
const showEditarPetForm = ref(false)
const petSelecionado = ref(null)
const novoPet = ref({
  nome: '',
  especie: 'Cão',
  raca: '',
  idade: '',
  peso: '',
  observacoes: ''
})

const especies = [
  'Cão', 'Gato', 'Ave', 'Réptil', 'Peixe', 'Hamster', 'Coelho', 'Outro'
]

const adicionarPet = () => {
  const pet = {
    id: Date.now(), // ID temporário
    ...novoPet.value
  }
  animais.value.push(pet)
  
  // Limpar formulário
  novoPet.value = {
    nome: '',
    especie: 'Cão',
    raca: '',
    idade: '',
    peso: '',
    observacoes: ''
  }
  
  showAdicionarPetForm.value = false
}

const editarPet = (animal) => {
  petSelecionado.value = { ...animal }
  showEditarPetForm.value = true
}

const salvarPet = () => {
  const index = animais.value.findIndex(a => a.id === petSelecionado.value.id)
  if (index !== -1) {
    animais.value[index] = { ...petSelecionado.value }
  }
  showEditarPetForm.value = false
  petSelecionado.value = null
}

const removerPet = (id) => {
  if (confirm('Tem certeza que deseja remover este pet?')) {
    animais.value = animais.value.filter(a => a.id !== id)
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
    idade: '',
    peso: '',
    observacoes: ''
  }
}

const voltar = () => {
  router.push('/cliente')
}

const agendarParaPet = (animal) => {
  // Navegar para o dashboard com o pet selecionado para agendamento
  router.push({ path: '/cliente', query: { agendarPet: animal.id } })
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

      <!-- Lista de Pets -->
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
                  <p class="help">{{ animal.idade }} • {{ animal.peso }}</p>
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
      <div v-if="!animais.length" class="has-text-centered mt-6">
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
                <label class="label">Idade</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="novoPet.idade"
                    placeholder="Ex: 3 anos, 6 meses"
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
                <label class="label">Idade</label>
                <div class="control">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="petSelecionado.idade"
                    placeholder="Ex: 3 anos, 6 meses"
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
  </div>
</template>

<style scoped>
.meus-pets-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.welcome-section {
  text-align: center;
  padding: 2rem 0;
}

.pet-card {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.pet-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
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

.card-footer-item {
  cursor: pointer;
  transition: background-color 0.2s;
}

.card-footer-item:hover {
  background-color: #f5f5f5;
}

.card-footer-item:active {
  background-color: #e8e8e8;
}

.empty-state {
  padding: 4rem 2rem;
  color: #666;
}

.empty-state .icon {
  color: #ddd;
  font-size: 4rem;
}

.modal-card {
  max-width: 600px;
  width: 95%;
}

@media (max-width: 768px) {
  .columns {
    margin: 0;
  }
  
  .column {
    padding: 0.5rem;
  }
}
</style> 
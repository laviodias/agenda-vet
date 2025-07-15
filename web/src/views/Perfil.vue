<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBrand } from '../composables/useBrand.js'

const router = useRouter()
const { brandConfig } = useBrand()

const user = ref({
  nome: 'João Silva',
  email: 'joao@email.com',
  telefone: '(11) 99999-9999',
  cpf: '123.456.789-00',
  endereco: {
    rua: 'Rua das Flores, 123',
    bairro: 'Centro',
    cidade: 'São Paulo',
    estado: 'SP',
    cep: '01234-567'
  }
})

const editando = ref(false)
const dadosEditados = ref({})

const iniciarEdicao = () => {
  dadosEditados.value = { ...user.value }
  editando.value = true
}

const salvarPerfil = () => {
  user.value = { ...dadosEditados.value }
  editando.value = false
}

const cancelarEdicao = () => {
  dadosEditados.value = { ...user.value }
  editando.value = false
}

const voltar = () => {
  router.push('/cliente')
}
</script>

<template>
  <div class="perfil-page">
    <!-- Header -->
    <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <div class="navbar-item">
          <span class="icon-text">
            <span class="icon">
              <i class="fas fa-paw"></i>
            </span>
            <span>{{ brandConfig?.nome_estabelecimento || 'AgendaVet' }} - Meu Perfil</span>
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
      <div class="columns">
        <div class="column is-8 is-offset-2">
          <!-- Header da página -->
          <div class="welcome-section mb-6">
            <h1 class="title is-2">Meu Perfil</h1>
            <p class="subtitle">Gerencie suas informações pessoais</p>
          </div>

          <!-- Card do perfil -->
          <div class="card">
            <header class="card-header">
              <p class="card-header-title">
                <span class="icon">
                  <i class="fas fa-user"></i>
                </span>
                <span>Informações Pessoais</span>
              </p>
              <div class="card-header-icon">
                <button 
                  v-if="!editando"
                  class="button is-primary is-small"
                  @click="iniciarEdicao"
                >
                  <span class="icon">
                    <i class="fas fa-edit"></i>
                  </span>
                  <span>Editar</span>
                </button>
                <div v-else class="buttons">
                  <button 
                    class="button is-success is-small"
                    @click="salvarPerfil"
                  >
                    <span class="icon">
                      <i class="fas fa-save"></i>
                    </span>
                    <span>Salvar</span>
                  </button>
                  <button 
                    class="button is-small"
                    @click="cancelarEdicao"
                  >
                    <span class="icon">
                      <i class="fas fa-times"></i>
                    </span>
                    <span>Cancelar</span>
                  </button>
                </div>
              </div>
            </header>

            <div class="card-content">
              <div class="columns">
                <div class="column is-6">
                  <div class="field">
                    <label class="label">Nome Completo</label>
                    <div class="control">
                      <input 
                        class="input" 
                        type="text" 
                        :value="editando ? dadosEditados.nome : user.nome"
                        :disabled="!editando"
                        @input="editando && (dadosEditados.nome = $event.target.value)"
                        placeholder="Seu nome completo"
                      >
                    </div>
                  </div>
                </div>

                <div class="column is-6">
                  <div class="field">
                    <label class="label">E-mail</label>
                    <div class="control">
                      <input 
                        class="input" 
                        type="email" 
                        :value="editando ? dadosEditados.email : user.email"
                        :disabled="!editando"
                        @input="editando && (dadosEditados.email = $event.target.value)"
                        placeholder="seu@email.com"
                      >
                    </div>
                  </div>
                </div>
              </div>

              <div class="columns">
                <div class="column is-6">
                  <div class="field">
                    <label class="label">Telefone</label>
                    <div class="control">
                      <input 
                        class="input" 
                        type="tel" 
                        :value="editando ? dadosEditados.telefone : user.telefone"
                        :disabled="!editando"
                        @input="editando && (dadosEditados.telefone = $event.target.value)"
                        placeholder="(11) 99999-9999"
                      >
                    </div>
                  </div>
                </div>

                <div class="column is-6">
                  <div class="field">
                    <label class="label">CPF</label>
                    <div class="control">
                      <input 
                        class="input" 
                        type="text" 
                        :value="editando ? dadosEditados.cpf : user.cpf"
                        :disabled="!editando"
                        @input="editando && (dadosEditados.cpf = $event.target.value)"
                        placeholder="123.456.789-00"
                      >
                    </div>
                  </div>
                </div>
              </div>

              <!-- Endereço -->
              <div class="section">
                <h3 class="title is-4">Endereço</h3>
                
                <div class="field">
                  <label class="label">Rua e Número</label>
                  <div class="control">
                    <input 
                      class="input" 
                      type="text" 
                      :value="editando ? dadosEditados.endereco.rua : user.endereco.rua"
                      :disabled="!editando"
                      @input="editando && (dadosEditados.endereco.rua = $event.target.value)"
                      placeholder="Rua das Flores, 123"
                    >
                  </div>
                </div>

                <div class="columns">
                  <div class="column is-4">
                    <div class="field">
                      <label class="label">Bairro</label>
                      <div class="control">
                        <input 
                          class="input" 
                          type="text" 
                          :value="editando ? dadosEditados.endereco.bairro : user.endereco.bairro"
                          :disabled="!editando"
                          @input="editando && (dadosEditados.endereco.bairro = $event.target.value)"
                          placeholder="Centro"
                        >
                      </div>
                    </div>
                  </div>

                  <div class="column is-4">
                    <div class="field">
                      <label class="label">Cidade</label>
                      <div class="control">
                        <input 
                          class="input" 
                          type="text" 
                          :value="editando ? dadosEditados.endereco.cidade : user.endereco.cidade"
                          :disabled="!editando"
                          @input="editando && (dadosEditados.endereco.cidade = $event.target.value)"
                          placeholder="São Paulo"
                        >
                      </div>
                    </div>
                  </div>

                  <div class="column is-2">
                    <div class="field">
                      <label class="label">Estado</label>
                      <div class="control">
                        <input 
                          class="input" 
                          type="text" 
                          :value="editando ? dadosEditados.endereco.estado : user.endereco.estado"
                          :disabled="!editando"
                          @input="editando && (dadosEditados.endereco.estado = $event.target.value)"
                          placeholder="SP"
                        >
                      </div>
                    </div>
                  </div>

                  <div class="column is-2">
                    <div class="field">
                      <label class="label">CEP</label>
                      <div class="control">
                        <input 
                          class="input" 
                          type="text" 
                          :value="editando ? dadosEditados.endereco.cep : user.endereco.cep"
                          :disabled="!editando"
                          @input="editando && (dadosEditados.endereco.cep = $event.target.value)"
                          placeholder="01234-567"
                        >
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Botões de ação -->
          <div class="buttons mt-5">
            <button class="button is-primary" @click="voltar">
              <span class="icon">
                <i class="fas fa-arrow-left"></i>
              </span>
              <span>Voltar ao Dashboard</span>
            </button>
            <button class="button is-info" @click="router.push('/meus-pets')">
              <span class="icon">
                <i class="fas fa-paw"></i>
              </span>
              <span>Gerenciar Meus Pets</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.perfil-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.welcome-section {
  text-align: center;
  padding: 2rem 0;
}

.card {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.card-header-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.field {
  margin-bottom: 1.5rem;
}

.section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

@media (max-width: 768px) {
  .column {
    padding: 0.5rem;
  }
}
</style> 
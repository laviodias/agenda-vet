<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService.js'

const router = useRouter()

const registerData = reactive({
  nome: '',
  email: '',
  senha: '',
  confirmarSenha: '',
  telefone: ''
})

const animalData = reactive({
  nome: '',
  especie: '',
  raca: '',
  dataNascimento: '',
  peso: '',
  observacoes: ''
})

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const step = ref(1)

const especies = ['Cão', 'Gato', 'Ave', 'Réptil', 'Peixe', 'Outro']

const racas = {
  'Cão': ['Labrador', 'Golden Retriever', 'Poodle', 'Bulldog', 'Pastor Alemão', 'Outro'],
  'Gato': ['Persa', 'Siamês', 'Maine Coon', 'Sphynx', 'Ragdoll', 'Outro'],
  'Ave': ['Canário', 'Periquito', 'Cacatua', 'Papagaio', 'Outro'],
  'Réptil': ['Iguana', 'Tartaruga', 'Cobra', 'Lagarto', 'Outro'],
  'Peixe': ['Betta', 'Dourado', 'Tetra', 'Outro'],
  'Outro': ['Outro']
}

const validateForm = () => {
  if (!registerData.nome || !registerData.email || !registerData.telefone || !registerData.senha || !registerData.confirmarSenha) {
    errorMessage.value = 'Por favor, preencha todos os campos obrigatórios'
    return false
  }

  if (registerData.senha !== registerData.confirmarSenha) {
    errorMessage.value = 'As senhas não coincidem'
    return false
  }

  if (registerData.senha.length < 6) {
    errorMessage.value = 'A senha deve ter pelo menos 6 caracteres'
    return false
  }

  return true
}

const validateAnimal = () => {
  if (!animalData.nome || !animalData.especie) {
    errorMessage.value = 'Por favor, preencha o nome e espécie do animal'
    return false
  }
  return true
}

const nextStep = () => {
  if (!validateForm()) return
  step.value = 2
  errorMessage.value = ''
}

const previousStep = () => {
  step.value = 1
  errorMessage.value = ''
}

const handleRegister = async () => {
  if (!validateAnimal()) return

  loading.value = true
  errorMessage.value = ''

  try {
    const dadosCliente = {
      nome: registerData.nome,
      email: registerData.email,
      telefone: registerData.telefone,
      senha: registerData.senha,
      pet: {
        nome: animalData.nome,
        especie: animalData.especie,
        raca: animalData.raca,
        data_nascimento: animalData.dataNascimento
      }
    }

    const response = await authService.registerCliente(dadosCliente)
    
    // Salvar dados do usuário se houver token
    if (response.usuario) {
      authService.setCurrentUser(response.usuario)
    }
    
    successMessage.value = 'Cadastro realizado com sucesso! Redirecionando...'
    
    setTimeout(() => {
      router.push('/cliente')
    }, 2000)
  } catch (error) {
    console.error('Erro no registro:', error)
    if (error.response?.data) {
      // Tratar erros específicos da API
      if (error.response.data.email) {
        errorMessage.value = error.response.data.email[0]
      } else if (error.response.data.senha) {
        errorMessage.value = error.response.data.senha[0]
      } else if (error.response.data.nome) {
        errorMessage.value = error.response.data.nome[0]
      } else if (error.response.data.telefone) {
        errorMessage.value = error.response.data.telefone[0]
      } else if (error.response.data.pet) {
        errorMessage.value = 'Erro nos dados do pet: ' + Object.values(error.response.data.pet).flat().join(', ')
      } else {
        errorMessage.value = 'Erro ao realizar cadastro. Verifique os dados informados.'
      }
    } else {
      errorMessage.value = 'Erro ao conectar com o servidor. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}

const togglePasswordVisibility = (field) => {
  if (field === 'password') {
    showPassword.value = !showPassword.value
  } else {
    showConfirmPassword.value = !showConfirmPassword.value
  }
}

const formatPhone = (value) => {
  return value
    .replace(/\D/g, '')
    .replace(/(\d{2})(\d)/, '($1) $2')
    .replace(/(\d{5})(\d)/, '$1-$2')
    .replace(/(-\d{4})\d+?$/, '$1')
}
</script>

<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <div class="logo">
          <i class="fas fa-paw"></i>
        </div>
        <h1 class="title is-3">Cadastre-se no AgendaVet</h1>
        <p class="subtitle">Crie sua conta e agende consultas para seu pet</p>
        
        <div class="steps">
          <div class="step" :class="{ 'is-active': step >= 1, 'is-completed': step > 1 }">
            <div class="step-number">1</div>
            <div class="step-label">Dados Pessoais</div>
          </div>
          <div class="step-line"></div>
          <div class="step" :class="{ 'is-active': step >= 2 }">
            <div class="step-number">2</div>
            <div class="step-label">Seu Pet</div>
          </div>
        </div>
      </div>

      <form v-if="step === 1" @submit.prevent="nextStep" class="register-form">
        <div class="field">
          <label class="label">Nome Completo *</label>
          <div class="control has-icons-left">
            <input 
              v-model="registerData.nome"
              class="input" 
              type="text" 
              placeholder="Seu nome completo"
              required
            >
            <span class="icon is-small is-left">
              <i class="fas fa-user"></i>
            </span>
          </div>
        </div>

        <div class="field">
          <label class="label">E-mail *</label>
          <div class="control has-icons-left">
            <input 
              v-model="registerData.email"
              class="input" 
              type="email" 
              placeholder="seu@email.com"
              required
            >
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
          </div>
        </div>

        <div class="field">
          <label class="label">Telefone *</label>
          <div class="control has-icons-left">
            <input 
              v-model="registerData.telefone"
              class="input" 
              type="text" 
              placeholder="(00) 00000-0000"
              maxlength="15"
              required
              @input="registerData.telefone = formatPhone(registerData.telefone)"
            >
            <span class="icon is-small is-left">
              <i class="fas fa-phone"></i>
            </span>
          </div>
        </div>

        <div class="field">
          <label class="label">Senha *</label>
          <div class="control has-icons-left has-icons-right">
            <input 
              v-model="registerData.senha"
              :type="showPassword ? 'text' : 'password'"
              class="input" 
              placeholder="Mínimo 6 caracteres"
              required
            >
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
            <span class="icon is-small is-right password-toggle" @click="togglePasswordVisibility('password')">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
          </div>
        </div>

        <div class="field">
          <label class="label">Confirmar Senha *</label>
          <div class="control has-icons-left has-icons-right">
            <input 
              v-model="registerData.confirmarSenha"
              :type="showConfirmPassword ? 'text' : 'password'"
              class="input" 
              placeholder="Confirme sua senha"
              required
            >
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
            <span class="icon is-small is-right password-toggle" @click="togglePasswordVisibility('confirm')">
              <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
          </div>
        </div>

        <div v-if="errorMessage" class="notification is-danger is-light">
          <i class="fas fa-exclamation-triangle"></i>
          {{ errorMessage }}
        </div>

        <div class="field">
          <div class="control">
            <button type="submit" class="button is-primary is-fullwidth">
              <span class="icon">
                <i class="fas fa-arrow-right"></i>
              </span>
              <span>Próximo</span>
            </button>
          </div>
        </div>
      </form>

      <form v-if="step === 2" @submit.prevent="handleRegister" class="register-form">
        <div class="field">
          <label class="label">Nome do Pet *</label>
          <div class="control has-icons-left">
            <input 
              v-model="animalData.nome"
              class="input" 
              type="text" 
              placeholder="Nome do seu pet"
              required
            >
            <span class="icon is-small is-left">
              <i class="fas fa-paw"></i>
            </span>
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <div class="field">
              <label class="label">Espécie *</label>
              <div class="control">
                <div class="select is-fullwidth">
                  <select v-model="animalData.especie" required>
                    <option value="">Selecione</option>
                    <option v-for="especie in especies" :key="especie" :value="especie">
                      {{ especie }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div class="column">
            <div class="field">
              <label class="label">Raça</label>
              <div class="control">
                <div class="select is-fullwidth">
                  <select v-model="animalData.raca">
                    <option value="">Selecione</option>
                    <option v-for="raca in racas[animalData.especie] || []" :key="raca" :value="raca">
                      {{ raca }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <div class="field">
              <label class="label">Data de Nascimento</label>
              <div class="control has-icons-left">
                <input 
                  v-model="animalData.dataNascimento"
                  class="input" 
                  type="date"
                >
                <span class="icon is-small is-left">
                  <i class="fas fa-calendar"></i>
                </span>
              </div>
            </div>
          </div>
          <div class="column">
            <div class="field">
              <label class="label">Peso (kg)</label>
              <div class="control has-icons-left">
                <input 
                  v-model="animalData.peso"
                  class="input" 
                  type="number" 
                  step="0.1"
                  placeholder="0.0"
                >
                <span class="icon is-small is-left">
                  <i class="fas fa-weight"></i>
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="field">
          <label class="label">Observações</label>
          <div class="control">
            <textarea 
              v-model="animalData.observacoes"
              class="textarea" 
              placeholder="Alguma informação adicional sobre seu pet..."
              rows="3"
            ></textarea>
          </div>
        </div>

        <div v-if="errorMessage" class="notification is-danger is-light">
          <i class="fas fa-exclamation-triangle"></i>
          {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="notification is-success is-light">
          <i class="fas fa-check-circle"></i>
          {{ successMessage }}
        </div>

        <div class="field">
          <div class="control">
            <button 
              type="button" 
              class="button is-light is-fullwidth mb-2"
              @click="previousStep"
            >
              <span class="icon">
                <i class="fas fa-arrow-left"></i>
              </span>
              <span>Voltar</span>
            </button>
            <button 
              type="submit" 
              class="button is-primary is-fullwidth"
              :class="{ 'is-loading': loading }"
              :disabled="loading"
            >
              <span class="icon">
                <i class="fas fa-user-plus"></i>
              </span>
              <span>{{ loading ? 'Cadastrando...' : 'Finalizar Cadastro' }}</span>
            </button>
          </div>
        </div>
      </form>

      <div class="field has-text-centered">
        <p class="help">
          Já tem uma conta? 
          <a href="#" @click.prevent="$emit('show-login')" class="has-text-primary">
            Faça login aqui
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2E7D32 0%, #A5D6A7 100%);
  padding: 1rem;
}

.register-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 500px;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  font-size: 3rem;
  color: #2E7D32;
  margin-bottom: 1rem;
}

.title {
  color: #2E7D32;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.steps {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e9ecef;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: all 0.3s;
}

.step.is-active .step-number {
  background: #2E7D32;
  color: white;
}

.step.is-completed .step-number {
  background: #A5D6A7;
  color: #2E7D32;
}

.step-label {
  font-size: 0.875rem;
  color: #666;
  font-weight: 600;
}

.step.is-active .step-label {
  color: #2E7D32;
}

.step-line {
  width: 60px;
  height: 2px;
  background: #e9ecef;
  margin: 0 1rem;
}

.register-form {
  margin-bottom: 1.5rem;
}

.field {
  margin-bottom: 1.5rem;
}

.label {
  color: #333;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.input, .select select, .textarea {
  border-radius: 8px;
  border: 2px solid #e9ecef;
  transition: border-color 0.2s;
}

.input:focus, .select select:focus, .textarea:focus {
  border-color: #2E7D32;
  box-shadow: 0 0 0 0.125em rgba(46, 125, 50, 0.25);
}

.password-toggle {
  cursor: pointer;
  color: #666;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #2E7D32;
}

.notification {
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.button {
  border-radius: 8px;
  font-weight: 600;
  height: 3rem;
  transition: all 0.2s;
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

@media (max-width: 480px) {
  .register-card {
    padding: 1.5rem;
  }
  
  .logo {
    font-size: 2.5rem;
  }
  
  .title {
    font-size: 1.5rem;
  }
  
  .steps {
    flex-direction: column;
    gap: 1rem;
  }
  
  .step-line {
    width: 2px;
    height: 30px;
    margin: 0;
  }
}
</style> 
<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService.js'
import { useBrand } from '../composables/useBrand.js'

const router = useRouter()
const { brandConfig } = useBrand()

const loginData = reactive({
  email: '',
  senha: ''
})

const loading = ref(false)
const errorMessage = ref('')
const showPassword = ref(false)

const handleLogin = async () => {
  if (!loginData.email || !loginData.senha) {
    errorMessage.value = 'Por favor, preencha todos os campos'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    const response = await authService.login(loginData.email, loginData.senha)
    
    // Salvar dados do usuário
    authService.setCurrentUser(response.usuario)
    
    // Redirecionar baseado no tipo de usuário
    if (response.usuario.tipo === 'admin') {
      router.push('/admin')
    } else {
      router.push('/cliente')
    }
  } catch (error) {
    console.error('Erro no login:', error)
    if (error.response?.data) {
      // Tratar erros específicos da API
      if (error.response.data.email) {
        errorMessage.value = error.response.data.email[0]
      } else if (error.response.data.senha) {
        errorMessage.value = error.response.data.senha[0]
      } else if (error.response.data.non_field_errors) {
        errorMessage.value = error.response.data.non_field_errors[0]
      } else {
        errorMessage.value = 'Erro ao fazer login. Verifique suas credenciais.'
      }
    } else {
      errorMessage.value = 'Erro ao conectar com o servidor. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <div class="logo">
          <i class="fas fa-paw"></i>
        </div>
        <h1 class="auth-title">Bem-vindo ao {{ brandConfig?.nome_estabelecimento || 'AgendaVet' }}</h1>
        <p class="auth-subtitle">Faça login para acessar sua conta</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="field">
          <label class="label">E-mail</label>
          <div class="control has-icons-left">
            <input 
              v-model="loginData.email"
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
          <label class="label">Senha</label>
          <div class="control has-icons-left has-icons-right">
            <input 
              v-model="loginData.senha"
              :type="showPassword ? 'text' : 'password'"
              class="input" 
              placeholder="Sua senha"
              required
            >
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
            <span class="icon is-small is-right password-toggle" @click="togglePasswordVisibility">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
          </div>
        </div>

        <div v-if="errorMessage" class="notification is-danger is-light">
          <i class="fas fa-exclamation-triangle"></i>
          {{ errorMessage }}
        </div>

        <div class="field">
          <div class="control">
            <button 
              type="submit" 
              class="button is-primary is-fullwidth"
              :class="{ 'is-loading': loading }"
              :disabled="loading"
            >
              <span class="icon">
                <i class="fas fa-sign-in-alt"></i>
              </span>
              <span>{{ loading ? 'Entrando...' : 'Entrar' }}</span>
            </button>
          </div>
        </div>

        <div class="field has-text-centered">
          <p class="help">
            Não tem uma conta? 
            <a href="#" @click.prevent="$emit('show-register')" class="has-text-primary">
              Cadastre-se aqui
            </a>
          </p>
        </div>

        <div class="field has-text-centered">
          <p class="help">
            <a href="#" class="has-text-grey">
              Esqueceu sua senha?
            </a>
          </p>
        </div>
      </form>

      <div class="demo-accounts">
        <details class="demo-info">
          <summary>Contas de demonstração</summary>
          <div class="demo-accounts-list">
            <div class="demo-account">
              <strong>Admin:</strong> admin@agendavet.com / admin123
            </div>
            <div class="demo-account">
              <strong>Cliente:</strong> cliente@email.com / cliente123
            </div>
          </div>
        </details>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--accent-color) 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  font-size: 3rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.auth-title {
  color: var(--primary-color);
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.auth-subtitle {
  color: var(--text-color);
  opacity: 0.7;
}

.login-form {
  margin-bottom: 1.5rem;
}

.field {
  margin-bottom: 1.5rem;
}

.label {
  color: var(--text-color);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.input {
  border-radius: 8px;
  border: 2px solid var(--border-color);
  transition: border-color 0.2s;
}

.input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.125em rgba(46, 125, 50, 0.25);
}

.password-toggle {
  cursor: pointer;
  color: var(--text-color);
  transition: color 0.2s;
}

.password-toggle:hover {
  color: var(--primary-color);
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

.demo-accounts {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.demo-info {
  font-size: 0.875rem;
  color: var(--text-color);
}

.demo-info summary {
  cursor: pointer;
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.demo-accounts-list {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 1rem;
  margin-top: 0.5rem;
}

.demo-account {
  margin-bottom: 0.5rem;
  font-family: monospace;
  font-size: 0.8rem;
}

.demo-account:last-child {
  margin-bottom: 0;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 1.5rem;
  }
  
  .logo {
    font-size: 2.5rem;
  }
  
  .auth-title {
    font-size: 1.5rem;
  }
}
</style> 
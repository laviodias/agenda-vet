<script setup>
import { ref } from 'vue'
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'
import { useBrand } from '../composables/useBrand.js'

const showLogin = ref(true)
const { brandConfig } = useBrand()

const toggleForm = () => {
  showLogin.value = !showLogin.value
}
</script>

<template>
  <div class="auth-container">
    <LoginForm 
      v-if="showLogin" 
      @show-register="toggleForm" 
    />
    <RegisterForm 
      v-else 
      @show-login="toggleForm" 
    />
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
</style> 
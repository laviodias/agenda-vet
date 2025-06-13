<script setup>
import { ref } from 'vue'
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'

const showLogin = ref(true)

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
  min-height: 100vh;
  background: linear-gradient(135deg, #2E7D32 0%, #A5D6A7 100%);
}
</style> 
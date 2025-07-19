<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useBrand } from '../../composables/useBrand.js'
import authService from '../../services/authService.js'

const { brandConfig } = useBrand()
const router = useRouter()

const logout = () => {
  authService.logout()
  router.push('/auth')
}
</script>

<template>
  <div class="admin-layout">
    <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <RouterLink class="navbar-item" to="/admin">
          <span class="icon-text">
            <span class="icon">
              <i class="fas fa-paw"></i>
            </span>
            <span>{{ brandConfig?.nome_estabelecimento || 'AgendaVet' }} Admin</span>
          </span>
        </RouterLink>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <RouterLink class="navbar-item" to="/admin/clientes">
            <span class="icon-text">
              <span class="icon">
                <i class="fas fa-user-friends"></i>
              </span>
              <span>Clientes</span>
            </span>
          </RouterLink>

          <RouterLink class="navbar-item" to="/admin/animais">
            <span class="icon-text">
              <span class="icon">
                <i class="fas fa-paw"></i>
              </span>
              <span>Animais</span>
            </span>
          </RouterLink>

          <RouterLink class="navbar-item" to="/admin/servicos">
            <span class="icon-text">
              <span class="icon">
                <i class="fas fa-clipboard-list"></i>
              </span>
              <span>Serviços</span>
            </span>
          </RouterLink>

          <RouterLink class="navbar-item" to="/admin/agendamentos">
            <span class="icon-text">
              <span class="icon">
                <i class="fas fa-list"></i>
              </span>
              <span>Agendamentos</span>
            </span>
          </RouterLink>

          <RouterLink class="navbar-item" to="/admin/marca">
            <span class="icon-text">
              <span class="icon">
                <i class="fas fa-palette"></i>
              </span>
              <span>Marca</span>
            </span>
          </RouterLink>

          <!-- <RouterLink class="navbar-item" to="/admin/roles">
            <span class="icon-text">
              <span class="icon">
                <i class="fas fa-user-shield"></i>
              </span>
              <span>Cargos</span>
            </span>
          </RouterLink> -->
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <button class="button is-light" @click="logout">
              <span class="icon">
                <i class="fas fa-sign-out-alt"></i>
              </span>
              <span>Sair</span>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.admin-layout {
  min-height: 100vh;
  background: var(--background);
}

.navbar {
  padding: 0.5rem 1rem;
}

.navbar-item {
  padding: 0.5rem 1rem;
}

.icon-text {
  align-items: center;
}

.icon {
  margin-right: 0.5rem;
}
</style> 
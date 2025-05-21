<script setup>
import { RouterLink, RouterView } from 'vue-router'
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
            <span>AgendaVet Admin</span>
          </span>
        </RouterLink>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <RouterLink class="navbar-item" to="/admin/funcionarios">
            <span class="icon-text">
              <span class="icon">
                <i class="fas fa-users"></i>
              </span>
              <span>Funcionários</span>
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

          <RouterLink class="navbar-item" to="/admin/agenda">
            <span class="icon-text">
              <span class="icon">
                <i class="fas fa-calendar-alt"></i>
              </span>
              <span>Agenda</span>
            </span>
          </RouterLink>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <RouterLink class="button is-light" to="/">
              <span class="icon">
                <i class="fas fa-sign-out-alt"></i>
              </span>
              <span>Sair</span>
            </RouterLink>
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
<template>
  <div class="roles-management">
    <div class="container">
      <h1 class="title">Gerenciamento de Cargos e Permissões</h1>
      
      <!-- Estatísticas -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">{{ stats.rolesCount }}</div>
          <div class="stat-label">Cargos Ativos</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.permissionsCount }}</div>
          <div class="stat-label">Permissões</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.usersCount }}</div>
          <div class="stat-label">Usuários</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.assignmentsCount }}</div>
          <div class="stat-label">Atribuições</div>
        </div>
      </div>

      <!-- Botões de Ação -->
      <div class="action-buttons">
        <button @click="showCreateRoleModal = true" class="btn btn-success">
          <i class="fas fa-plus"></i> Criar Novo Cargo
        </button>
        <button @click="openAssignPermissionsModal" class="btn btn-primary">
          <i class="fas fa-key"></i> Atribuir Permissões
        </button>
        <button @click="openAssignUsersModal" class="btn btn-info">
          <i class="fas fa-users"></i> Atribuir Cargos a Usuários
        </button>
      </div>

      <!-- Lista de Roles -->
      <div class="roles-section">
        <div class="roles-header">
          <h2>Cargos Existentes ({{ roles.length }})</h2>
          <div class="filter-controls">
            <label>
              <input type="checkbox" v-model="showInactiveRoles" :disabled="loadingInactiveRoles">
              Mostrar cargos inativos
            </label>
          </div>
        </div>
        
        <!-- Loading state -->
        <div v-if="loading" class="loading">
          Carregando cargos...
        </div>
        
        <!-- Empty state -->
        <div v-else-if="filteredRoles.length === 0" class="empty-state">
          <p>{{ showInactiveRoles ? 'Nenhum cargo encontrado.' : 'Nenhum cargo ativo encontrado.' }}</p>
        </div>
        
        <!-- Roles grid -->
        <div v-else class="roles-grid">
          <div v-for="role in filteredRoles" :key="role.id" class="role-card" :class="{ 'inactive': !role.is_active }">
            <div class="role-header">
              <h3>{{ role.display_name }}</h3>
              <span :class="['status-badge', role.is_active ? 'active' : 'inactive']">
                {{ role.is_active ? 'Ativo' : 'Inativo' }}
              </span>
            </div>
            <p class="role-description">{{ role.description || 'Sem descrição' }}</p>
            <div class="role-permissions">
              <h4>Permissões ({{ role.permissions_count || role.permissions.length }}):</h4>
              <div class="permissions-list">
                <span v-for="rolePermission in role.permissions" :key="rolePermission.id" class="permission-tag">
                  {{ rolePermission.permission ? rolePermission.permission.description : rolePermission.description }}
                </span>
                <span v-if="!role.permissions || role.permissions.length === 0" class="no-permissions">
                  Nenhuma permissão atribuída
                </span>
              </div>
            </div>
            <div class="role-actions">
              <button @click="editRole(role)" class="btn btn-sm btn-outline-primary">
                Editar
              </button>
              <button @click="toggleRoleStatus(role)" :class="['btn', 'btn-sm', role.is_active ? 'btn-outline-warning' : 'btn-outline-success']">
                {{ role.is_active ? 'Desativar' : 'Ativar' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Criar Role -->
    <div v-if="showCreateRoleModal" class="modal-overlay" @click="showCreateRoleModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Criar Novo Cargo</h3>
          <button @click="showCreateRoleModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="createRole" class="modal-body">
          <div class="form-group">
            <label>Nome do Cargo:</label>
            <input v-model="newRole.name" type="text" required placeholder="Ex: veterinario">
          </div>
          <div class="form-group">
            <label>Nome de Exibição:</label>
            <input v-model="newRole.display_name" type="text" required placeholder="Ex: Veterinário">
          </div>
          <div class="form-group">
            <label>Descrição:</label>
            <textarea v-model="newRole.description" placeholder="Descrição das responsabilidades"></textarea>
          </div>
          <div class="form-group">
            <label>Permissões:</label>
            <div class="permissions-grid">
              <div v-for="resource in permissionsByResource" :key="resource.name" class="resource-group">
                <h4>{{ resource.display_name }}</h4>
                <div class="permissions-list">
                  <label v-for="permission in resource.permissions" :key="permission.id" class="permission-checkbox">
                    <input 
                      type="checkbox" 
                      :value="permission.id" 
                      v-model="newRole.permissions"
                    >
                    {{ permission.description }}
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showCreateRoleModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-success">
              Criar Cargo
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Atribuir Permissões -->
    <div v-if="showAssignPermissionsModal" class="modal-overlay" @click="showAssignPermissionsModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Atribuir Permissões</h3>
          <button @click="showAssignPermissionsModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="assignPermissions" class="modal-body">
          <div class="form-group">
            <label>Selecionar Cargo:</label>
            <select v-model="selectedRole" required>
              <option value="">Escolha um cargo</option>
              <option v-for="role in activeRoles" :key="role.id" :value="role.id">
                {{ role.display_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Permissões:</label>
            <div v-if="selectedRole" class="permissions-summary">
              <span class="selected-count">{{ selectedPermissions.length }} permissões selecionadas</span>
            </div>
            <div class="permissions-grid">
              <div v-for="resource in permissionsByResource" :key="resource.name" class="resource-group">
                <h4>{{ resource.display_name }}</h4>
                <div class="permissions-list">
                  <label v-for="permission in resource.permissions" :key="permission.id" class="permission-checkbox">
                    <input 
                      type="checkbox" 
                      :value="permission.id" 
                      v-model="selectedPermissions"
                    >
                    {{ permission.description }}
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showAssignPermissionsModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Atualizar Permissões
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Atribuir Usuários -->
    <div v-if="showAssignUsersModal" class="modal-overlay" @click="showAssignUsersModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Atribuir Cargos a Usuários</h3>
          <button @click="showAssignUsersModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="assignUsers" class="modal-body">
          <div class="form-group">
            <label>Selecionar Usuário:</label>
            <select v-model="selectedUser" required>
              <option value="">Escolha um usuário</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.nome }} ({{ user.email }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Cargos:</label>
            <div v-if="selectedUser" class="roles-summary">
              <span v-if="loadingUserRoles" class="loading-indicator">Carregando cargos...</span>
              <span v-else class="selected-count">{{ selectedUserRoles.length }} cargos selecionados</span>
            </div>
            <div class="roles-list">
              <label v-for="role in activeRoles" :key="role.id" class="role-checkbox">
                <input 
                  type="checkbox" 
                  :value="role.id" 
                  v-model="selectedUserRoles"
                >
                {{ role.display_name }}
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showAssignUsersModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-info">
              Atribuir Cargos
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar Cargo -->
    <div v-if="showEditRoleModal" class="modal-overlay" @click="showEditRoleModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Editar Cargo</h3>
          <button @click="showEditRoleModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="updateRole" class="modal-body">
          <div class="form-group">
            <label>Nome do Cargo:</label>
            <input v-model="editingRole.name" type="text" required placeholder="Ex: veterinario">
          </div>
          <div class="form-group">
            <label>Nome de Exibição:</label>
            <input v-model="editingRole.display_name" type="text" required placeholder="Ex: Veterinário">
          </div>
          <div class="form-group">
            <label>Descrição:</label>
            <textarea v-model="editingRole.description" placeholder="Descrição das responsabilidades"></textarea>
          </div>
          <div class="form-group">
            <label>Status:</label>
            <select v-model="editingRole.is_active">
              <option :value="true">Ativo</option>
              <option :value="false">Inativo</option>
            </select>
          </div>
          <div class="form-group">
            <label>Permissões:</label>
            <div class="permissions-grid">
              <div v-for="resource in permissionsByResource" :key="resource.name" class="resource-group">
                <h4>{{ resource.display_name }}</h4>
                <div class="permissions-list">
                  <label v-for="permission in resource.permissions" :key="permission.id" class="permission-checkbox">
                    <input 
                      type="checkbox" 
                      :value="permission.id" 
                      v-model="editingRole.permissions"
                    >
                    {{ permission.description }}
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showEditRoleModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Atualizar Cargo
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import adminService from '../../services/adminService'

export default {
  name: 'RolesManagement',
  data() {
    return {
      roles: [],
      permissions: [],
      users: [],
      stats: {
        rolesCount: 0,
        permissionsCount: 0,
        usersCount: 0,
        assignmentsCount: 0
      },
      showCreateRoleModal: false,
      showAssignPermissionsModal: false,
      showAssignUsersModal: false,
      showEditRoleModal: false,
      newRole: {
        name: '',
        display_name: '',
        description: '',
        permissions: []
      },
      editingRole: {
        id: null,
        name: '',
        display_name: '',
        description: '',
        is_active: true,
        permissions: []
      },
      selectedRole: '',
      selectedPermissions: [],
      selectedUser: '',
      selectedUserRoles: [],
      loading: false,
      showInactiveRoles: false, // Novo estado para controlar a visibilidade dos roles inativos
      loadingInactiveRoles: false, // Estado para loading dos roles inativos
      allRolesLoaded: false, // Estado para controlar se já carregamos todos os roles
      loadingUserRoles: false // Estado para loading dos roles do usuário
    }
  },
  computed: {
    activeRoles() {
      return this.roles.filter(role => role.is_active)
    },
    filteredRoles() {
      if (this.showInactiveRoles) {
        // Se marcou para mostrar inativos, mostrar todos os roles
        return this.roles
      } else {
        // Se não marcou, mostrar apenas os ativos
        return this.roles.filter(role => role.is_active)
      }
    },
    permissionsByResource() {
      const grouped = {}
      this.permissions.forEach(permission => {
        if (!grouped[permission.resource]) {
          grouped[permission.resource] = {
            name: permission.resource,
            display_name: this.getResourceDisplayName(permission.resource),
            permissions: []
          }
        }
        grouped[permission.resource].permissions.push(permission)
      })
      return Object.values(grouped)
    }
  },
  async mounted() {
    console.log('Componente Roles montado')
    await this.loadData()
    this.debugRoles() // Debug temporário
  },
  watch: {
    roles: {
      handler(newRoles) {
        console.log('Roles atualizados:', newRoles.length)
      },
      deep: true
    },
    showInactiveRoles: {
      async handler(newValue) {
        if (newValue && !this.allRolesLoaded) {
          // Se marcou para mostrar inativos e ainda não carregamos todos os roles
          this.loadingInactiveRoles = true
          try {
            await this.loadAllRoles()
            this.allRolesLoaded = true
          } finally {
            this.loadingInactiveRoles = false
          }
        }
        // Se já temos todos os roles carregados, não precisa fazer nova requisição
      }
    },
    selectedRole: {
      handler(newValue) {
        // Quando o role for selecionado no modal de permissões
        if (this.showAssignPermissionsModal) {
          this.onRoleSelectedForPermissions()
        }
      }
    },
    selectedUser: {
      handler(newValue) {
        // Quando o usuário for selecionado no modal de atribuição de roles
        if (this.showAssignUsersModal) {
          this.onUserSelectedForRoles()
        }
      }
    }
  },
  methods: {
    debugRoles() {
      console.log('Debug - Roles:', this.roles)
      this.roles.forEach(role => {
        console.log(`Role: ${role.display_name}`, role)
        console.log(`Permissões:`, role.permissions)
      })
    },
    async loadData() {
      try {
        this.loading = true
        
        // Carregar dados em paralelo
        const [rolesResponse, permissionsResponse, usersResponse, statsResponse] = await Promise.all([
          this.loadRoles(),
          this.loadPermissions(),
          this.loadUsers(),
          this.loadStats()
        ])
        
        
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.loading = false
      }
    },
    async loadRoles() {
      try {
        const response = await adminService.getRoles()
        
        // Verificar se a resposta é um array direto ou está dentro de .data
        if (Array.isArray(response)) {
          this.roles = response
        } else if (Array.isArray(response.data)) {
          this.roles = response.data
        } else {
          this.roles = []
        }
        
        console.log('Roles carregados:', this.roles)
        console.log('Número de roles:', this.roles.length)
        
        // Debug detalhado de cada role
        this.roles.forEach((role, index) => {
          console.log(`Role ${index + 1}:`, {
            id: role.id,
            name: role.name,
            display_name: role.display_name,
            permissions: role.permissions,
            permissions_count: role.permissions_count
          })
        })
        
        // Resetar cache quando carregar apenas roles ativos
        this.allRolesLoaded = false
      } catch (error) {
        console.error('Erro ao carregar roles:', error)
        console.error('Erro completo:', error.response || error)
      }
    },
    async loadAllRoles() {
      try {
        console.log('Carregando todos os roles (incluindo inativos)...')
        const response = await adminService.getRoles(true) // includeInactive = true
        
        // Verificar se a resposta é um array direto ou está dentro de .data
        if (Array.isArray(response)) {
          this.roles = response
        } else if (Array.isArray(response.data)) {
          this.roles = response.data
        } else {
          this.roles = []
        }
        
        console.log('Todos os roles carregados:', this.roles.length)
        this.allRolesLoaded = true // Marcar que carregamos todos os roles
      } catch (error) {
        console.error('Erro ao carregar todos os roles:', error)
      }
    },
    async loadPermissions() {
      try {
        const response = await adminService.getPermissions()
        
        // Verificar se a resposta é um array direto ou está dentro de .data
        if (Array.isArray(response)) {
          this.permissions = response
        } else if (Array.isArray(response.data)) {
          this.permissions = response.data
        } else {
          this.permissions = []
        }
        
      } catch (error) {
        console.error('Erro ao carregar permissões:', error)
      }
    },
    async loadUsers() {
      try {
        console.log('Carregando usuários...')
        const response = await adminService.getUsers()
        
        // Verificar se a resposta é um array direto ou está dentro de .data
        if (Array.isArray(response)) {
          this.users = response
        } else if (Array.isArray(response.data)) {
          this.users = response.data
        } else {
          this.users = []
        }
        
        console.log('Usuários carregados:', this.users.length)
      } catch (error) {
        console.error('Erro ao carregar usuários:', error)
      }
    },
    async loadStats() {
      try {
        const response = await adminService.getRoleStats()
        this.stats = response || {
          rolesCount: this.roles.length,
          permissionsCount: this.permissions.length,
          usersCount: this.users.length,
          assignmentsCount: 0
        }
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
      }
    },
    async createRole() {
      try {
        await adminService.createRole(this.newRole)
        this.showCreateRoleModal = false
        this.resetNewRole()
        await this.loadRoles()
        this.$toast.success('Cargo criado com sucesso!')
      } catch (error) {
        console.error('Erro ao criar role:', error)
        this.$toast.error('Erro ao criar role')
      }
    },
    async assignPermissions() {
      try {
        await adminService.assignPermissions(this.selectedRole, this.selectedPermissions)
        this.showAssignPermissionsModal = false
        this.resetSelectedData()
        await this.loadRoles()
        this.$toast.success('Permissões atualizadas com sucesso!')
      } catch (error) {
        console.error('Erro ao atribuir permissões:', error)
        this.$toast.error('Erro ao atribuir permissões')
      }
    },
    openAssignPermissionsModal() {
      this.showAssignPermissionsModal = true
      this.selectedRole = ''
      this.selectedPermissions = []
    },
    async onRoleSelectedForPermissions() {
      if (this.selectedRole) {
        // Encontrar o role selecionado
        const role = this.roles.find(r => r.id == this.selectedRole)
        console.log('Role encontrado:', role)
        
        if (role && role.permissions) {
          // Extrair os IDs das permissões que o role já tem
          this.selectedPermissions = role.permissions.map(rp => {
            console.log('Processando permissão:', rp)
            // Verificar se é um objeto RolePermission ou Permission
            if (rp.permission) {
              return rp.permission.id
            } else if (rp.id) {
              return rp.id
            }
            return null
          }).filter(id => id !== null)
          
          console.log('Role selecionado:', role.display_name)
          console.log('Permissões do role carregadas:', this.selectedPermissions)
          console.log('Estrutura das permissões:', role.permissions)
        } else {
          this.selectedPermissions = []
          console.log('Role não encontrado ou sem permissões')
        }
      } else {
        this.selectedPermissions = []
      }
    },
    async assignUsers() {
      try {
        await adminService.assignUserRoles(this.selectedUser, this.selectedUserRoles)
        this.showAssignUsersModal = false
        this.resetSelectedData()
        this.$toast.success('Cargos atribuídos com sucesso!')
      } catch (error) {
        console.error('Erro ao atribuir roles:', error)
        this.$toast.error('Erro ao atribuir roles')
      }
    },
    openAssignUsersModal() {
      this.showAssignUsersModal = true
      this.selectedUser = ''
      this.selectedUserRoles = []
    },
    async onUserSelectedForRoles() {
      if (this.selectedUser) {
        try {
          this.loadingUserRoles = true
          console.log('Carregando roles do usuário:', this.selectedUser)
          // Buscar os roles que o usuário já tem
          const response = await adminService.getUserRoles(this.selectedUser)
          
          console.log('Resposta da API:', response)
          
          // Extrair os IDs dos roles que o usuário já tem
          let userRoles = []
          if (Array.isArray(response)) {
            userRoles = response
          } else if (Array.isArray(response.data)) {
            userRoles = response.data
          }
          
          // Extrair os IDs dos roles
          this.selectedUserRoles = userRoles.map(userRole => {
            console.log('Processando userRole:', userRole)
            return userRole.role ? userRole.role.id : userRole.id
          }).filter(id => id !== null)
          
          console.log('Roles do usuário carregados:', this.selectedUserRoles)
        } catch (error) {
          console.error('Erro ao carregar roles do usuário:', error)
          this.selectedUserRoles = []
        } finally {
          this.loadingUserRoles = false
        }
      } else {
        this.selectedUserRoles = []
      }
    },
    async editRole(role) {
      // Preparar o role para edição
      this.editingRole = {
        id: role.id,
        name: role.name,
        display_name: role.display_name,
        description: role.description || '',
        is_active: role.is_active,
        permissions: role.permissions ? role.permissions.map(rp => rp.permission ? rp.permission.id : rp.id) : []
      }
      this.showEditRoleModal = true
    },
    async updateRole() {
      try {
        await adminService.updateRole(this.editingRole.id, this.editingRole)
        this.showEditRoleModal = false
        this.resetEditingRole()
        await this.loadRoles()
        this.$toast.success('Cargo atualizado com sucesso!')
      } catch (error) {
        console.error('Erro ao atualizar role:', error)
        this.$toast.error('Erro ao atualizar role')
      }
    },
    async toggleRoleStatus(role) {
      try {
        await adminService.toggleRoleStatus(role.id)
        // Atualizar apenas o status do role na lista local
        const index = this.roles.findIndex(r => r.id === role.id)
        if (index !== -1) {
          this.roles[index].is_active = !this.roles[index].is_active
        }
        this.$toast.success(`Cargo ${role.is_active ? 'desativado' : 'ativado'} com sucesso!`)
      } catch (error) {
        console.error('Erro ao alterar status do role:', error)
        this.$toast.error('Erro ao alterar status do role')
      }
    },
    resetNewRole() {
      this.newRole = {
        name: '',
        display_name: '',
        description: '',
        permissions: []
      }
    },
    resetEditingRole() {
      this.editingRole = {
        id: null,
        name: '',
        display_name: '',
        description: '',
        is_active: true,
        permissions: []
      }
    },
    resetSelectedData() {
      this.selectedRole = ''
      this.selectedPermissions = []
      this.selectedUser = ''
      this.selectedUserRoles = []
    },
    getResourceDisplayName(resource) {
      const resourceNames = {
        'usuarios': 'Usuários',
        'agendamentos': 'Agendamentos',
        'animais': 'Animais',
        'servicos': 'Serviços',
        'configuracoes': 'Configurações',
        'relatorios': 'Relatórios',
        'brand': 'Marca/Branding'
      }
      return resourceNames[resource] || resource
    }
  }
}
</script>

<style scoped>
.roles-management {
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  color: #333;
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  color: #007bff;
}

.stat-label {
  color: #6c757d;
  margin-top: 5px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-outline-primary {
  background: transparent;
  color: #007bff;
  border: 1px solid #007bff;
}

.btn-outline-warning {
  background: transparent;
  color: #ffc107;
  border: 1px solid #ffc107;
}

.btn-outline-success {
  background: transparent;
  color: #28a745;
  border: 1px solid #28a745;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

.roles-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.roles-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.roles-header h2 {
  margin: 0;
  color: #333;
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-controls label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  color: #555;
}

.filter-controls input[type="checkbox"] {
  width: auto;
  transform: scale(1.2);
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.role-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  background: white;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.role-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.role-card.inactive {
  opacity: 0.7;
  background-color: #f8f9fa;
  border-color: #e0e0e0;
}

.role-card.inactive .role-header h3 {
  color: #999;
}

.role-card.inactive .role-description {
  color: #999;
}

.role-card.inactive .permission-tag {
  background-color: #e9ecef;
  color: #6c757d;
}

.role-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.role-header h3 {
  margin: 0;
  color: #333;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
}

.role-description {
  color: #666;
  margin-bottom: 15px;
}

.role-permissions h4 {
  margin-bottom: 10px;
  font-size: 14px;
  color: #333;
}

.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.permission-tag {
  background: #e9ecef;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #495057;
}

.no-permissions {
  color: #6c757d;
  font-style: italic;
}

.role-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group textarea {
  height: 80px;
  resize: vertical;
}

.permissions-grid {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
}

.resource-group {
  margin-bottom: 20px;
}

.resource-group h4 {
  margin-bottom: 10px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}

.permission-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
  font-size: 14px;
}

.permission-checkbox input[type="checkbox"] {
  width: auto;
}

.roles-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
}

.role-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 14px;
}

.role-checkbox input[type="checkbox"] {
  width: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #dee2e6;
}

/* New styles for loading and empty states */
.loading, .empty-state {
  text-align: center;
  padding: 20px;
  color: #666;
  font-style: italic;
}

.loading-indicator {
  margin-left: 10px;
  font-size: 14px;
  color: #007bff;
}

.cache-indicator {
  margin-left: 10px;
  font-size: 14px;
  color: #28a745;
  font-style: italic;
}

.permissions-summary {
  margin-bottom: 10px;
  padding: 8px 12px;
  background: #e9ecef;
  border-radius: 4px;
  border-left: 4px solid #007bff;
}

.selected-count {
  font-size: 14px;
  color: #495057;
  font-weight: 500;
}

.roles-summary {
  margin-bottom: 10px;
  padding: 8px 12px;
  background: #e9ecef;
  border-radius: 4px;
  border-left: 4px solid #17a2b8;
}
</style> 
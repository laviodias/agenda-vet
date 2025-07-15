import { ref, computed } from 'vue'
import authService from '@/services/authService.js'
import apiService from '@/services/api.js'

export function useRoles() {
  return {
    loading: { value: false },
    error: { value: null },
    userRoles: [],
    userPermissions: [],
    roles: [],
    permissions: [],
    hasRole: () => false,
    hasAnyRole: () => false,
    isAdmin: { value: false },
    isVeterinario: { value: false },
    isRecepcionista: { value: false },
    isCliente: { value: false },
    hasPermission: () => false,
    canAccessAdmin: { value: false },
    canManageUsers: { value: false },
    canManageAppointments: { value: false },
    canManageServices: { value: false },
    canManageSettings: { value: false },
    refreshPermissions: async () => {},
    fetchRoles: async () => {},
    fetchPermissions: async () => {},
    assignRole: async () => {},
    removeRole: async () => {},
    fetchUserPermissions: async () => {},
    formatPermission: () => ({}),
    debugPermissions: () => {}
  }
} 
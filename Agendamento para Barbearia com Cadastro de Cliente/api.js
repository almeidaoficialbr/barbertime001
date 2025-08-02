// Configuração da API
const API_BASE_URL = 'http://localhost:5000/api';

// Classe para gerenciar requisições à API
class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
  }

  // Configurar token de autenticação
  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }

  // Obter token atual
  getToken() {
    return this.token || localStorage.getItem('access_token');
  }

  // Fazer requisição HTTP
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const token = this.getToken();

    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Adicionar token de autenticação se disponível
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Métodos HTTP
  async get(endpoint, options = {}) {
    return this.request(endpoint, { method: 'GET', ...options });
  }

  async post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
      ...options,
    });
  }

  async put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
      ...options,
    });
  }

  async delete(endpoint, options = {}) {
    return this.request(endpoint, { method: 'DELETE', ...options });
  }
}

// Instância global da API
const api = new ApiClient();

// Serviços específicos
export const authService = {
  // Login
  async login(email, password) {
    const response = await api.post('/auth/login', { email, password });
    if (response.access_token) {
      api.setToken(response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.user));
    }
    return response;
  },

  // Logout
  async logout() {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      api.setToken(null);
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  },

  // Registrar tenant
  async registerTenant(data) {
    return api.post('/auth/register-tenant', data);
  },

  // Obter usuário atual
  async getCurrentUser() {
    return api.get('/auth/me');
  },

  // Renovar token
  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await api.post('/auth/refresh', {}, {
      headers: {
        Authorization: `Bearer ${refreshToken}`,
      },
    });

    if (response.access_token) {
      api.setToken(response.access_token);
    }

    return response;
  },
};

export const publicService = {
  // Listar barbearias
  async getBarbershops(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return api.get(`/public/barbershops${queryString ? `?${queryString}` : ''}`);
  },

  // Obter detalhes da barbearia
  async getBarbershopDetails(slug) {
    return api.get(`/public/barbershops/${slug}`);
  },

  // Obter serviços da barbearia
  async getBarbershopServices(slug) {
    return api.get(`/public/barbershops/${slug}/services`);
  },

  // Obter funcionários da barbearia
  async getBarbershopStaff(slug) {
    return api.get(`/public/barbershops/${slug}/staff`);
  },

  // Obter horários disponíveis
  async getAvailableSlots(slug, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return api.get(`/public/barbershops/${slug}/available-slots${queryString ? `?${queryString}` : ''}`);
  },

  // Obter cidades
  async getCities() {
    return api.get('/public/cities');
  },
};

export const tenantService = {
  // Obter configurações do tenant
  async getConfig() {
    return api.get('/tenant/config');
  },

  // Atualizar configurações do tenant
  async updateConfig(data) {
    return api.put('/tenant/config', data);
  },

  // Upload de logo
  async uploadLogo(file) {
    const formData = new FormData();
    formData.append('logo', file);

    return api.request('/tenant/logo', {
      method: 'POST',
      body: formData,
      headers: {}, // Remover Content-Type para FormData
    });
  },

  // Obter funcionários
  async getStaff() {
    return api.get('/tenant/staff');
  },

  // Criar funcionário
  async createStaff(data) {
    return api.post('/tenant/staff', data);
  },

  // Atualizar funcionário
  async updateStaff(id, data) {
    return api.put(`/tenant/staff/${id}`, data);
  },

  // Remover funcionário
  async deleteStaff(id) {
    return api.delete(`/tenant/staff/${id}`);
  },

  // Obter dashboard
  async getDashboard() {
    return api.get('/tenant/dashboard');
  },
};

// Utilitários
export const utils = {
  // Verificar se usuário está autenticado
  isAuthenticated() {
    return !!api.getToken();
  },

  // Obter usuário do localStorage
  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Verificar role do usuário
  hasRole(role) {
    const user = this.getCurrentUser();
    return user && user.role === role;
  },

  // Verificar se é super admin
  isSuperAdmin() {
    return this.hasRole('super_admin');
  },

  // Verificar se é admin do tenant
  isTenantAdmin() {
    return this.hasRole('tenant_admin');
  },

  // Verificar se é funcionário
  isTenantUser() {
    return this.hasRole('tenant_user');
  },
};

export default api;


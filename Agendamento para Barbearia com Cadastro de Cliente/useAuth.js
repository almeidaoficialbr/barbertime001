import React, { useState, useEffect, createContext, useContext } from 'react';
import { authService, utils } from '../lib/api';

// Contexto de autenticação
const AuthContext = createContext();

// Provider de autenticação
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Verificar autenticação ao carregar
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      if (utils.isAuthenticated()) {
        const userData = utils.getCurrentUser();
        if (userData) {
          setUser(userData);
          setIsAuthenticated(true);
        } else {
          // Tentar obter dados atualizados do servidor
          const response = await authService.getCurrentUser();
          setUser(response.user);
          setIsAuthenticated(true);
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      // Token pode estar expirado, limpar dados
      await logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      setLoading(true);
      const response = await authService.login(email, password);
      setUser(response.user);
      setIsAuthenticated(true);
      return response;
    } catch (error) {
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const registerTenant = async (data) => {
    try {
      setLoading(true);
      const response = await authService.registerTenant(data);
      return response;
    } catch (error) {
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    registerTenant,
    checkAuth,
    // Funções de verificação de role
    isSuperAdmin: () => utils.isSuperAdmin(),
    isTenantAdmin: () => utils.isTenantAdmin(),
    isTenantUser: () => utils.isTenantUser(),
    hasRole: (role) => utils.hasRole(role),
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook para usar o contexto de autenticação
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Hook para verificar autenticação
export function useRequireAuth() {
  const { isAuthenticated, loading } = useAuth();
  
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      // Redirecionar para login se não autenticado
      window.location.href = '/login';
    }
  }, [isAuthenticated, loading]);

  return { isAuthenticated, loading };
}

// Hook para verificar role específica
export function useRequireRole(requiredRole) {
  const { user, hasRole, loading } = useAuth();
  const hasRequiredRole = hasRole(requiredRole);

  useEffect(() => {
    if (!loading && (!user || !hasRequiredRole)) {
      // Redirecionar se não tiver a role necessária
      window.location.href = '/unauthorized';
    }
  }, [user, hasRequiredRole, loading, requiredRole]);

  return { hasRequiredRole, loading };
}


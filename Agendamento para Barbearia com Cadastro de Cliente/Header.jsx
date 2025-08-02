import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger,
  DropdownMenuSeparator 
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { 
  User, 
  LogOut, 
  Settings, 
  Menu, 
  X,
  Scissors,
  MapPin
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

export function Header() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const getUserInitials = (user) => {
    if (!user) return 'U';
    const firstName = user.first_name || '';
    const lastName = user.last_name || '';
    return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
  };

  const getRoleBadge = (role) => {
    const roleMap = {
      super_admin: { label: 'Super Admin', variant: 'destructive' },
      tenant_admin: { label: 'Admin', variant: 'default' },
      tenant_user: { label: 'Funcionário', variant: 'secondary' },
    };
    
    return roleMap[role] || { label: 'Usuário', variant: 'outline' };
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo e navegação principal */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Scissors className="h-8 w-8 text-amber-600" />
              <span className="text-xl font-bold text-gray-900">
                Barbearias Brejo
              </span>
            </Link>

            {/* Navegação desktop */}
            <nav className="hidden md:ml-8 md:flex md:space-x-8">
              <Link 
                to="/barbershops" 
                className="text-gray-700 hover:text-amber-600 px-3 py-2 text-sm font-medium transition-colors"
              >
                <div className="flex items-center space-x-1">
                  <MapPin className="h-4 w-4" />
                  <span>Barbearias</span>
                </div>
              </Link>
              
              {isAuthenticated && user?.role === 'super_admin' && (
                <Link 
                  to="/admin" 
                  className="text-gray-700 hover:text-amber-600 px-3 py-2 text-sm font-medium transition-colors"
                >
                  Administração
                </Link>
              )}
              
              {isAuthenticated && (user?.role === 'tenant_admin' || user?.role === 'tenant_user') && (
                <Link 
                  to="/dashboard" 
                  className="text-gray-700 hover:text-amber-600 px-3 py-2 text-sm font-medium transition-colors"
                >
                  Dashboard
                </Link>
              )}
            </nav>
          </div>

          {/* Ações do usuário */}
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                {/* Menu do usuário */}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                      <Avatar className="h-10 w-10">
                        <AvatarImage src={user?.avatar_url} alt={user?.full_name} />
                        <AvatarFallback className="bg-amber-100 text-amber-800">
                          {getUserInitials(user)}
                        </AvatarFallback>
                      </Avatar>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent className="w-64" align="end" forceMount>
                    <div className="flex flex-col space-y-1 p-2">
                      <p className="text-sm font-medium leading-none">{user?.full_name}</p>
                      <p className="text-xs leading-none text-muted-foreground">{user?.email}</p>
                      <div className="flex items-center space-x-2 mt-2">
                        <Badge variant={getRoleBadge(user?.role).variant} className="text-xs">
                          {getRoleBadge(user?.role).label}
                        </Badge>
                        {user?.tenant && (
                          <Badge variant="outline" className="text-xs">
                            {user.tenant.name}
                          </Badge>
                        )}
                      </div>
                    </div>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={() => navigate('/profile')}>
                      <User className="mr-2 h-4 w-4" />
                      <span>Perfil</span>
                    </DropdownMenuItem>
                    {(user?.role === 'tenant_admin' || user?.role === 'tenant_user') && (
                      <DropdownMenuItem onClick={() => navigate('/settings')}>
                        <Settings className="mr-2 h-4 w-4" />
                        <span>Configurações</span>
                      </DropdownMenuItem>
                    )}
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={handleLogout}>
                      <LogOut className="mr-2 h-4 w-4" />
                      <span>Sair</span>
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </>
            ) : (
              <>
                {/* Botões para usuários não autenticados */}
                <div className="hidden md:flex md:items-center md:space-x-4">
                  <Button variant="ghost" onClick={() => navigate('/login')}>
                    Entrar
                  </Button>
                  <Button onClick={() => navigate('/register')}>
                    Cadastrar Barbearia
                  </Button>
                </div>
              </>
            )}

            {/* Menu mobile */}
            <div className="md:hidden">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                {mobileMenuOpen ? (
                  <X className="h-6 w-6" />
                ) : (
                  <Menu className="h-6 w-6" />
                )}
              </Button>
            </div>
          </div>
        </div>

        {/* Menu mobile */}
        {mobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-200">
              <Link
                to="/barbershops"
                className="text-gray-700 hover:text-amber-600 block px-3 py-2 text-base font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                <div className="flex items-center space-x-2">
                  <MapPin className="h-5 w-5" />
                  <span>Barbearias</span>
                </div>
              </Link>

              {isAuthenticated ? (
                <>
                  {user?.role === 'super_admin' && (
                    <Link
                      to="/admin"
                      className="text-gray-700 hover:text-amber-600 block px-3 py-2 text-base font-medium"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Administração
                    </Link>
                  )}
                  
                  {(user?.role === 'tenant_admin' || user?.role === 'tenant_user') && (
                    <Link
                      to="/dashboard"
                      className="text-gray-700 hover:text-amber-600 block px-3 py-2 text-base font-medium"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Dashboard
                    </Link>
                  )}

                  <div className="border-t border-gray-200 pt-4 pb-3">
                    <div className="flex items-center px-3">
                      <Avatar className="h-10 w-10">
                        <AvatarImage src={user?.avatar_url} alt={user?.full_name} />
                        <AvatarFallback className="bg-amber-100 text-amber-800">
                          {getUserInitials(user)}
                        </AvatarFallback>
                      </Avatar>
                      <div className="ml-3">
                        <div className="text-base font-medium text-gray-800">{user?.full_name}</div>
                        <div className="text-sm text-gray-500">{user?.email}</div>
                      </div>
                    </div>
                    <div className="mt-3 space-y-1 px-2">
                      <Button
                        variant="ghost"
                        className="w-full justify-start"
                        onClick={() => {
                          navigate('/profile');
                          setMobileMenuOpen(false);
                        }}
                      >
                        <User className="mr-2 h-4 w-4" />
                        Perfil
                      </Button>
                      <Button
                        variant="ghost"
                        className="w-full justify-start"
                        onClick={() => {
                          handleLogout();
                          setMobileMenuOpen(false);
                        }}
                      >
                        <LogOut className="mr-2 h-4 w-4" />
                        Sair
                      </Button>
                    </div>
                  </div>
                </>
              ) : (
                <div className="border-t border-gray-200 pt-4 pb-3 space-y-2 px-3">
                  <Button
                    variant="ghost"
                    className="w-full justify-start"
                    onClick={() => {
                      navigate('/login');
                      setMobileMenuOpen(false);
                    }}
                  >
                    Entrar
                  </Button>
                  <Button
                    className="w-full"
                    onClick={() => {
                      navigate('/register');
                      setMobileMenuOpen(false);
                    }}
                  >
                    Cadastrar Barbearia
                  </Button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  );
}


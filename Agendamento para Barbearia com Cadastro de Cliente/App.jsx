import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth.jsx';
import { Layout } from './components/Layout/Layout';
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Dashboard } from './pages/admin/Dashboard';
import { Customization } from './pages/admin/Customization';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Rotas públicas */}
          <Route path="/" element={
            <Layout>
              <Home />
            </Layout>
          } />
          
          {/* Rota de login sem layout completo */}
          <Route path="/login" element={<Login />} />
          
          {/* Rotas de admin */}
          <Route path="/admin" element={
            <Layout>
              <Dashboard />
            </Layout>
          } />
          
          <Route path="/admin/customization" element={
            <Layout>
              <Customization />
            </Layout>
          } />
          
          {/* Placeholder para outras rotas */}
          <Route path="*" element={
            <Layout>
              <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                  <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    Página em Desenvolvimento
                  </h1>
                  <p className="text-gray-600">
                    Esta funcionalidade será implementada em breve.
                  </p>
                </div>
              </div>
            </Layout>
          } />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

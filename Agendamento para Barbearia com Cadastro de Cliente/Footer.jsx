import { Link } from 'react-router-dom';
import { Scissors, MapPin, Mail, Phone, Instagram, Facebook } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo e descrição */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Scissors className="h-8 w-8 text-amber-500" />
              <span className="text-xl font-bold">Barbearias Brejo</span>
            </div>
            <p className="text-gray-300 mb-4 max-w-md">
              A plataforma que conecta você às melhores barbearias de Brejo-MA. 
              Agende seus serviços de forma rápida e prática.
            </p>
            <div className="flex items-center space-x-2 text-gray-300">
              <MapPin className="h-5 w-5 text-amber-500" />
              <span>Brejo - Maranhão</span>
            </div>
          </div>

          {/* Links rápidos */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Links Rápidos</h3>
            <ul className="space-y-2">
              <li>
                <Link 
                  to="/barbershops" 
                  className="text-gray-300 hover:text-amber-500 transition-colors"
                >
                  Encontrar Barbearias
                </Link>
              </li>
              <li>
                <Link 
                  to="/register" 
                  className="text-gray-300 hover:text-amber-500 transition-colors"
                >
                  Cadastrar Barbearia
                </Link>
              </li>
              <li>
                <Link 
                  to="/about" 
                  className="text-gray-300 hover:text-amber-500 transition-colors"
                >
                  Sobre Nós
                </Link>
              </li>
              <li>
                <Link 
                  to="/contact" 
                  className="text-gray-300 hover:text-amber-500 transition-colors"
                >
                  Contato
                </Link>
              </li>
            </ul>
          </div>

          {/* Para barbearias */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Para Barbearias</h3>
            <ul className="space-y-2">
              <li>
                <Link 
                  to="/login" 
                  className="text-gray-300 hover:text-amber-500 transition-colors"
                >
                  Área do Parceiro
                </Link>
              </li>
              <li>
                <Link 
                  to="/pricing" 
                  className="text-gray-300 hover:text-amber-500 transition-colors"
                >
                  Planos e Preços
                </Link>
              </li>
              <li>
                <Link 
                  to="/features" 
                  className="text-gray-300 hover:text-amber-500 transition-colors"
                >
                  Funcionalidades
                </Link>
              </li>
              <li>
                <Link 
                  to="/support" 
                  className="text-gray-300 hover:text-amber-500 transition-colors"
                >
                  Suporte
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Contato e redes sociais */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-6 mb-4 md:mb-0">
              <div className="flex items-center space-x-2 text-gray-300">
                <Mail className="h-4 w-4 text-amber-500" />
                <span>contato@barbeariabrejo.com</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-300">
                <Phone className="h-4 w-4 text-amber-500" />
                <span>(99) 9999-9999</span>
              </div>
            </div>

            {/* Redes sociais */}
            <div className="flex items-center space-x-4">
              <a 
                href="#" 
                className="text-gray-300 hover:text-amber-500 transition-colors"
                aria-label="Instagram"
              >
                <Instagram className="h-5 w-5" />
              </a>
              <a 
                href="#" 
                className="text-gray-300 hover:text-amber-500 transition-colors"
                aria-label="Facebook"
              >
                <Facebook className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-800 mt-8 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} Barbearias Brejo. Todos os direitos reservados.
          </p>
          <div className="flex justify-center space-x-6 mt-2">
            <Link 
              to="/privacy" 
              className="text-gray-400 hover:text-amber-500 text-sm transition-colors"
            >
              Política de Privacidade
            </Link>
            <Link 
              to="/terms" 
              className="text-gray-400 hover:text-amber-500 text-sm transition-colors"
            >
              Termos de Uso
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}


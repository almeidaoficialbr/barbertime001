import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Search, 
  MapPin, 
  Star, 
  Clock, 
  Scissors, 
  Users, 
  Calendar,
  CheckCircle,
  ArrowRight
} from 'lucide-react';
import { publicService } from '../lib/api';
import heroImage from '../assets/hero-bg.jpg';

export function Home() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [featuredBarbershops, setFeaturedBarbershops] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFeaturedBarbershops();
  }, []);

  const loadFeaturedBarbershops = async () => {
    try {
      const response = await publicService.getBarbershops({ per_page: 3 });
      setFeaturedBarbershops(response.barbershops || []);
    } catch (error) {
      console.error('Erro ao carregar barbearias:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    navigate(`/barbershops?search=${encodeURIComponent(searchTerm)}`);
  };

  const features = [
    {
      icon: Calendar,
      title: 'Agendamento Online',
      description: 'Agende seus serviços 24/7 de forma rápida e prática'
    },
    {
      icon: MapPin,
      title: 'Localização Fácil',
      description: 'Encontre barbearias próximas a você em Brejo-MA'
    },
    {
      icon: Star,
      title: 'Avaliações Reais',
      description: 'Veja avaliações de outros clientes antes de escolher'
    },
    {
      icon: Users,
      title: 'Profissionais Qualificados',
      description: 'Conecte-se com os melhores barbeiros da região'
    }
  ];

  const benefits = [
    'Agendamento online 24 horas',
    'Confirmação automática por WhatsApp',
    'Histórico de serviços',
    'Avaliações e comentários',
    'Lembretes de agendamento',
    'Cancelamento fácil'
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section 
        className="relative bg-cover bg-center bg-no-repeat py-24 lg:py-32"
        style={{ backgroundImage: `url(${heroImage})` }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-60"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Encontre a Melhor
              <span className="text-amber-500 block">Barbearia em Brejo</span>
            </h1>
            <p className="text-xl text-gray-200 mb-8 max-w-3xl mx-auto">
              Agende seus serviços de forma rápida e prática. 
              Conectamos você aos melhores profissionais da região.
            </p>

            {/* Barra de busca */}
            <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <Input
                    type="text"
                    placeholder="Buscar barbearias..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 h-12 text-lg bg-white"
                  />
                </div>
                <Button type="submit" size="lg" className="h-12 px-8">
                  <Search className="mr-2 h-5 w-5" />
                  Buscar
                </Button>
              </div>
            </form>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" onClick={() => navigate('/barbershops')}>
                <MapPin className="mr-2 h-5 w-5" />
                Ver Todas as Barbearias
              </Button>
              <Button variant="outline" size="lg" onClick={() => navigate('/register')}>
                <Scissors className="mr-2 h-5 w-5" />
                Cadastrar Minha Barbearia
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Por que escolher nossa plataforma?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Oferecemos a melhor experiência para conectar clientes e barbearias
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="mx-auto w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center mb-4">
                    <feature.icon className="h-6 w-6 text-amber-600" />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-600">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Barbershops */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Barbearias em Destaque
            </h2>
            <p className="text-xl text-gray-600">
              Conheça algumas das melhores barbearias de Brejo-MA
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[1, 2, 3].map((i) => (
                <Card key={i} className="animate-pulse">
                  <div className="h-48 bg-gray-200 rounded-t-lg"></div>
                  <CardHeader>
                    <div className="h-6 bg-gray-200 rounded mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  </CardHeader>
                </Card>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {featuredBarbershops.map((barbershop) => (
                <Card key={barbershop.id} className="hover:shadow-lg transition-shadow cursor-pointer">
                  <div 
                    className="h-48 bg-gradient-to-r from-gray-800 to-gray-600 rounded-t-lg flex items-center justify-center"
                    style={{
                      backgroundImage: barbershop.logo_url ? `url(${barbershop.logo_url})` : 'none',
                      backgroundSize: 'cover',
                      backgroundPosition: 'center'
                    }}
                  >
                    {!barbershop.logo_url && (
                      <Scissors className="h-16 w-16 text-white opacity-50" />
                    )}
                  </div>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-lg">{barbershop.business_name}</CardTitle>
                        <CardDescription className="flex items-center mt-1">
                          <MapPin className="h-4 w-4 mr-1" />
                          {barbershop.city}, {barbershop.state}
                        </CardDescription>
                      </div>
                      <Badge variant="secondary" className="flex items-center">
                        <Star className="h-3 w-3 mr-1 fill-current" />
                        {barbershop.rating}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-4 line-clamp-2">
                      {barbershop.description || 'Tradição e modernidade em cada corte'}
                    </p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center text-sm text-gray-500">
                        <Clock className="h-4 w-4 mr-1" />
                        <span>{barbershop.status === 'open' ? 'Aberto' : 'Fechado'}</span>
                      </div>
                      <Button 
                        size="sm" 
                        onClick={() => navigate(`/barbershop/${barbershop.slug}`)}
                      >
                        Ver Detalhes
                        <ArrowRight className="ml-1 h-4 w-4" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <Button size="lg" onClick={() => navigate('/barbershops')}>
              Ver Todas as Barbearias
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16 bg-amber-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Vantagens de usar nossa plataforma
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                Simplifique sua experiência de agendamento e descubra os melhores 
                profissionais de Brejo-MA.
              </p>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>

              <div className="mt-8">
                <Button size="lg" onClick={() => navigate('/barbershops')}>
                  Começar Agora
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </div>
            </div>

            <div className="relative">
              <div className="bg-white rounded-lg shadow-xl p-8">
                <div className="text-center">
                  <div className="w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Calendar className="h-8 w-8 text-amber-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    Agendamento Simples
                  </h3>
                  <p className="text-gray-600 mb-6">
                    Em poucos cliques você agenda seu horário na barbearia de sua preferência
                  </p>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-600">1. Escolha a barbearia</span>
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    </div>
                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-600">2. Selecione o serviço</span>
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    </div>
                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-600">3. Confirme o horário</span>
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Tem uma barbearia em Brejo?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Cadastre sua barbearia em nossa plataforma e alcance mais clientes. 
            Gerencie agendamentos, funcionários e muito mais.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="outline" onClick={() => navigate('/register')}>
              <Scissors className="mr-2 h-5 w-5" />
              Cadastrar Barbearia
            </Button>
            <Button size="lg" onClick={() => navigate('/features')}>
              Ver Funcionalidades
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}


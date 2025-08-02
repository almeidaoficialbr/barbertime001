import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Upload, Palette, Info, Clock, FileText, Eye } from 'lucide-react';
import { api } from '@/lib/api';

export function Customization() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  
  // Estados para diferentes seções
  const [theme, setTheme] = useState({
    primary_color: '#1A1A1A',
    secondary_color: '#B8860B',
    accent_color: '#8B0000',
    logo_url: null
  });
  
  const [businessInfo, setBusinessInfo] = useState({
    business_name: '',
    description: '',
    address: '',
    city: 'Brejo',
    state: 'MA',
    zip_code: '',
    phone: '',
    email: '',
    website: '',
    instagram: '',
    facebook: '',
    whatsapp: ''
  });
  
  const [openingHours, setOpeningHours] = useState({
    monday: { open: '08:00', close: '18:00', closed: false },
    tuesday: { open: '08:00', close: '18:00', closed: false },
    wednesday: { open: '08:00', close: '18:00', closed: false },
    thursday: { open: '08:00', close: '18:00', closed: false },
    friday: { open: '08:00', close: '18:00', closed: false },
    saturday: { open: '08:00', close: '16:00', closed: false },
    sunday: { open: '08:00', close: '16:00', closed: true }
  });
  
  const [policies, setPolicies] = useState({
    cancellation_policy: '',
    terms_of_service: '',
    privacy_policy: ''
  });

  const dayNames = {
    monday: 'Segunda-feira',
    tuesday: 'Terça-feira',
    wednesday: 'Quarta-feira',
    thursday: 'Quinta-feira',
    friday: 'Sexta-feira',
    saturday: 'Sábado',
    sunday: 'Domingo'
  };

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Carregar dados em paralelo
      const [themeRes, businessRes, hoursRes, policiesRes] = await Promise.all([
        api.get('/customization/theme'),
        api.get('/customization/business-info'),
        api.get('/customization/opening-hours'),
        api.get('/customization/policies')
      ]);
      
      if (themeRes.data.theme) {
        setTheme(themeRes.data.theme);
      }
      
      if (businessRes.data.business_info) {
        setBusinessInfo(businessRes.data.business_info);
      }
      
      if (hoursRes.data.opening_hours) {
        setOpeningHours(hoursRes.data.opening_hours);
      }
      
      if (policiesRes.data.policies) {
        setPolicies(policiesRes.data.policies);
      }
      
    } catch (error) {
      showMessage('Erro ao carregar dados de personalização', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (text, type = 'success') => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => {
      setMessage('');
      setMessageType('');
    }, 5000);
  };

  const handleLogoUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validar tipo de arquivo
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/svg+xml'];
    if (!allowedTypes.includes(file.type)) {
      showMessage('Tipo de arquivo não permitido. Use PNG, JPG, GIF ou SVG.', 'error');
      return;
    }

    // Validar tamanho (5MB)
    if (file.size > 5 * 1024 * 1024) {
      showMessage('Arquivo muito grande. Máximo 5MB.', 'error');
      return;
    }

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/upload/logo', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setTheme(prev => ({
        ...prev,
        logo_url: response.data.logo_urls.original
      }));

      showMessage('Logo enviado com sucesso!');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Erro ao enviar logo', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleThemeUpdate = async () => {
    try {
      setLoading(true);
      await api.put('/customization/theme', { ...theme });
      showMessage('Tema atualizado com sucesso!');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Erro ao atualizar tema', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleBusinessInfoUpdate = async () => {
    try {
      setLoading(true);
      await api.put('/customization/business-info', { ...businessInfo });
      showMessage('Informações atualizadas com sucesso!');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Erro ao atualizar informações', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleOpeningHoursUpdate = async () => {
    try {
      setLoading(true);
      await api.put('/customization/opening-hours', { opening_hours: openingHours });
      showMessage('Horários atualizados com sucesso!');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Erro ao atualizar horários', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handlePoliciesUpdate = async () => {
    try {
      setLoading(true);
      await api.put('/customization/policies', { policies });
      showMessage('Políticas atualizadas com sucesso!');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Erro ao atualizar políticas', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = () => {
    // Abrir preview em nova aba
    window.open('/', '_blank');
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Personalização</h1>
          <p className="text-gray-600">Configure a aparência e informações da sua barbearia</p>
        </div>
        <Button onClick={handlePreview} variant="outline">
          <Eye className="w-4 h-4 mr-2" />
          Visualizar Site
        </Button>
      </div>

      {message && (
        <Alert className={messageType === 'error' ? 'border-red-500 bg-red-50' : 'border-green-500 bg-green-50'}>
          <AlertDescription className={messageType === 'error' ? 'text-red-700' : 'text-green-700'}>
            {message}
          </AlertDescription>
        </Alert>
      )}

      <Tabs defaultValue="theme" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="theme" className="flex items-center gap-2">
            <Palette className="w-4 h-4" />
            Tema
          </TabsTrigger>
          <TabsTrigger value="business" className="flex items-center gap-2">
            <Info className="w-4 h-4" />
            Informações
          </TabsTrigger>
          <TabsTrigger value="hours" className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            Horários
          </TabsTrigger>
          <TabsTrigger value="policies" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            Políticas
          </TabsTrigger>
        </TabsList>

        <TabsContent value="theme">
          <Card>
            <CardHeader>
              <CardTitle>Tema e Identidade Visual</CardTitle>
              <CardDescription>
                Configure as cores e logo da sua barbearia
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Upload de Logo */}
              <div className="space-y-2">
                <Label>Logo da Barbearia</Label>
                <div className="flex items-center gap-4">
                  {theme.logo_url && (
                    <img 
                      src={theme.logo_url} 
                      alt="Logo atual" 
                      className="w-16 h-16 object-contain border rounded"
                    />
                  )}
                  <div>
                    <Input
                      type="file"
                      accept="image/*"
                      onChange={handleLogoUpload}
                      className="hidden"
                      id="logo-upload"
                    />
                    <Label htmlFor="logo-upload" className="cursor-pointer">
                      <div className="flex items-center gap-2 px-4 py-2 border rounded-md hover:bg-gray-50">
                        <Upload className="w-4 h-4" />
                        Enviar Logo
                      </div>
                    </Label>
                    <p className="text-sm text-gray-500 mt-1">
                      PNG, JPG, GIF ou SVG. Máximo 5MB.
                    </p>
                  </div>
                </div>
              </div>

              {/* Cores */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label>Cor Primária</Label>
                  <div className="flex items-center gap-2">
                    <Input
                      type="color"
                      value={theme.primary_color}
                      onChange={(e) => setTheme(prev => ({ ...prev, primary_color: e.target.value }))}
                      className="w-12 h-10 p-1 border rounded"
                    />
                    <Input
                      type="text"
                      value={theme.primary_color}
                      onChange={(e) => setTheme(prev => ({ ...prev, primary_color: e.target.value }))}
                      placeholder="#1A1A1A"
                      className="flex-1"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Cor Secundária</Label>
                  <div className="flex items-center gap-2">
                    <Input
                      type="color"
                      value={theme.secondary_color}
                      onChange={(e) => setTheme(prev => ({ ...prev, secondary_color: e.target.value }))}
                      className="w-12 h-10 p-1 border rounded"
                    />
                    <Input
                      type="text"
                      value={theme.secondary_color}
                      onChange={(e) => setTheme(prev => ({ ...prev, secondary_color: e.target.value }))}
                      placeholder="#B8860B"
                      className="flex-1"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Cor de Destaque</Label>
                  <div className="flex items-center gap-2">
                    <Input
                      type="color"
                      value={theme.accent_color}
                      onChange={(e) => setTheme(prev => ({ ...prev, accent_color: e.target.value }))}
                      className="w-12 h-10 p-1 border rounded"
                    />
                    <Input
                      type="text"
                      value={theme.accent_color}
                      onChange={(e) => setTheme(prev => ({ ...prev, accent_color: e.target.value }))}
                      placeholder="#8B0000"
                      className="flex-1"
                    />
                  </div>
                </div>
              </div>

              {/* Preview das cores */}
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium mb-3">Preview das Cores</h4>
                <div className="flex gap-4">
                  <div 
                    className="w-16 h-16 rounded-lg border"
                    style={{ backgroundColor: theme.primary_color }}
                    title="Cor Primária"
                  />
                  <div 
                    className="w-16 h-16 rounded-lg border"
                    style={{ backgroundColor: theme.secondary_color }}
                    title="Cor Secundária"
                  />
                  <div 
                    className="w-16 h-16 rounded-lg border"
                    style={{ backgroundColor: theme.accent_color }}
                    title="Cor de Destaque"
                  />
                </div>
              </div>

              <Button onClick={handleThemeUpdate} disabled={loading}>
                Salvar Tema
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="business">
          <Card>
            <CardHeader>
              <CardTitle>Informações da Barbearia</CardTitle>
              <CardDescription>
                Configure as informações que aparecerão no seu site
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Nome da Barbearia</Label>
                  <Input
                    value={businessInfo.business_name || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, business_name: e.target.value }))}
                    placeholder="Ex: Barbearia Clássica"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Email</Label>
                  <Input
                    type="email"
                    value={businessInfo.email || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, email: e.target.value }))}
                    placeholder="contato@barbearia.com"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Telefone</Label>
                  <Input
                    value={businessInfo.phone || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, phone: e.target.value }))}
                    placeholder="(99) 99999-9999"
                  />
                </div>

                <div className="space-y-2">
                  <Label>WhatsApp</Label>
                  <Input
                    value={businessInfo.whatsapp || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, whatsapp: e.target.value }))}
                    placeholder="(99) 99999-9999"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Descrição</Label>
                <Textarea
                  value={businessInfo.description || ''}
                  onChange={(e) => setBusinessInfo(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Descreva sua barbearia, serviços e diferenciais..."
                  rows={3}
                />
              </div>

              <div className="space-y-2">
                <Label>Endereço</Label>
                <Textarea
                  value={businessInfo.address || ''}
                  onChange={(e) => setBusinessInfo(prev => ({ ...prev, address: e.target.value }))}
                  placeholder="Rua, número, bairro..."
                  rows={2}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label>Cidade</Label>
                  <Input
                    value={businessInfo.city || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, city: e.target.value }))}
                    placeholder="Brejo"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Estado</Label>
                  <Input
                    value={businessInfo.state || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, state: e.target.value }))}
                    placeholder="MA"
                    maxLength={2}
                  />
                </div>

                <div className="space-y-2">
                  <Label>CEP</Label>
                  <Input
                    value={businessInfo.zip_code || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, zip_code: e.target.value }))}
                    placeholder="00000-000"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label>Website</Label>
                  <Input
                    value={businessInfo.website || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, website: e.target.value }))}
                    placeholder="https://www.barbearia.com"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Instagram</Label>
                  <Input
                    value={businessInfo.instagram || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, instagram: e.target.value }))}
                    placeholder="@barbearia"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Facebook</Label>
                  <Input
                    value={businessInfo.facebook || ''}
                    onChange={(e) => setBusinessInfo(prev => ({ ...prev, facebook: e.target.value }))}
                    placeholder="facebook.com/barbearia"
                  />
                </div>
              </div>

              <Button onClick={handleBusinessInfoUpdate} disabled={loading}>
                Salvar Informações
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="hours">
          <Card>
            <CardHeader>
              <CardTitle>Horários de Funcionamento</CardTitle>
              <CardDescription>
                Configure os horários de funcionamento da sua barbearia
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {Object.entries(openingHours).map(([day, hours]) => (
                <div key={day} className="flex items-center gap-4 p-4 border rounded-lg">
                  <div className="w-32">
                    <Label className="font-medium">{dayNames[day]}</Label>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <Switch
                      checked={!hours.closed}
                      onCheckedChange={(checked) => 
                        setOpeningHours(prev => ({
                          ...prev,
                          [day]: { ...prev[day], closed: !checked }
                        }))
                      }
                    />
                    <Label className="text-sm">
                      {hours.closed ? 'Fechado' : 'Aberto'}
                    </Label>
                  </div>

                  {!hours.closed && (
                    <>
                      <div className="flex items-center gap-2">
                        <Label className="text-sm">Abertura:</Label>
                        <Input
                          type="time"
                          value={hours.open}
                          onChange={(e) => 
                            setOpeningHours(prev => ({
                              ...prev,
                              [day]: { ...prev[day], open: e.target.value }
                            }))
                          }
                          className="w-32"
                        />
                      </div>

                      <div className="flex items-center gap-2">
                        <Label className="text-sm">Fechamento:</Label>
                        <Input
                          type="time"
                          value={hours.close}
                          onChange={(e) => 
                            setOpeningHours(prev => ({
                              ...prev,
                              [day]: { ...prev[day], close: e.target.value }
                            }))
                          }
                          className="w-32"
                        />
                      </div>
                    </>
                  )}
                </div>
              ))}

              <Button onClick={handleOpeningHoursUpdate} disabled={loading}>
                Salvar Horários
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="policies">
          <Card>
            <CardHeader>
              <CardTitle>Políticas e Termos</CardTitle>
              <CardDescription>
                Configure as políticas da sua barbearia
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Política de Cancelamento</Label>
                <Textarea
                  value={policies.cancellation_policy || ''}
                  onChange={(e) => setPolicies(prev => ({ ...prev, cancellation_policy: e.target.value }))}
                  placeholder="Descreva sua política de cancelamento de agendamentos..."
                  rows={4}
                />
              </div>

              <div className="space-y-2">
                <Label>Termos de Serviço</Label>
                <Textarea
                  value={policies.terms_of_service || ''}
                  onChange={(e) => setPolicies(prev => ({ ...prev, terms_of_service: e.target.value }))}
                  placeholder="Descreva os termos de uso dos seus serviços..."
                  rows={4}
                />
              </div>

              <div className="space-y-2">
                <Label>Política de Privacidade</Label>
                <Textarea
                  value={policies.privacy_policy || ''}
                  onChange={(e) => setPolicies(prev => ({ ...prev, privacy_policy: e.target.value }))}
                  placeholder="Descreva como os dados dos clientes são tratados..."
                  rows={4}
                />
              </div>

              <Button onClick={handlePoliciesUpdate} disabled={loading}>
                Salvar Políticas
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}


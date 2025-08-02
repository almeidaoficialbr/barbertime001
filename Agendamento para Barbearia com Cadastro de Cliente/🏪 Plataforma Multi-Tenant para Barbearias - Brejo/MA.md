# 🏪 Plataforma Multi-Tenant para Barbearias - Brejo/MA

Uma plataforma SaaS completa que permite a barbearias criar seus próprios sites de agendamento online, com personalização total e dados isolados por tenant.

## 🎯 **Visão Geral**

Esta plataforma permite que múltiplas barbearias tenham seus próprios ambientes personalizados, onde cada uma pode:
- Personalizar cores, logo e informações
- Gerenciar seus próprios clientes e agendamentos
- Ter dados completamente isolados de outras barbearias
- Oferecer agendamento online 24/7 para seus clientes

## 🏗️ **Arquitetura**

- **Backend**: Flask (Python) com arquitetura multi-tenant
- **Frontend**: React com Tailwind CSS
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação**: JWT com isolamento por tenant
- **Upload de Arquivos**: Suporte para logos personalizados

## 📋 **Funcionalidades Principais**

### Para Barbearias (Tenants):
- ✅ Login individual e dados privados
- ✅ Personalização completa (cores, logo, informações)
- ✅ Gestão de serviços e preços
- ✅ Gestão de funcionários e horários
- ✅ Gestão de clientes
- ✅ Sistema de agendamentos
- ✅ Relatórios e analytics
- ✅ Configuração de horários de funcionamento
- ✅ Políticas personalizadas

### Para Clientes:
- ✅ Busca de barbearias em Brejo/MA
- ✅ Agendamento online 24/7
- ✅ Interface personalizada por barbearia
- ✅ Histórico de agendamentos

## 🚀 **Instalação e Execução**

### Pré-requisitos
- Python 3.8+
- Node.js 16+
- npm ou yarn

### 1. Backend (Flask)

```bash
# Navegar para o diretório do backend
cd barbershop-platform

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências (se necessário)
pip install -r requirements.txt

# Iniciar servidor
python src/main.py
```

O backend estará rodando em: `http://localhost:5000`

### 2. Frontend (React)

```bash
# Navegar para o diretório do frontend
cd barbershop-frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estará rodando em: `http://localhost:5173`

## 🔐 **Credenciais Padrão**

### Super Administrador
- **Email**: admin@barbershop-platform.com
- **Senha**: admin123

### Barbearia de Teste
- **Nome**: Barbearia do João
- **Slug**: barbearia-joao
- **Admin**: joao@barbearia.com / senha123

## 📁 **Estrutura do Projeto**

```
plataforma-multi-tenant/
├── barbershop-platform/          # Backend Flask
│   ├── src/
│   │   ├── models/               # Modelos de dados
│   │   ├── routes/               # Rotas da API
│   │   ├── middleware/           # Middleware de tenant
│   │   └── main.py              # Arquivo principal
│   ├── venv/                    # Ambiente virtual Python
│   └── requirements.txt         # Dependências Python
│
├── barbershop-frontend/          # Frontend React
│   ├── src/
│   │   ├── components/          # Componentes React
│   │   ├── pages/               # Páginas da aplicação
│   │   ├── hooks/               # Hooks personalizados
│   │   └── lib/                 # Utilitários
│   ├── package.json             # Dependências Node.js
│   └── vite.config.js           # Configuração Vite
│
└── README_PLATAFORMA.md         # Esta documentação
```

## 🔧 **Configuração para Produção**

### Variáveis de Ambiente (.env)
```env
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_super_segura
DATABASE_URL=postgresql://usuario:senha@localhost/barbershop_platform
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=5242880
CORS_ORIGINS=https://seu-dominio.com
```

### Deploy do Backend
1. Configure PostgreSQL
2. Atualize as variáveis de ambiente
3. Execute as migrações: `python src/main.py`
4. Configure servidor WSGI (Gunicorn)

### Deploy do Frontend
1. Build da aplicação: `npm run build`
2. Configure servidor web (Nginx)
3. Aponte para o diretório `dist/`

## 🎨 **Personalização**

Cada barbearia pode personalizar:
- **Cores**: Primária, secundária e de destaque
- **Logo**: Upload de imagem personalizada
- **Informações**: Nome, descrição, contatos
- **Horários**: Funcionamento por dia da semana
- **Políticas**: Cancelamento, termos, privacidade

## 📊 **Planos de Assinatura**

- **Básico**: R$ 49/mês - Funcionalidades essenciais
- **Profissional**: R$ 99/mês - Recursos avançados
- **Premium**: R$ 199/mês - Todos os recursos

## 🔒 **Segurança**

- Isolamento completo de dados por tenant
- Autenticação JWT segura
- Middleware de resolução automática de tenant
- Validação de permissões em todas as rotas
- Upload seguro de arquivos

## 🐛 **Solução de Problemas**

### Backend não inicia
```bash
cd barbershop-platform
source venv/bin/activate
python src/main.py
```

### Frontend não carrega
```bash
cd barbershop-frontend
npm install
npm run dev
```

### Erro de CORS
Verifique se o backend está rodando na porta 5000 e o frontend na 5173.

## 📞 **Suporte**

Para dúvidas ou problemas:
1. Verifique a documentação
2. Consulte os logs de erro
3. Entre em contato com o suporte técnico

---

**Desenvolvido para barbearias de Brejo/MA** 💈


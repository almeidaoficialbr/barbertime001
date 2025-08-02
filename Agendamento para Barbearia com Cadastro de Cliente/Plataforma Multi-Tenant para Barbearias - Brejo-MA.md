# Plataforma Multi-Tenant para Barbearias - Brejo-MA

## Visão Geral do Projeto

### Conceito
Desenvolver uma plataforma SaaS (Software as a Service) que permita múltiplas barbearias da cidade de Brejo-MA terem seus próprios ambientes personalizados e seguros, onde cada estabelecimento pode gerenciar seus clientes e agendamentos de forma independente.

### Objetivos Principais
1. **Isolamento de Dados**: Cada barbearia terá acesso apenas aos seus próprios dados
2. **Personalização**: Interface customizável por barbearia (cores, logo, informações)
3. **Busca Local**: Clientes podem encontrar barbearias em Brejo-MA
4. **Agendamento Integrado**: Sistema completo de agendamento por barbearia
5. **Gestão Centralizada**: Painel administrativo para cada barbearia

## Arquitetura Multi-Tenant

### Modelo de Tenancy
**Tenant por Schema (Database-per-Tenant)**
- Cada barbearia terá seu próprio schema no banco de dados
- Isolamento completo de dados
- Melhor segurança e performance
- Facilita backup e migração individual

### Estrutura de Usuários
1. **Super Admin**: Administrador da plataforma
2. **Tenant Admin**: Proprietário/gerente da barbearia
3. **Tenant User**: Funcionários da barbearia
4. **Cliente**: Usuários finais que fazem agendamentos

## Funcionalidades por Tipo de Usuário

### Super Admin (Plataforma)
- Cadastrar novas barbearias
- Gerenciar planos e assinaturas
- Monitorar uso da plataforma
- Suporte técnico
- Analytics gerais

### Tenant Admin (Barbearia)
- Configurar dados da barbearia
- Personalizar interface (cores, logo, informações)
- Gerenciar funcionários
- Configurar serviços e preços
- Definir horários de funcionamento
- Relatórios e analytics
- Gerenciar agendamentos

### Tenant User (Funcionário)
- Visualizar agendamentos do dia
- Confirmar/cancelar agendamentos
- Atualizar status dos serviços
- Cadastrar novos clientes

### Cliente
- Buscar barbearias em Brejo-MA
- Visualizar informações da barbearia
- Agendar serviços
- Gerenciar seus agendamentos
- Avaliar serviços

## Estrutura do Banco de Dados

### Schema Principal (Platform)
```sql
-- Tabela de Tenants (Barbearias)
tenants:
- id (PK)
- name (nome da barbearia)
- slug (identificador único)
- domain (subdomínio personalizado)
- status (ativo/inativo)
- plan_id (plano contratado)
- created_at
- updated_at

-- Configurações do Tenant
tenant_configs:
- tenant_id (FK)
- logo_url
- primary_color
- secondary_color
- address
- phone
- email
- description
- opening_hours (JSON)

-- Usuários da Plataforma
platform_users:
- id (PK)
- tenant_id (FK)
- email
- password_hash
- role (super_admin, tenant_admin, tenant_user)
- status
- created_at
```

### Schema por Tenant (Cada Barbearia)
```sql
-- Clientes da barbearia
clients:
- id (PK)
- name
- email
- phone
- birth_date
- preferences (JSON)
- created_at

-- Serviços oferecidos
services:
- id (PK)
- name
- description
- duration (minutos)
- price
- active
- created_at

-- Funcionários
staff:
- id (PK)
- user_id (FK para platform_users)
- name
- specialties (JSON)
- schedule (JSON)
- active

-- Agendamentos
appointments:
- id (PK)
- client_id (FK)
- staff_id (FK)
- service_id (FK)
- appointment_date
- start_time
- end_time
- status (agendado, confirmado, concluído, cancelado)
- notes
- created_at

-- Avaliações
reviews:
- id (PK)
- client_id (FK)
- appointment_id (FK)
- rating (1-5)
- comment
- created_at
```

## Tecnologias e Stack

### Backend
- **Python 3.11+**
- **Flask 2.3+** com extensões:
  - Flask-SQLAlchemy (ORM)
  - Flask-Migrate (migrações)
  - Flask-JWT-Extended (autenticação)
  - Flask-CORS (CORS)
  - Flask-Mail (emails)
- **PostgreSQL** (banco principal)
- **Redis** (cache e sessões)
- **Celery** (tarefas assíncronas)

### Frontend
- **React 18+** com:
  - React Router (roteamento)
  - Material-UI ou Tailwind CSS (UI)
  - Axios (HTTP client)
  - React Query (cache de dados)
- **TypeScript** (tipagem)
- **Vite** (build tool)

### Infraestrutura
- **Docker** (containerização)
- **Nginx** (proxy reverso)
- **Let's Encrypt** (SSL)
- **AWS/DigitalOcean** (hospedagem)

## Fluxo de Funcionamento

### 1. Cadastro de Barbearia
1. Super admin cadastra nova barbearia
2. Sistema cria tenant e schema dedicado
3. Barbearia recebe credenciais de acesso
4. Configuração inicial (dados, personalização)

### 2. Acesso do Cliente
1. Cliente acessa plataforma
2. Busca por barbearias em Brejo-MA
3. Seleciona barbearia desejada
4. Visualiza serviços e horários
5. Realiza agendamento

### 3. Gestão pela Barbearia
1. Login no painel administrativo
2. Visualização de agendamentos
3. Gestão de clientes e serviços
4. Relatórios e analytics

## Segurança e Isolamento

### Isolamento de Dados
- Schema separado por tenant
- Middleware de tenant resolution
- Validação de acesso em todas as queries
- Logs de auditoria por tenant

### Autenticação e Autorização
- JWT tokens com tenant_id
- Roles e permissões por tenant
- Rate limiting por tenant
- Criptografia de dados sensíveis

### Backup e Recuperação
- Backup automático por tenant
- Restore individual por barbearia
- Versionamento de dados

## Personalização por Tenant

### Visual
- Logo personalizado
- Cores primária e secundária
- Tema customizado
- Layout adaptável

### Funcional
- Serviços específicos
- Horários de funcionamento
- Políticas de cancelamento
- Métodos de pagamento

### Comunicação
- Templates de email personalizados
- Mensagens automáticas
- Notificações customizadas

## Monetização

### Planos de Assinatura
1. **Básico**: R$ 49/mês
   - Até 100 agendamentos/mês
   - 1 funcionário
   - Personalização básica

2. **Profissional**: R$ 99/mês
   - Agendamentos ilimitados
   - Até 5 funcionários
   - Personalização completa
   - Relatórios avançados

3. **Enterprise**: R$ 199/mês
   - Recursos ilimitados
   - API personalizada
   - Suporte prioritário
   - Integrações avançadas

## Roadmap de Desenvolvimento

### Fase 1 (MVP) - 4 semanas
- Arquitetura multi-tenant básica
- Sistema de autenticação
- CRUD de barbearias e agendamentos
- Interface básica para clientes

### Fase 2 - 3 semanas
- Personalização visual
- Busca por localização
- Sistema de notificações
- Painel administrativo

### Fase 3 - 2 semanas
- Relatórios e analytics
- Sistema de avaliações
- Integração com pagamentos
- Otimizações de performance

### Fase 4 - 1 semana
- Testes finais
- Deploy em produção
- Documentação
- Treinamento

## Considerações Técnicas

### Performance
- Cache Redis para dados frequentes
- Indexação otimizada no PostgreSQL
- CDN para assets estáticos
- Lazy loading no frontend

### Escalabilidade
- Arquitetura horizontal
- Load balancing
- Database sharding se necessário
- Microserviços para funcionalidades específicas

### Monitoramento
- Logs centralizados
- Métricas de performance
- Alertas automáticos
- Health checks

## Próximos Passos

1. Validar arquitetura com stakeholders
2. Configurar ambiente de desenvolvimento
3. Implementar estrutura base multi-tenant
4. Desenvolver sistema de autenticação
5. Criar interfaces básicas
6. Implementar funcionalidades core
7. Testes e refinamentos
8. Deploy e lançamento


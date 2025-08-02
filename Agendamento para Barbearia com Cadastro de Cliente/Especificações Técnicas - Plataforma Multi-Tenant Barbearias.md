# Especificações Técnicas - Plataforma Multi-Tenant Barbearias

## Modelo de Dados Detalhado

### Schema Principal (platform)

#### Tabela: tenants
```sql
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    domain VARCHAR(255) UNIQUE,
    status VARCHAR(20) DEFAULT 'active',
    plan_id INTEGER,
    subscription_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
```

#### Tabela: tenant_configs
```sql
CREATE TABLE tenant_configs (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    logo_url VARCHAR(500),
    primary_color VARCHAR(7) DEFAULT '#1A1A1A',
    secondary_color VARCHAR(7) DEFAULT '#B8860B',
    accent_color VARCHAR(7) DEFAULT '#8B0000',
    business_name VARCHAR(255),
    description TEXT,
    address TEXT,
    city VARCHAR(100) DEFAULT 'Brejo',
    state VARCHAR(2) DEFAULT 'MA',
    zip_code VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    instagram VARCHAR(100),
    facebook VARCHAR(100),
    whatsapp VARCHAR(20),
    opening_hours JSONB,
    policies JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela: platform_users
```sql
CREATE TABLE platform_users (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) NOT NULL, -- super_admin, tenant_admin, tenant_user
    status VARCHAR(20) DEFAULT 'active',
    last_login_at TIMESTAMP,
    email_verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela: subscription_plans
```sql
CREATE TABLE subscription_plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    billing_cycle VARCHAR(20), -- monthly, yearly
    max_appointments INTEGER,
    max_staff INTEGER,
    features JSONB,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Schema por Tenant (tenant_{slug})

#### Tabela: clients
```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    birth_date DATE,
    gender VARCHAR(10),
    preferences JSONB,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela: services
```sql
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    duration INTEGER NOT NULL, -- em minutos
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(100),
    active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela: staff
```sql
CREATE TABLE staff (
    id SERIAL PRIMARY KEY,
    platform_user_id INTEGER, -- referência para platform_users
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    nickname VARCHAR(50),
    specialties JSONB,
    working_hours JSONB,
    hourly_rate DECIMAL(10,2),
    commission_rate DECIMAL(5,2),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela: appointments
```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    staff_id INTEGER REFERENCES staff(id),
    service_id INTEGER REFERENCES services(id),
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, confirmed, in_progress, completed, cancelled, no_show
    total_price DECIMAL(10,2),
    payment_status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(50),
    notes TEXT,
    client_notes TEXT,
    reminder_sent BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela: reviews
```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    appointment_id INTEGER REFERENCES appointments(id),
    staff_id INTEGER REFERENCES staff(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    response TEXT,
    responded_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela: working_hours
```sql
CREATE TABLE working_hours (
    id SERIAL PRIMARY KEY,
    staff_id INTEGER REFERENCES staff(id),
    day_of_week INTEGER CHECK (day_of_week >= 0 AND day_of_week <= 6), -- 0=domingo
    start_time TIME,
    end_time TIME,
    break_start TIME,
    break_end TIME,
    active BOOLEAN DEFAULT true
);
```

#### Tabela: blocked_times
```sql
CREATE TABLE blocked_times (
    id SERIAL PRIMARY KEY,
    staff_id INTEGER REFERENCES staff(id),
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## APIs e Endpoints

### Autenticação
```
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
POST /api/auth/forgot-password
POST /api/auth/reset-password
GET  /api/auth/me
```

### Gestão de Tenants (Super Admin)
```
GET    /api/admin/tenants
POST   /api/admin/tenants
GET    /api/admin/tenants/{id}
PUT    /api/admin/tenants/{id}
DELETE /api/admin/tenants/{id}
POST   /api/admin/tenants/{id}/activate
POST   /api/admin/tenants/{id}/deactivate
```

### Configurações do Tenant
```
GET  /api/tenant/config
PUT  /api/tenant/config
POST /api/tenant/config/logo
```

### Gestão de Funcionários
```
GET    /api/staff
POST   /api/staff
GET    /api/staff/{id}
PUT    /api/staff/{id}
DELETE /api/staff/{id}
GET    /api/staff/{id}/schedule
PUT    /api/staff/{id}/schedule
```

### Gestão de Serviços
```
GET    /api/services
POST   /api/services
GET    /api/services/{id}
PUT    /api/services/{id}
DELETE /api/services/{id}
```

### Gestão de Clientes
```
GET    /api/clients
POST   /api/clients
GET    /api/clients/{id}
PUT    /api/clients/{id}
DELETE /api/clients/{id}
GET    /api/clients/{id}/appointments
```

### Agendamentos
```
GET    /api/appointments
POST   /api/appointments
GET    /api/appointments/{id}
PUT    /api/appointments/{id}
DELETE /api/appointments/{id}
GET    /api/appointments/available-slots
POST   /api/appointments/{id}/confirm
POST   /api/appointments/{id}/cancel
POST   /api/appointments/{id}/complete
```

### Busca Pública (Clientes)
```
GET  /api/public/barbershops
GET  /api/public/barbershops/{slug}
GET  /api/public/barbershops/{slug}/services
GET  /api/public/barbershops/{slug}/staff
GET  /api/public/barbershops/{slug}/available-slots
POST /api/public/barbershops/{slug}/appointments
```

### Avaliações
```
GET  /api/reviews
POST /api/reviews
GET  /api/reviews/{id}
PUT  /api/reviews/{id}/response
```

## Middleware e Segurança

### Tenant Resolution Middleware
```python
class TenantMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        # Extrair tenant do subdomínio ou header
        host = environ.get('HTTP_HOST', '')
        tenant_slug = self.extract_tenant_slug(host)
        
        # Definir schema do banco
        if tenant_slug:
            environ['TENANT_SLUG'] = tenant_slug
            environ['DB_SCHEMA'] = f'tenant_{tenant_slug}'
        
        return self.app(environ, start_response)
```

### Autenticação JWT
```python
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    tenant_id = current_user.get('tenant_id')
    
    # Verificar se usuário pertence ao tenant
    if not verify_tenant_access(tenant_id):
        return jsonify({'error': 'Unauthorized'}), 403
```

### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: f"{get_tenant_id()}:{request.remote_addr}",
    default_limits=["1000 per hour", "100 per minute"]
)
```

## Configuração de Ambiente

### Docker Compose
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/barbershop_platform
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=barbershop_platform
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    
  celery:
    build: .
    command: celery -A app.celery worker --loglevel=info
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

### Variáveis de Ambiente
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/barbershop_platform
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-password

# File Storage
UPLOAD_FOLDER=/uploads
MAX_CONTENT_LENGTH=16777216

# External APIs
GOOGLE_MAPS_API_KEY=your-maps-key
PAYMENT_GATEWAY_KEY=your-payment-key
```

## Estrutura de Arquivos

```
barbershop-platform/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── appointment.py
│   │   └── service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tenant.py
│   │   ├── appointments.py
│   │   ├── clients.py
│   │   └── public.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── tenant.py
│   │   └── auth.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── email.py
│   │   └── validators.py
│   └── config.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
├── migrations/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Próximos Passos de Implementação

1. **Configurar ambiente base**
   - Setup do PostgreSQL com schemas
   - Configuração do Redis
   - Setup do Flask com extensões

2. **Implementar autenticação**
   - Sistema JWT multi-tenant
   - Middleware de resolução de tenant
   - Controle de acesso baseado em roles

3. **Desenvolver APIs core**
   - CRUD de tenants
   - Gestão de usuários
   - APIs de agendamento

4. **Criar frontend base**
   - Estrutura React com TypeScript
   - Sistema de roteamento
   - Componentes base

5. **Implementar personalização**
   - Sistema de temas
   - Upload de logos
   - Configurações por tenant

6. **Testes e deploy**
   - Testes unitários e integração
   - CI/CD pipeline
   - Deploy em produção


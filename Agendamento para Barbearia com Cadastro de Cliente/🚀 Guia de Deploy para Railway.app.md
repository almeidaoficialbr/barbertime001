# 🚀 Guia de Deploy para Railway.app

Este guia detalha como implantar a plataforma multi-tenant (Backend Flask + Frontend React + PostgreSQL) no Railway.app.

## 📋 **Pré-requisitos**

- Uma conta no [Railway.app](https://railway.app/)
- Uma conta no [GitHub](https://github.com/)
- O código da plataforma multi-tenant no seu repositório GitHub

## 1. **Preparar o Repositório GitHub**

Certifique-se de que seu repositório GitHub contém a estrutura de pastas correta:

```
seu-repositorio/
├── barbershop-platform/          # Backend Flask
├── barbershop-frontend/          # Frontend React
├── docker-compose.yml            # Arquivo Docker Compose
├── .gitignore                    # Ignorar arquivos desnecessários
├── README_PLATAFORMA.md          # Documentação da plataforma
├── DEPLOY.md                     # Guia de deploy geral
└── INICIO_RAPIDO.md              # Guia de início rápido
```

**Importante**: O `docker-compose.yml` que você já possui está configurado para usar o Dockerfile de cada serviço, o que é ideal para o Railway.

## 2. **Criar um Novo Projeto no Railway**

1. Acesse o [Railway Dashboard](https://railway.app/dashboard).
2. Clique em `New Project`.
3. Selecione `Deploy from GitHub Repo`.
4. Conecte sua conta GitHub (se ainda não o fez) e autorize o Railway.
5. Escolha o repositório que contém o código da sua plataforma multi-tenant.

## 3. **Configurar os Serviços (Backend, Frontend, Banco de Dados)**

O Railway irá analisar seu `docker-compose.yml` e sugerir a criação de múltiplos serviços. Confirme a criação dos serviços `backend`, `frontend`, `db` e `redis`.

### 3.1. **Configurar o Banco de Dados (PostgreSQL)**

O Railway irá provisionar automaticamente um banco de dados PostgreSQL. Você precisará obter as credenciais para o backend:

1. No seu projeto Railway, clique no serviço `db` (PostgreSQL).
2. Vá para a aba `Connect`.
3. Copie a `Connection String` (URL do banco de dados).

### 3.2. **Configurar o Backend (Flask)**

1. No seu projeto Railway, clique no serviço `backend`.
2. Vá para a aba `Variables`.
3. Adicione as seguintes variáveis de ambiente:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: Uma chave secreta forte e única (ex: gerada por `os.urandom(24).hex()` no Python)
   - `DATABASE_URL`: Cole a `Connection String` do PostgreSQL que você copiou anteriormente.
   - `UPLOAD_FOLDER`: `/app/uploads` (caminho dentro do container Docker)
   - `MAX_CONTENT_LENGTH`: `5242880` (5MB)
   - `CORS_ORIGINS`: `https://seu-dominio-do-frontend.railway.app,http://localhost:5173` (substitua `seu-dominio-do-frontend.railway.app` pelo domínio gerado pelo Railway para o seu frontend).

4. Vá para a aba `Settings`.
5. Em `Build Command`, certifique-se de que está configurado para usar o Dockerfile (`Dockerfile` no diretório `barbershop-platform`).
6. Em `Start Command`, defina: `python src/main.py`

### 3.3. **Configurar o Frontend (React)**

1. No seu projeto Railway, clique no serviço `frontend`.
2. Vá para a aba `Variables`.
3. Adicione as seguintes variáveis de ambiente:
   - `VITE_API_BASE_URL`: `https://seu-dominio-do-backend.railway.app/api` (substitua `seu-dominio-do-backend.railway.app` pelo domínio gerado pelo Railway para o seu backend).

4. Vá para a aba `Settings`.
5. Em `Build Command`, certifique-se de que está configurado para usar o Dockerfile (`Dockerfile` no diretório `barbershop-frontend`).
6. Em `Start Command`, defina: `nginx -g "daemon off;"` (conforme seu Dockerfile).
7. Em `Domains`, o Railway irá gerar um domínio público para o seu frontend. Anote-o.

### 3.4. **Configurar o Redis**

O serviço `redis` geralmente não precisa de configurações adicionais, a menos que você o utilize diretamente no seu código. O Railway irá provisioná-lo automaticamente.

## 4. **Deploy Inicial**

Após configurar todos os serviços, o Railway iniciará o processo de build e deploy automaticamente. Você pode acompanhar o progresso na aba `Deployments` de cada serviço.

## 5. **Acessar a Aplicação**

Uma vez que todos os serviços estejam `Healthy`:

1. Acesse o domínio público do seu serviço `frontend` (anotado no passo 3.3).
2. O frontend deverá carregar e se comunicar com o backend.

## 6. **Testar a Aplicação**

- Tente acessar a página de login do frontend.
- Use as credenciais de super admin (`admin@barbershop-platform.com` / `admin123`) para verificar se o login funciona.
- Tente registrar uma nova barbearia para verificar o isolamento de dados.

## 7. **Considerações Finais**

- **Domínios Personalizados**: Você pode configurar domínios personalizados para seus serviços de frontend e backend no Railway.
- **Escalabilidade**: O Railway facilita a escalabilidade dos seus serviços conforme a demanda.
- **Monitoramento**: Utilize as ferramentas de log e métricas do Railway para monitorar sua aplicação.

Com este guia, você deve ser capaz de implantar sua plataforma multi-tenant com sucesso no Railway.app!


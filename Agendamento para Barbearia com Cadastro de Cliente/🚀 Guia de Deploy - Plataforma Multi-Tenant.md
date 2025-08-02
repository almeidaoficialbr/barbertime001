# 🚀 Guia de Deploy - Plataforma Multi-Tenant

Este guia contém instruções detalhadas para fazer o deploy da plataforma em diferentes ambientes.

## 📋 **Pré-requisitos**

- Docker e Docker Compose instalados
- Domínio configurado (para produção)
- Certificado SSL (para produção)

## 🔧 **Deploy Local com Docker**

### 1. Clonar o repositório
```bash
git clone <seu-repositorio>
cd plataforma-multi-tenant
```

### 2. Configurar variáveis de ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar variáveis
nano .env
```

### 3. Iniciar com Docker Compose
```bash
# Build e start dos containers
docker-compose up --build -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

### 4. Acessar a aplicação
- Frontend: http://localhost
- Backend API: http://localhost:5000
- Banco de dados: localhost:5432

## 🌐 **Deploy em Produção**

### 1. Servidor (VPS/Cloud)

#### Requisitos mínimos:
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB SSD
- OS: Ubuntu 20.04+

#### Instalação do Docker:
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
```

### 2. Configuração de Produção

#### Variáveis de ambiente (.env):
```env
# Flask
FLASK_ENV=production
SECRET_KEY=sua_chave_super_secreta_aqui_com_32_caracteres
DATABASE_URL=postgresql://barbershop:senha_forte_aqui@db:5432/barbershop_platform

# Upload
UPLOAD_FOLDER=/app/uploads
MAX_CONTENT_LENGTH=5242880

# CORS
CORS_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com

# Database
POSTGRES_DB=barbershop_platform
POSTGRES_USER=barbershop
POSTGRES_PASSWORD=senha_forte_aqui

# SSL (se usando)
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
```

### 3. SSL/HTTPS (Recomendado)

#### Usando Let's Encrypt:
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Copiar certificados para o projeto
sudo cp /etc/letsencrypt/live/seu-dominio.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/seu-dominio.com/privkey.pem ./ssl/key.pem
```

### 4. Deploy
```bash
# Fazer deploy
git pull origin main
docker-compose down
docker-compose up --build -d

# Verificar status
docker-compose ps
docker-compose logs -f
```

## 📊 **Monitoramento**

### Logs
```bash
# Ver logs em tempo real
docker-compose logs -f

# Logs específicos
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Status dos serviços
```bash
# Status geral
docker-compose ps

# Uso de recursos
docker stats

# Espaço em disco
df -h
```

## 🔄 **Backup e Restore**

### Backup do banco de dados
```bash
# Criar backup
docker-compose exec db pg_dump -U barbershop barbershop_platform > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup automático (crontab)
0 2 * * * cd /path/to/project && docker-compose exec db pg_dump -U barbershop barbershop_platform > backups/backup_$(date +\%Y\%m\%d_\%H\%M\%S).sql
```

### Restore do banco de dados
```bash
# Restaurar backup
docker-compose exec -T db psql -U barbershop barbershop_platform < backup_20240101_020000.sql
```

## 🔧 **Manutenção**

### Atualização
```bash
# Atualizar código
git pull origin main

# Rebuild containers
docker-compose down
docker-compose up --build -d
```

### Limpeza
```bash
# Remover containers não utilizados
docker system prune -a

# Remover volumes órfãos
docker volume prune
```

## 🐛 **Troubleshooting**

### Container não inicia
```bash
# Ver logs detalhados
docker-compose logs [service_name]

# Verificar configuração
docker-compose config

# Reiniciar serviço específico
docker-compose restart [service_name]
```

### Problemas de conectividade
```bash
# Testar conectividade entre containers
docker-compose exec backend ping db
docker-compose exec frontend ping backend

# Verificar portas
netstat -tulpn | grep :5000
netstat -tulpn | grep :80
```

### Problemas de permissão
```bash
# Ajustar permissões de upload
sudo chown -R 1000:1000 uploads/
sudo chmod -R 755 uploads/
```

## 📞 **Suporte**

Para problemas de deploy:
1. Verificar logs dos containers
2. Confirmar variáveis de ambiente
3. Testar conectividade de rede
4. Verificar recursos do servidor

---

**Deploy realizado com sucesso!** 🎉


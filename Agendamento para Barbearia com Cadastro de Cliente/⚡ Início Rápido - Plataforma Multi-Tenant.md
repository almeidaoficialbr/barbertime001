# ⚡ Início Rápido - Plataforma Multi-Tenant

Guia para executar a plataforma em **5 minutos**!

## 🚀 **Execução Rápida (Desenvolvimento)**

### 1. Backend (Terminal 1)
```bash
cd barbershop-platform
source venv/bin/activate
python src/main.py
```
✅ Backend rodando em: http://localhost:5000

### 2. Frontend (Terminal 2)
```bash
cd barbershop-frontend
npm install
npm run dev
```
✅ Frontend rodando em: http://localhost:5173

## 🔐 **Login de Teste**

### Super Admin
- **URL**: http://localhost:5173/login
- **Email**: admin@barbershop-platform.com
- **Senha**: admin123

### Barbearia de Teste
- **Email**: joao@barbearia.com
- **Senha**: senha123

## 📱 **Funcionalidades Disponíveis**

✅ **Sistema de Login**
✅ **Dashboard Administrativo**  
✅ **Gestão de Barbearias**
✅ **Sistema Multi-Tenant**
✅ **APIs Completas**
✅ **Personalização por Tenant**

## 🔧 **Comandos Úteis**

### Resetar Banco de Dados
```bash
cd barbershop-platform
rm -f src/database/app.db
python src/main.py
```

### Instalar Dependências
```bash
# Backend
cd barbershop-platform
pip install -r requirements.txt

# Frontend
cd barbershop-frontend
npm install
```

### Verificar Status
```bash
# Verificar se backend está rodando
curl http://localhost:5000/api/public/health

# Verificar se frontend está rodando
curl http://localhost:5173
```

## 🐛 **Problemas Comuns**

### Backend não inicia
```bash
cd barbershop-platform
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

### Frontend não carrega
```bash
cd barbershop-frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Erro de CORS
- Certifique-se que backend está na porta 5000
- Certifique-se que frontend está na porta 5173

---

**Pronto! Sua plataforma está funcionando!** 🎉

Para mais detalhes, consulte o `README_PLATAFORMA.md`


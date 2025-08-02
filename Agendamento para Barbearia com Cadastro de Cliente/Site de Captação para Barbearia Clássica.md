# Site de Captação para Barbearia Clássica

## Descrição do Projeto

Este é um site completo de captação de clientes para barbearia, desenvolvido com Flask (Python) no backend e HTML/CSS/JavaScript no frontend. O sistema permite que clientes se cadastrem e agendem horários de forma intuitiva e moderna.

## Funcionalidades

### 🏠 Página Principal
- Design moderno com tema vintage/clássico
- Seção hero com imagem de impacto
- Apresentação dos serviços com preços
- Seção "Sobre Nós" com informações da barbearia
- Depoimentos de clientes
- Call-to-action para agendamento
- Footer com informações de contato

### 📅 Sistema de Agendamento
- **Etapa 1**: Cadastro de dados pessoais (nome, email, telefone)
- **Etapa 2**: Seleção de data e horário no calendário interativo
- **Etapa 3**: Confirmação dos dados antes do envio
- Validação de formulários em tempo real
- Máscara automática para telefone
- Calendário responsivo com horários disponíveis
- Bloqueio de domingos e datas passadas

### 🔧 Backend (Flask)
- API RESTful para cadastro e agendamento
- Banco de dados SQLite para armazenar clientes e agendamentos
- Validação de dados no servidor
- Sistema de verificação de horários disponíveis
- Logs de confirmação por email (simulado)

## Estrutura do Projeto

```
barbearia-site/
├── app.py                 # Aplicação Flask principal
├── database.db           # Banco de dados SQLite (criado automaticamente)
├── requirements.txt      # Dependências Python
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página principal
│   └── agendamento.html  # Página de agendamento
└── static/              # Arquivos estáticos
    ├── css/
    │   ├── style.css     # CSS principal
    │   └── calendar.css  # CSS do calendário
    ├── js/
    │   ├── main.js       # JavaScript principal
    │   ├── calendar.js   # Funcionalidades do calendário
    │   └── agendamento.js # Sistema de agendamento
    └── images/
        └── hero-bg.jpg   # Imagem de fundo principal
```

## Tecnologias Utilizadas

### Backend
- **Python 3.11**
- **Flask 2.3.3** - Framework web
- **Flask-CORS 4.0.0** - Suporte a CORS
- **SQLite** - Banco de dados

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilização e responsividade
- **JavaScript ES6** - Interatividade
- **Google Fonts** - Tipografia (Oswald + Roboto)
- **Font Awesome** - Ícones

## Como Executar

### 1. Instalar Dependências
```bash
cd barbearia-site
pip3 install -r requirements.txt
```

### 2. Executar o Servidor
```bash
python3 app.py
```

### 3. Acessar o Site
Abra o navegador e acesse: `http://localhost:5000`

## Configuração

### Horários de Funcionamento
- **Segunda a Sexta**: 9h às 19h (intervalos de 30min)
- **Sábado**: 8h às 17h (intervalos de 30min)
- **Domingo**: Fechado

### Banco de Dados
O banco de dados SQLite é criado automaticamente na primeira execução com as seguintes tabelas:

**clientes**
- id (chave primária)
- nome
- email (único)
- telefone
- data_cadastro

**agendamentos**
- id (chave primária)
- cliente_id (chave estrangeira)
- data_agendamento
- horario
- status
- data_criacao

## API Endpoints

### POST /api/agendamento
Cria um novo agendamento
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "telefone": "(11) 98765-4321",
  "data": "2025-07-31",
  "horario": "14:30"
}
```

### GET /api/horarios-disponiveis/{data}
Retorna horários disponíveis para uma data específica

### GET /api/agendamentos
Lista todos os agendamentos (para administração)

## Design e Estilo

### Paleta de Cores
- **Primária**: #1A1A1A (Preto)
- **Secundária**: #B8860B (Dourado/Bronze)
- **Neutras**: #333333, #CCCCCC, #F5F5F5

### Tipografia
- **Títulos**: Oswald (robusta e moderna)
- **Corpo**: Roboto (limpa e legível)

### Características Visuais
- Design moderno com toques vintage
- Responsivo (mobile-first)
- Animações suaves
- Interface intuitiva
- Elementos visuais relacionados à barbearia

## Funcionalidades Futuras

- [ ] Sistema de autenticação para administradores
- [ ] Painel administrativo para gerenciar agendamentos
- [ ] Integração com WhatsApp para notificações
- [ ] Sistema de pagamento online
- [ ] Avaliações e comentários de clientes
- [ ] Galeria de trabalhos realizados
- [ ] Sistema de fidelidade/pontos

## Suporte e Manutenção

Para dúvidas ou suporte técnico, consulte a documentação do Flask ou entre em contato com o desenvolvedor.

---

**Desenvolvido com ❤️ para Barbearia Clássica**


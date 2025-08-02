# Planejamento - Site de Captação para Barbearia

## Funcionalidades Principais

### 1. Sistema de Cadastro
- Formulário com campos obrigatórios:
  - Nome completo
  - Email
  - Número de telefone
- Validação de dados
- Armazenamento das informações

### 2. Sistema de Agendamento
- Calendário interativo para seleção de data
- Seleção de horário disponível
- Confirmação do agendamento
- Envio das informações para o proprietário

### 3. Páginas do Site
- **Página Principal (Home)**
  - Apresentação da barbearia
  - Call-to-action para agendamento
  - Depoimentos/avaliações
  - Galeria de trabalhos

- **Página de Agendamento**
  - Formulário de cadastro
  - Calendário de agendamento
  - Confirmação

- **Página de Contato**
  - Informações da barbearia
  - Localização/mapa
  - Horários de funcionamento

## Conceito Visual

### Estilo
- Moderno e masculino
- Cores escuras (preto, cinza escuro, dourado/bronze)
- Tipografia robusta e elegante
- Elementos vintage/clássicos da barbearia

### Elementos Visuais
- Ícones relacionados à barbearia (navalha, tesoura, pente)
- Imagens de alta qualidade
- Gradientes sutis
- Animações suaves

### Layout
- Design responsivo (mobile-first)
- Navegação intuitiva
- Formulários limpos e organizados
- Calendário visual atrativo

## Tecnologias
- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite (para simplicidade)
- **Funcionalidades**: 
  - Validação de formulários
  - Calendário interativo
  - Sistema de notificações por email

## Fluxo do Usuário
1. Usuário acessa o site
2. Navega pela página principal
3. Clica em "Agendar Horário"
4. Preenche formulário de cadastro
5. Seleciona data no calendário
6. Escolhe horário disponível
7. Confirma agendamento
8. Recebe confirmação
9. Proprietário recebe notificação com os dados



## Especificações Técnicas Detalhadas

### Estrutura de Arquivos
```
barbearia-site/
├── app.py (Flask backend)
├── database.db (SQLite)
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── calendar.js
│   └── images/
│       ├── logo.png
│       ├── hero-bg.jpg
│       └── gallery/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── agendamento.html
│   └── confirmacao.html
└── requirements.txt
```

### Banco de Dados (SQLite)
**Tabela: clientes**
- id (INTEGER PRIMARY KEY)
- nome (TEXT NOT NULL)
- email (TEXT NOT NULL UNIQUE)
- telefone (TEXT NOT NULL)
- data_cadastro (DATETIME DEFAULT CURRENT_TIMESTAMP)

**Tabela: agendamentos**
- id (INTEGER PRIMARY KEY)
- cliente_id (INTEGER FOREIGN KEY)
- data_agendamento (DATE NOT NULL)
- horario (TIME NOT NULL)
- status (TEXT DEFAULT 'agendado')
- data_criacao (DATETIME DEFAULT CURRENT_TIMESTAMP)

### APIs Backend (Flask)
- `POST /api/cadastro` - Cadastrar novo cliente
- `POST /api/agendamento` - Criar novo agendamento
- `GET /api/horarios-disponiveis/<data>` - Buscar horários disponíveis
- `GET /api/agendamentos` - Listar agendamentos (admin)

### Funcionalidades JavaScript
- Validação de formulários em tempo real
- Calendário interativo com datas disponíveis
- Máscaras para telefone e outros campos
- Animações de transição entre etapas
- Feedback visual para ações do usuário

### Responsividade
- Breakpoints: 320px, 768px, 1024px, 1200px
- Mobile-first approach
- Touch-friendly para dispositivos móveis
- Calendário adaptável para telas pequenas

### Horários de Funcionamento
- Segunda a Sexta: 9h às 19h
- Sábado: 8h às 17h
- Domingo: Fechado
- Intervalos de 30 minutos entre agendamentos


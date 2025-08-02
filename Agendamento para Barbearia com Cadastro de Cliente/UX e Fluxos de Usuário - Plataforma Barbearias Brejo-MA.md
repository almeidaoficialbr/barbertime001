# UX e Fluxos de Usuário - Plataforma Barbearias Brejo-MA

## Personas e Jornadas do Usuário

### Persona 1: João - Cliente Final
**Perfil**: 28 anos, trabalha em escritório, gosta de manter o visual sempre em dia
**Necessidades**: Agendar corte rapidamente, encontrar barbearia próxima, horários flexíveis
**Dispositivo**: Principalmente mobile (80% do tempo)

### Persona 2: Carlos - Proprietário de Barbearia
**Perfil**: 35 anos, dono da "Barbearia do Carlos", 8 anos no ramo
**Necessidades**: Gerenciar agendamentos, controlar funcionários, aumentar clientela
**Dispositivo**: Desktop no trabalho, mobile para verificações rápidas

### Persona 3: Ana - Funcionária/Barbeira
**Perfil**: 26 anos, trabalha na barbearia há 3 anos, especialista em cortes femininos
**Necessidades**: Ver agenda do dia, confirmar agendamentos, atualizar status
**Dispositivo**: Tablet na barbearia, mobile pessoal

## Fluxos de Navegação

### Fluxo 1: Cliente Buscando Barbearia

#### Jornada Completa
```
1. Acesso Inicial
   ├── Cliente acessa app/site
   ├── Localização detectada automaticamente (Brejo-MA)
   └── Tela inicial com barbearias próximas

2. Busca e Filtros
   ├── Lista de barbearias com:
   │   ├── Foto de capa
   │   ├── Nome e avaliação
   │   ├── Distância
   │   ├── Status (aberto/fechado)
   │   └── Próximo horário disponível
   ├── Filtros disponíveis:
   │   ├── Distância
   │   ├── Avaliação
   │   ├── Preço
   │   ├── Especialidades
   │   └── Disponibilidade hoje

3. Seleção da Barbearia
   ├── Tela da barbearia com:
   │   ├── Galeria de fotos
   │   ├── Informações (endereço, telefone, horários)
   │   ├── Lista de serviços e preços
   │   ├── Equipe (fotos e especialidades)
   │   ├── Avaliações de clientes
   │   └── Botão "Agendar Horário"

4. Processo de Agendamento
   ├── Seleção do serviço
   ├── Escolha do profissional (opcional)
   ├── Calendário com datas disponíveis
   ├── Horários disponíveis para a data
   ├── Formulário de dados pessoais
   ├── Confirmação do agendamento
   └── Tela de sucesso com detalhes

5. Pós-Agendamento
   ├── Email/SMS de confirmação
   ├── Lembrete 24h antes
   ├── Lembrete 2h antes
   └── Solicitação de avaliação após o serviço
```

#### Wireframes Mobile - Cliente

**Tela 1: Home/Busca**
```
┌─────────────────────┐
│ 🔍 Buscar barbearia │
│ 📍 Brejo-MA         │
├─────────────────────┤
│ 🏪 Barbearia do João│
│ ⭐⭐⭐⭐⭐ (4.8)     │
│ 📍 500m • Aberto    │
│ 🕐 Próximo: 14:30   │
├─────────────────────┤
│ 🏪 Corte & Estilo   │
│ ⭐⭐⭐⭐ (4.5)       │
│ 📍 800m • Fechado   │
│ 🕐 Abre às 08:00    │
├─────────────────────┤
│ [Ver mais...]       │
└─────────────────────┘
```

**Tela 2: Detalhes da Barbearia**
```
┌─────────────────────┐
│ [Foto da barbearia] │
│ Barbearia do João   │
│ ⭐⭐⭐⭐⭐ (4.8) 127 av│
├─────────────────────┤
│ 📍 Rua A, 123       │
│ 📞 (99) 99999-9999  │
│ 🕐 Seg-Sex: 8h-18h  │
├─────────────────────┤
│ SERVIÇOS            │
│ ✂️ Corte R$ 25      │
│ 🧔 Barba R$ 15      │
│ 💇 Combo R$ 35      │
├─────────────────────┤
│ [AGENDAR HORÁRIO]   │
└─────────────────────┘
```

**Tela 3: Agendamento**
```
┌─────────────────────┐
│ Escolha o serviço   │
│ ○ Corte (R$ 25)     │
│ ○ Barba (R$ 15)     │
│ ● Combo (R$ 35)     │
├─────────────────────┤
│ Profissional        │
│ ● Qualquer um       │
│ ○ João (especialista│
│ ○ Pedro (iniciante) │
├─────────────────────┤
│ [CONTINUAR]         │
└─────────────────────┘
```

### Fluxo 2: Proprietário Gerenciando Barbearia

#### Dashboard Principal
```
1. Login e Acesso
   ├── Tela de login com email/senha
   ├── Verificação de tenant
   └── Redirecionamento para dashboard

2. Dashboard Overview
   ├── Métricas do dia:
   │   ├── Agendamentos hoje
   │   ├── Receita prevista
   │   ├── Taxa de ocupação
   │   └── Novos clientes
   ├── Próximos agendamentos
   ├── Alertas e notificações
   └── Ações rápidas

3. Gestão de Agendamentos
   ├── Calendário mensal/semanal/diário
   ├── Lista de agendamentos
   ├── Filtros por status/profissional
   ├── Ações: confirmar/cancelar/reagendar
   └── Adicionar agendamento manual

4. Gestão de Clientes
   ├── Lista de clientes
   ├── Busca e filtros
   ├── Histórico de agendamentos
   ├── Adicionar/editar cliente
   └── Notas e preferências

5. Configurações
   ├── Dados da barbearia
   ├── Personalização visual
   ├── Serviços e preços
   ├── Horários de funcionamento
   ├── Equipe e permissões
   └── Integrações
```

#### Wireframes Desktop - Proprietário

**Dashboard Principal**
```
┌─────────────────────────────────────────────────────────┐
│ Logo Barbearia    [Notificações] [Perfil] [Sair]       │
├─────────────────────────────────────────────────────────┤
│ Dashboard │ Agenda │ Clientes │ Serviços │ Relatórios   │
├─────────────────────────────────────────────────────────┤
│ HOJE                    │ PRÓXIMOS AGENDAMENTOS          │
│ 📅 12 agendamentos      │ 14:00 - João Silva - Corte     │
│ 💰 R$ 420 receita       │ 14:30 - Pedro Santos - Barba   │
│ 👥 3 novos clientes     │ 15:00 - Carlos Lima - Combo    │
│ 📊 85% ocupação         │ 15:30 - Ana Costa - Corte      │
├─────────────────────────┼─────────────────────────────────┤
│ GRÁFICO SEMANAL         │ AÇÕES RÁPIDAS                  │
│ [Gráfico de receita]    │ [+ Novo Agendamento]            │
│                         │ [+ Novo Cliente]                │
│                         │ [📊 Relatório do Mês]          │
└─────────────────────────┴─────────────────────────────────┘
```

### Fluxo 3: Funcionário Usando o Sistema

#### Interface Simplificada
```
1. Login Funcionário
   ├── Acesso com credenciais específicas
   ├── Permissões limitadas
   └── Interface simplificada

2. Agenda do Dia
   ├── Lista dos seus agendamentos
   ├── Horários livres
   ├── Status de cada agendamento
   └── Ações básicas

3. Atendimento
   ├── Marcar cliente como "chegou"
   ├── Iniciar atendimento
   ├── Finalizar serviço
   ├── Adicionar observações
   └── Próximo cliente

4. Perfil
   ├── Seus dados
   ├── Especialidades
   ├── Horários de trabalho
   └── Estatísticas pessoais
```

## Experiência do Usuário (UX)

### Princípios de Design

#### 1. Mobile-First
- 70% dos acessos serão mobile
- Interface touch-friendly
- Navegação por gestos
- Carregamento rápido

#### 2. Simplicidade
- Máximo 3 cliques para agendar
- Informações essenciais visíveis
- Fluxo linear e intuitivo
- Feedback visual constante

#### 3. Personalização
- Cores da barbearia
- Logo personalizado
- Mensagens customizadas
- Experiência branded

#### 4. Acessibilidade
- Contraste adequado
- Textos legíveis
- Navegação por teclado
- Suporte a leitores de tela

### Estados da Interface

#### Loading States
```
- Skeleton screens durante carregamento
- Indicadores de progresso
- Mensagens de status
- Fallbacks para erros de conexão
```

#### Empty States
```
- Primeira vez usando o app
- Nenhum agendamento encontrado
- Barbearia sem horários disponíveis
- Lista de clientes vazia
```

#### Error States
```
- Erro de conexão
- Agendamento não disponível
- Dados inválidos
- Permissão negada
```

### Micro-interações

#### Feedback Visual
```
- Botões com hover/press states
- Animações de transição suaves
- Confirmações visuais
- Progress indicators
```

#### Notificações
```
- Toast messages para ações
- Badges para notificações
- Alertas para confirmações
- Status indicators
```

## Responsividade

### Breakpoints
```css
/* Mobile First */
.container {
  width: 100%;
  padding: 16px;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }
  
  .sidebar {
    display: block;
  }
}

/* Large Desktop */
@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
  }
}
```

### Adaptações por Dispositivo

#### Mobile (< 768px)
- Menu hambúrguer
- Cards em coluna única
- Botões grandes (44px mínimo)
- Navegação bottom tab

#### Tablet (768px - 1024px)
- Grid de 2 colunas
- Sidebar colapsável
- Navegação híbrida
- Modais em overlay

#### Desktop (> 1024px)
- Layout de 3 colunas
- Sidebar fixa
- Navegação top bar
- Modais centralizados

## Testes de Usabilidade

### Cenários de Teste

#### Teste 1: Primeiro Agendamento
```
Objetivo: Cliente consegue agendar pela primeira vez
Passos:
1. Abrir app
2. Encontrar barbearia
3. Escolher serviço
4. Agendar horário
5. Confirmar dados

Métricas:
- Tempo para completar
- Taxa de abandono
- Pontos de confusão
- Satisfação (1-10)
```

#### Teste 2: Gestão de Agenda
```
Objetivo: Proprietário gerencia agendamentos
Passos:
1. Login no painel
2. Visualizar agenda do dia
3. Confirmar agendamento
4. Cancelar agendamento
5. Adicionar novo agendamento

Métricas:
- Eficiência das tarefas
- Erros cometidos
- Facilidade de uso
- Funcionalidades mais usadas
```

### Métricas de Sucesso

#### Conversão
- Taxa de agendamento completado: > 80%
- Abandono no funil: < 20%
- Retorno de clientes: > 60%

#### Performance
- Tempo de carregamento: < 3s
- Time to interactive: < 5s
- First contentful paint: < 2s

#### Satisfação
- NPS (Net Promoter Score): > 50
- Rating na app store: > 4.5
- Suporte tickets: < 5% dos usuários

## Próximas Etapas de UX

1. **Prototipagem**
   - Wireframes detalhados
   - Protótipo interativo
   - Testes com usuários

2. **Design System**
   - Componentes reutilizáveis
   - Guia de estilo
   - Tokens de design

3. **Implementação**
   - Frontend responsivo
   - Testes de usabilidade
   - Iterações baseadas em feedback

4. **Otimização**
   - A/B tests
   - Analytics de uso
   - Melhorias contínuas


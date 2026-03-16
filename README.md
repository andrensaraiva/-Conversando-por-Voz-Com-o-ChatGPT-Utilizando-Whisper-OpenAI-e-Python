<div align="center">

```
██╗   ██╗ ██████╗ ██╗  ██╗███╗   ██╗██████╗  ██████╗
██║   ██║██╔═══██╗╚██╗██╔╝████╗  ██║██╔══██╗██╔════╝
██║   ██║██║   ██║ ╚███╔╝ ██╔██╗ ██║██████╔╝██║     
╚██╗ ██╔╝██║   ██║ ██╔██╗ ██║╚██╗██║██╔═══╝ ██║     
 ╚████╔╝ ╚██████╔╝██╔╝ ██╗██║ ╚████║██║     ╚██████╗
  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝
```

### **Protótipo de NPC Inteligente por Voz com IA**

> *"E se você pudesse conversar por voz com um personagem de jogo alimentado por inteligência artificial?"*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-ChatGPT-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Whisper](https://img.shields.io/badge/Whisper-Speech--to--Text-FF6F00?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![gTTS](https://img.shields.io/badge/gTTS-Text--to--Speech-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://gtts.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Converse por voz com NPCs que têm personalidade, história e missões.**
**Whisper · ChatGPT · gTTS · Game Design · Python**

[Conceito](#-conceito) · [Como Funciona](#-como-funciona) · [Executar](#-como-executar) · [Personas](#-personas-disponíveis) · [Game Design](#-game-design--por-que-isso-importa)

</div>

---

## 📖 Sobre o Projeto

**VoxNPC** não é apenas mais um chatbot por voz. É um **protótipo de NPC inteligente** que transforma a interação com IA generativa em uma **experiência interativa inspirada em jogos**.

Em vez de simplesmente perguntar algo e receber uma resposta genérica, você **conversa com personagens que têm personalidade, história de fundo, estilo de fala próprio e até missões para completar**. Cada interação gera pontos de experiência, cada NPC tem uma voz narrativa distinta, e a conversa se desenrola como um diálogo de videogame — não como uma pesquisa no Google.

### O que torna esse projeto diferente?

| Projeto Convencional | VoxNPC |
|---|---|
| Assistente genérico | NPCs com personalidade e backstory |
| Pergunta → Resposta | Diálogo narrativo com progressão |
| Interface sem identidade | Experiência temática imersiva |
| Apenas técnico | Técnico + criativo + game design |
| Sem contexto | Memória de conversa e continuidade |

---

## 💡 Conceito

### A Ideia Central

VoxNPC reimagina o conceito de **assistente por voz** através das lentes do **game design**. O usuário não fala com uma IA — fala com um **personagem**. Cada persona é um NPC com:

- **Nome e identidade** — não é "assistente", é *Eldrin, o Sábio* ou *NEON-7*
- **Personalidade definida** — cada persona responde com estilo próprio
- **Contexto narrativo** — backstory, tema, universo
- **Missões** — objetivos que gamificam a interação
- **Progressão** — XP, níveis e conquistas por conversar

### Conexão IA + Voz + Game Design

```
┌─────────────────────────────────────────────────────────────────┐
│                         GAME DESIGN                             │
│  Personas · Missões · XP · Níveis · Narrativa · Imersão        │
├─────────────────────────────────────────────────────────────────┤
│     VOICE                    AI ENGINE                          │
│  ┌──────────┐            ┌──────────────┐                       │
│  │ Whisper  │ ──texto──▶ │   ChatGPT    │                       │
│  │  (STT)   │            │ + Persona    │                       │
│  └──────────┘            │ + Contexto   │                       │
│       ▲                  └──────┬───────┘                       │
│       │                         │                               │
│    🎙️ voz                   resposta                            │
│       │                         │                               │
│   [Usuário] ◀──── 🔊 ────── [gTTS]                             │
│                              (TTS)                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Objetivos

- **Técnico**: Integrar Whisper (STT) + ChatGPT (IA) + gTTS (TTS) em um pipeline de voz funcional
- **Criativo**: Transformar um assistente genérico em uma experiência com identidade e imersão
- **Game Design**: Aplicar mecânicas de jogos (personas, XP, missões, narrativa) de forma leve e elegante
- **Portfólio**: Criar um projeto que demonstre criatividade, integração de APIs e pensamento de produto

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função | Detalhe |
|---|---|---|
| **Python 3.10+** | Linguagem base | Toda a aplicação |
| **OpenAI Whisper** | Speech-to-Text | Transcreve a fala do usuário em texto |
| **OpenAI ChatGPT** | IA Generativa | Gera respostas com personalidade de NPC |
| **gTTS** | Text-to-Speech | Converte as respostas em áudio falado |
| **Rich** | Interface no terminal | Painéis, tabelas e formatação visual |
| **Click** | CLI | Argumentos de linha de comando |
| **SoundDevice** | Captura de áudio | Gravação pelo microfone |
| **python-dotenv** | Configuração | Variáveis de ambiente seguras |

---

## 🏗️ Arquitetura da Solução

O projeto segue uma **arquitetura modular** onde cada responsabilidade está isolada em seu próprio módulo:

```
┌────────────────────────────────────────────────────────────┐
│                        main.py                             │
│                   (Ponto de Entrada)                       │
├────────────────────────────────────────────────────────────┤
│                  DialogueSystem                            │
│            (Orquestrador Central)                          │
├──────────┬──────────┬────────────┬────────────┬───────────┤
│  STT     │  TTS     │  AI Engine │ NPC Manager│   Game    │
│ Whisper  │  gTTS    │  ChatGPT   │  Personas  │ Mechanics │
├──────────┴──────────┴────────────┴────────────┴───────────┤
│                      config.py                             │
│                  (Configuração Central)                    │
└────────────────────────────────────────────────────────────┘
```

### Módulos

| Módulo | Arquivo | Responsabilidade |
|---|---|---|
| **Speech-to-Text** | `src/speech_to_text.py` | Gravação de áudio + transcrição via Whisper |
| **Text-to-Speech** | `src/text_to_speech.py` | Síntese de voz + reprodução via gTTS |
| **AI Engine** | `src/ai_engine.py` | Comunicação com ChatGPT + memória de conversa |
| **NPC Manager** | `src/npc_manager.py` | Carregamento de personas + construção de prompts |
| **Game Mechanics** | `src/game_mechanics.py` | XP, níveis, missões e progressão |
| **Dialogue System** | `src/dialogue_system.py` | Orquestra todo o fluxo de diálogo |
| **Config** | `config.py` | Configurações, caminhos e constantes |

---

## 🔄 Fluxo de Funcionamento

```
                    ╔═══════════════════╗
                    ║   INÍCIO SESSÃO   ║
                    ╚════════╤══════════╝
                             │
                    ┌────────▼────────┐
                    │ Escolher Persona │
                    │  (NPC Manager)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Saudação NPC   │◀──── Áudio (gTTS)
                    │  + Briefing     │
                    └────────┬────────┘
                             │
              ┌──────────────▼──────────────┐
              │     LOOP DE DIÁLOGO         │
              │                             │
              │  ┌───────────────────────┐  │
              │  │ 🎙️ Usuário fala       │  │
              │  │ (SoundDevice grava)   │  │
              │  └──────────┬────────────┘  │
              │             │               │
              │  ┌──────────▼────────────┐  │
              │  │ 📝 Whisper transcreve │  │
              │  └──────────┬────────────┘  │
              │             │               │
              │  ┌──────────▼────────────┐  │
              │  │ 🧠 ChatGPT responde   │  │
              │  │ (com persona ativa)   │  │
              │  └──────────┬────────────┘  │
              │             │               │
              │  ┌──────────▼────────────┐  │
              │  │ 🔊 gTTS sintetiza     │  │
              │  │ e reproduz resposta   │  │
              │  └──────────┬────────────┘  │
              │             │               │
              │  ┌──────────▼────────────┐  │
              │  │ 🎮 Game Mechanics     │  │
              │  │ +XP, check missões    │  │
              │  └──────────┬────────────┘  │
              │             │               │
              │         [Continua?]         │
              │          Sim ↩ / Não ↓      │
              └──────────────┬──────────────┘
                             │
                    ┌────────▼────────┐
                    │ 📊 Status Final │
                    │ XP · Nível · ⏱️  │
                    └────────┬────────┘
                             │
                    ╔════════▼══════════╗
                    ║   FIM DA SESSÃO   ║
                    ╚═══════════════════╝
```

**Passo a passo:**

1. O usuário escolhe uma **persona** (NPC) para conversar
2. O NPC se apresenta com sua **saudação** (texto + áudio)
3. O usuário **fala** pelo microfone
4. O **Whisper** transcreve a fala em texto
5. O texto é enviado ao **ChatGPT** com o prompt de personalidade do NPC
6. A resposta é exibida e **convertida em áudio** pelo gTTS
7. O sistema registra a interação: **+XP, verificação de missões, progressão**
8. O ciclo se repete até o usuário encerrar
9. Ao sair, o **painel de status final** é exibido

---

## 🎭 Personas Disponíveis

### 🧙 Eldrin, o Sábio
> *Guardião do Conhecimento Ancestral*

- **Tema**: Fantasia Medieval
- **Estilo**: Poético, contemplativo, cheio de metáforas
- **Trata o usuário como**: "Jovem aventureiro"
- **Ideal para**: Perguntas reflexivas, conselhos, histórias

### 🤖 NEON-7
> *Hacker Informante das Sombras Digitais*

- **Tema**: Cyberpunk / Sci-Fi
- **Estilo**: Direto, irreverente, gírias tech
- **Trata o usuário como**: "Novato"
- **Ideal para**: Perguntas técnicas, tecnologia, futuro

### 👑 Lady Isolde
> *Narradora Real da Corte de Avalon*

- **Tema**: Medieval / Fantasia Arturiana
- **Estilo**: Elegante, teatral, narrativa épica
- **Trata o usuário como**: "Nobre viajante"
- **Ideal para**: Histórias, narrativas colaborativas, aventuras

---

## 🎮 Game Design — Por que isso importa

### Mecânicas Incorporadas

| Mecânica | Implementação | Efeito na Experiência |
|---|---|---|
| **Personas/NPCs** | Arquivos JSON com personalidade, backstory e regras | Cada conversa tem identidade e imersão |
| **Sistema de XP** | Pontos por interação, bônus por engajamento | Incentiva conversas mais longas e profundas |
| **Progressão/Níveis** | 5 níveis: Aprendiz → Mestre das Vozes | Senso de conquista e evolução |
| **Missões** | Objetivos específicos por persona | Direcionamento e propósito na conversa |
| **Narrativa Contextual** | Backstory e universo de cada persona | Mundo coerente e envolvente |
| **Estilo de Fala** | Cada NPC fala de forma única e consistente | Personalidade tangível e memorável |
| **Feedback Visual** | Painéis, barras de progresso, notificações | Resposta imediata e satisfação |

### Por que Game Design + IA é poderoso?

1. **Engajamento**: Personas com personalidade retêm o usuário por mais tempo que um chatbot genérico
2. **Memorabilidade**: Conversar com "Eldrin, o Sábio" é mais memorável que conversar com "Assistente"
3. **Direção**: Missões dão ao usuário algo para fazer, não apenas algo para perguntar
4. **Imersão**: Contexto narrativo transforma uma demo técnica em uma experiência
5. **Diferenciação**: No portfólio, demonstra pensamento de **design de produto**, não apenas código

### Como isso agrega ao portfólio

- Mostra que você pensa além do código — em **experiência do usuário**
- Demonstra capacidade de integrar conceitos de **diferentes disciplinas** (IA, áudio, game design)
- Evidencia uso criativo de tecnologia, não apenas replicação de tutoriais
- Recrutadores lembram de projetos com **identidade e proposta**, não de mais um CRUD

---

## 📁 Estrutura de Pastas

```
VoxNPC/
│
├── 📄 main.py                      # Ponto de entrada da aplicação
├── ⚙️ config.py                     # Configuração central do projeto
├── 📋 requirements.txt             # Dependências Python
├── 🔒 .env.example                 # Template de variáveis de ambiente
├── 🚫 .gitignore                   # Arquivos ignorados pelo Git
├── 📖 README.md                    # Este documento
│
├── 📂 src/                         # Código-fonte principal
│   ├── __init__.py
│   ├── speech_to_text.py           # 🎙️ Whisper — transcrição de áudio
│   ├── text_to_speech.py           # 🔊 gTTS — síntese de voz
│   ├── ai_engine.py                # 🧠 ChatGPT — motor de IA
│   ├── npc_manager.py              # 🎭 Gerenciador de personas/NPCs
│   ├── dialogue_system.py          # 💬 Sistema de diálogo interativo
│   └── game_mechanics.py           # 🎮 Mecânicas de gamificação
│
├── 📂 personas/                    # Definições de NPCs (JSON)
│   ├── sage.json                   # 🧙 Eldrin, o Sábio
│   ├── cyberpunk_guide.json        # 🤖 NEON-7
│   └── medieval_narrator.json      # 👑 Lady Isolde
│
├── 📂 assets/
│   └── audio/                      # 🔊 Arquivos de áudio gerados
│
└── 📂 docs/                        # 📚 Documentação complementar
    ├── CONCEPT.md                  # Conceito criativo detalhado
    ├── GAME_DESIGN.md              # Análise de game design
    └── PORTFOLIO_GUIDE.md          # Guia de apresentação em portfólio
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- Conta na [OpenAI](https://platform.openai.com/) com API Key ativa
- Microfone funcional (para modo voz)
- FFmpeg instalado (necessário para Whisper)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/VoxNPC.git
cd VoxNPC

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env e adicione sua OPENAI_API_KEY
```

### Instalação do FFmpeg (necessário para Whisper)

```bash
# Windows (com Chocolatey)
choco install ffmpeg

# Windows (com Scoop)
scoop install ffmpeg

# Linux (Debian/Ubuntu)
sudo apt install ffmpeg

# Mac
brew install ffmpeg
```

### Execução

```bash
# Modo padrão — voz + persona Eldrin (sage)
python main.py

# Escolher persona específica
python main.py --persona cyberpunk
python main.py --persona medieval

# Modo texto (sem microfone — ideal para testar)
python main.py --mode texto

# Modo híbrido (escolhe voz ou texto a cada turno)
python main.py --mode ambos

# Listar todas as personas disponíveis
python main.py --list-personas

# Modo debug (informações extras no console)
python main.py --debug
```

---

## 🧪 Como Testar

### Teste Rápido (modo texto, sem microfone)

A forma mais fácil de testar é usando o **modo texto**, que não exige microfone nem dependências de áudio pesadas:

```bash
# 1. Instale apenas as dependências leves
pip install openai gtts pygame python-dotenv rich click

# 2. Configure sua chave da OpenAI
cp .env.example .env
# Abra o .env e preencha: OPENAI_API_KEY=sk-sua-chave-aqui

# 3. Execute em modo texto
python main.py --mode texto
```

### Testando cada Persona

```bash
# 🧙 Eldrin, o Sábio (Fantasia Medieval)
python main.py --mode texto --persona sage

# 🤖 NEON-7 (Cyberpunk / Sci-Fi)
python main.py --mode texto --persona cyberpunk

# 👑 Lady Isolde (Medieval / Fantasia Arturiana)
python main.py --mode texto --persona medieval
```

### Comandos durante a conversa

Uma vez dentro da conversa, você pode digitar:

| Comando | Ação |
|---|---|
| `status` | 📊 Mostra XP, nível e estatísticas da sessão |
| `missões` | 📜 Lista as missões disponíveis da persona |
| `persona` | 🎭 Troca a persona do NPC no meio da conversa |
| `ajuda` | ❓ Mostra todos os comandos disponíveis |
| `limpar` | 🗑️ Reseta o histórico de conversa |
| `sair` | 👋 Encerra a conversa e mostra o status final |

### Teste com voz (requer setup extra)

Para testar com entrada por voz, instale as dependências de áudio:

```bash
# Instale FFmpeg (necessário para Whisper)
# Windows: choco install ffmpeg  ou  scoop install ffmpeg
# Linux:   sudo apt install ffmpeg
# Mac:     brew install ffmpeg

# Instale as dependências de áudio
pip install numpy sounddevice soundfile openai-whisper

# Execute com voz
python main.py

# Ou modo híbrido (escolhe voz ou texto a cada turno)
python main.py --mode ambos
```

### Testes Unitários

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## 💬 Exemplos de Uso

### Exemplo 1: Conversa com Eldrin, o Sábio 🧙

```
🎙️ Você: "Me dê um conselho sobre estudar programação"

🧙 Eldrin: "Ah, jovem aventureiro... Estudar a arte da programação é como
plantar uma árvore milenar. Nos primeiros dias, parecerá que nada acontece
— mas as raízes estão crescendo. Cada linha de código que você escreve é
uma semente lançada ao solo fértil do conhecimento. As antigas escrituras
dizem: 'A paciência é a mãe de todas as habilidades'. Não busque dominar
tudo de uma vez. Deixe que cada conceito floresça em seu tempo, e um dia
olhará para trás e verá a floresta que construiu."

✨ +10 XP (interação)
```

### Exemplo 2: Conversa com NEON-7 🤖

```
🎙️ Você: "O que é inteligência artificial?"

🤖 NEON-7: "Tá, novato, cola aqui. IA é basicamente quando você ensina
uma máquina a pensar — ou pelo menos a fingir muito bem que pensa. A gente
pega terabytes de dados, enfia num modelo neural e deixa ele encontrar
padrões que nenhum humano conseguiria. Na prática? É o que faz seu feed
saber o que você quer ver, é o que me mantém vivo na rede, e é o que vai
redefinir cada trabalho que existe. A questão não é se a IA vai mudar o
mundo, novato — é se você vai estar do lado certo quando isso acontecer."

✨ +15 XP (interação detalhada)
⬆️ LEVEL UP! 🗺️ Você alcançou o nível 2: Explorador!
```

### Exemplo 3: Narrativa com Lady Isolde 👑

```
🎙️ Você: "Me conte uma história de aventura"

👑 Lady Isolde: "Ah, nobre viajante, aproximai-vos e ouvi! Nos tempos em
que as montanhas ainda conversavam com as nuvens, existiu um cavaleiro sem
nome que vagava pelas terras esquecidas de Avalon. Seu escudo não trazia
brasão, sua espada não tinha fama — mas seu coração carregava algo que
nenhuma armadura poderia conter: a coragem de quem nada tem a perder. Um
dia, às portas de uma floresta que ninguém ousava cruzar, ele ouviu uma
voz... Desejais saber o que a voz disse, viajante?"

✨ +10 XP (interação)
🏆 Missão concluída: 📖 Ouvinte de Lendas (+30 XP)
```

---

## 📊 Sistema de Progressão

| Nível | Título | XP Mínimo | Emoji |
|---|---|---|---|
| 1 | Aprendiz | 0 | 🌱 |
| 2 | Explorador | 50 | 🗺️ |
| 3 | Aventureiro | 120 | ⚔️ |
| 4 | Veterano | 250 | 🛡️ |
| 5 | Mestre das Vozes | 500 | 👑 |

---

## 🔧 Funcionalidades

### ✅ Implementadas

- [x] Pipeline completo de voz: falar → transcrever → IA → responder → ouvir
- [x] Sistema de personas com personalidade, backstory e estilo de fala
- [x] 3 personas temáticas (Fantasia, Cyberpunk, Medieval)
- [x] Sistema de XP e progressão com 5 níveis
- [x] Sistema de missões por persona
- [x] Memória de conversa (contexto mantido entre turnos)
- [x] Modo texto, voz e híbrido
- [x] Interface rica no terminal com Rich
- [x] CLI com Click (argumentos de linha de comando)
- [x] Configuração via variáveis de ambiente (.env)
- [x] Feedback visual: painéis, notificações de level up, barra de XP

### 🔮 Funcionalidades Futuras

#### 🟢 Fáceis

- [ ] Mais personas (Pirata, Detetive Noir, Professor Zen, Alien)
- [ ] Salvar áudio de entrada e saída com timestamp
- [ ] Histórico de conversas salvo em arquivo JSON
- [ ] Escolha de idioma para TTS (inglês, espanhol, etc.)
- [ ] Comando de voz para trocar persona durante a conversa

#### 🟡 Intermediárias

- [ ] Interface web com Streamlit ou Gradio
- [ ] Múltiplas vozes de TTS por persona (via Azure ou ElevenLabs)
- [ ] Sistema de conquistas/achievements desbloqueáveis
- [ ] Diálogos temáticos com narrativa por etapas (arcos de história)
- [ ] Pontuação por qualidade de interação (análise de sentimento)
- [ ] Modo "Mestre de RPG" com criação de aventura colaborativa

#### 🔴 Avançadas

- [ ] Vozes customizadas com clonagem via Coqui TTS ou ElevenLabs
- [ ] Interface gráfica com avatar animado do NPC
- [ ] Multiplayer: dois NPCs conversando entre si
- [ ] Fine-tuning de modelo para cada persona
- [ ] Integração com banco de dados para persistência entre sessões
- [ ] Deploy como aplicação web com WebSocket para áudio em tempo real

---

## 🎨 Versões do Projeto

### V1 — Versão Simples
> *Para quem quer entregar o desafio funcional*

- **Escopo**: Pipeline básico de voz (Whisper → ChatGPT → gTTS)
- **Complexidade**: Baixa
- **Impacto Visual**: Básico (terminal simples)
- **Dificuldade**: ⭐⭐
- **Tempo estimado**: 2-4 horas

### V2 — Versão Portfólio  ← *Este projeto*
> *Para quem quer impressionar no GitHub*

- **Escopo**: Pipeline de voz + personas + game mechanics + documentação
- **Complexidade**: Média
- **Impacto Visual**: Alto (terminal rico, README elaborado, arquitetura clara)
- **Dificuldade**: ⭐⭐⭐
- **Tempo estimado**: 8-16 horas

### V3 — Versão Diferenciada
> *Para quem quer criar algo realmente especial*

- **Escopo**: Tudo da V2 + interface web + vozes customizadas + narrativa ramificada
- **Complexidade**: Alta
- **Impacto Visual**: Muito alto (demo visual, áudio diferenciado, experiência completa)
- **Dificuldade**: ⭐⭐⭐⭐⭐
- **Tempo estimado**: 30+ horas

---

## 🎨 Identidade Visual & Apresentação

### Paleta de Cores Sugerida

| Cor | Hex | Uso |
|---|---|---|
| Ciano Neon | `#00F5FF` | Destaque principal, títulos |
| Roxo Profundo | `#7B2FBE` | Acentos, badges, IA |
| Verde Esmeralda | `#00D26A` | Sucesso, XP, progresso |
| Amarelo Quente | `#FFD93D` | Level up, conquistas |
| Cinza Escuro | `#1E1E2E` | Background, contexto |
| Branco Suave | `#E0E0E0` | Texto principal |

### Como Apresentar no GitHub

- **Banner visual** no topo do README (pode criar no Canva ou Figma)
- **Badges** com tecnologias e status do projeto
- **Diagramas ASCII** para arquitetura (como feito acima)
- **Exemplos de uso** com outputs formatados
- **Screenshots** do terminal rodando (GIF é ainda melhor)
- **Seção de game design** — diferencia de 99% dos projetos de portfólio
- **Documentação complementar** na pasta `docs/`
- **Estilo autoral** — um README que conta uma história, não apenas lista features

### Dicas de Apresentação Autoral

1. Use uma frase de impacto no topo
2. Conte a motivação por trás do projeto, não apenas o que ele faz
3. Mostre exemplos reais de conversas com NPCs
4. Inclua diagramas — recrutadores escaneiam visualmente
5. Tenha uma seção "Por que isso importa" — mostra pensamento crítico

---

## 📝 Aprendizados

Ao desenvolver o VoxNPC, explorei e pratiquei:

- **Integração de APIs** — OpenAI (Whisper + ChatGPT), gTTS
- **Processamento de áudio** — Gravação, transcrição e síntese de voz
- **Prompt Engineering** — Construção de system prompts para controlar personalidade da IA
- **Arquitetura modular em Python** — Separação clara de responsabilidades
- **Design de experiência** — Pensar além do código, na interação do usuário
- **Game Design aplicado** — Uso de mecânicas de jogos fora do contexto de games
- **CLI profissional** — Click, Rich, .env, argumentos de linha de comando
- **Documentação** — README como peça de comunicação, não apenas manual técnico

---

## 🎤 Diferencial para Entrevista

### Como apresentar este projeto em uma entrevista técnica

> "Eu desenvolvi um protótipo de NPC inteligente por voz usando Python. O sistema captura a fala do usuário via microfone, transcreve usando Whisper da OpenAI, envia o texto para o ChatGPT com um prompt de personalidade customizado, recebe a resposta e converte de volta em áudio usando gTTS. Mas o diferencial é que eu apliquei conceitos de game design: cada NPC tem personalidade, backstory e missões — transformando uma demo técnica em uma experiência interativa. Isso me permitiu explorar integração de APIs, processamento de áudio, prompt engineering e design de experiência em um único projeto."

### Pontos-chave para destacar

| Área | O que demonstrar |
|---|---|
| **Integração de APIs** | "Integrei 3 serviços diferentes (Whisper, ChatGPT, gTTS) em um pipeline coeso" |
| **Processamento de Áudio** | "Lidei com gravação, transcrição e síntese de voz em tempo real" |
| **IA Aplicada** | "Usei prompt engineering para criar personas com personalidade consistente" |
| **Design de Experiência** | "Transformei uma automação em uma experiência com identidade e propósito" |
| **Criatividade Técnica** | "Apliquei game design para enriquecer o projeto sem aumentar complexidade desnecessária" |
| **Arquitetura** | "Organizei o projeto com arquitetura modular, cada módulo com responsabilidade única" |

---

## 🏷️ Tags do Projeto

```
python, openai, chatgpt, whisper, speech-to-text, text-to-speech, gtts,
voice-assistant, npc, game-design, interactive, ai, artificial-intelligence,
conversational-ai, prompt-engineering, portfolio, dio, python-project,
voice-interaction, gamification
```

---

## ✍️ Descrições Curtas para o GitHub

1. **🎮 Protótipo de NPC inteligente por voz — Converse com personagens de IA que têm personalidade, missões e progressão. Whisper + ChatGPT + gTTS + Game Design.**

2. **🗣️ Transformando conversas por voz com IA em experiências interativas inspiradas em jogos. NPCs com personalidade, sistema de XP e narrativas temáticas.**

3. **🧙 VoxNPC — Fale com NPCs alimentados por IA. Cada personagem tem história, estilo e missões. Um protótipo que une voz, inteligência artificial e game design.**

4. **🎙️ De assistente por voz a experiência de jogo — Pipeline Python com Whisper, ChatGPT e gTTS, enriquecido com mecânicas de game design e personas narrativas.**

5. **🤖 NPC Inteligente por Voz — Protótipo de personagem virtual conversacional com IA generativa, personalidade dinâmica e gamificação. Python · OpenAI · gTTS.**

---

## 💡 Nomes Criativos Considerados

### Focados em Voz + IA
1. **VoxNPC** ← *escolhido*
2. VoiceForge AI
3. EchoMind
4. SpeakSage
5. VozViva AI

### Focados em Game Design
6. DialogueQuest
7. NPCraft
8. QuestVoice
9. TalkLore
10. VoiceRealm

### Focados em Narrativa
11. NarrAI
12. StoryWhisper
13. EchoSaga
14. LoreSpeaker
15. VoxLore

### Focados em Tecnologia
16. WhisperNPC
17. PromptVox
18. AICompanion
19. NeuralVoice
20. SynthPersona

---

## 📦 Resumo do Conceito

**VoxNPC** é um protótipo de NPC inteligente por voz que transforma a interação com IA generativa em uma experiência interativa inspirada em game design. O sistema captura a fala do usuário, transcreve via Whisper, envia para o ChatGPT com um prompt de personalidade customizado de NPC, e converte a resposta em áudio via gTTS — tudo isso enriquecido com sistema de personas temáticas, missões, XP e progressão. O resultado é um projeto que vai além da automação técnica e entrega uma experiência conversacional com identidade, propósito e imersão.

## 🎯 Pitch (3 linhas)

> Um NPC de jogo que conversa por voz, alimentado por IA.
> Whisper escuta, ChatGPT pensa com personalidade, gTTS responde.
> Não é um chatbot — é uma experiência.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 👤 Autor

Desenvolvido como projeto do desafio **DIO** — *Conversando por Voz com o ChatGPT Utilizando Whisper, OpenAI e Python*.

Transformado em experiência interativa com game design por paixão por tecnologia, jogos e IA.

---

<div align="center">

**⭐ Se este projeto te inspirou, deixe uma estrela!**

*"A melhor forma de aprender IA não é apenas usá-la — é criar experiências com ela."*

</div>
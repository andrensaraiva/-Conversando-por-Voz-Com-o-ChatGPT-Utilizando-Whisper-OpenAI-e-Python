# 🎯 VoxNPC — Guia de Portfólio e Entrevista

## Como Apresentar Este Projeto

Este guia ajuda a destacar o VoxNPC em entrevistas técnicas, portfólio e networking profissional.

---

## Pitch Rápido (30 segundos)

> "Eu criei um protótipo de NPC inteligente por voz. O sistema usa Whisper para capturar a fala do usuário, ChatGPT para gerar respostas com a personalidade de um personagem — como um sábio medieval ou um hacker cyberpunk — e gTTS para responder em áudio. O diferencial é que apliquei game design: cada NPC tem backstory, estilo de fala, missões e um sistema de XP. Transformei uma demo técnica em uma experiência interativa."

---

## Pontos Técnicos para Destacar

### 1. Integração de APIs
- "Integrei três serviços distintos (Whisper, ChatGPT, gTTS) em um pipeline coeso"
- "Gerenciei tokens, rate limits e erro handling na comunicação com a OpenAI"
- "Implementei cache do modelo Whisper para otimizar performance"

### 2. Processamento de Áudio
- "Implementei captura de áudio em tempo real via SoundDevice"
- "Lidei com normalização de áudio, taxa de amostragem e formatos de arquivo"
- "Criei pipeline bidirecional: áudio → texto → IA → texto → áudio"

### 3. Prompt Engineering
- "Construí system prompts que controlam personalidade, estilo de fala e comportamento"
- "Cada persona gera dinamicamente seu prompt baseado em regras JSON"
- "Implementei regras de comportamento que a IA segue consistentemente"

### 4. Arquitetura de Software
- "Organizei o projeto em módulos com responsabilidade única"
- "Usei padrões como composição, cache lazy loading e data classes"
- "Criei uma CLI profissional com Click e interface rica com Rich"

### 5. Design de Experiência
- "Apliquei princípios de game design para transformar a interação"
- "Implementei feedback imediato, progressão e sistema de recompensas"
- "Pensei no projeto como produto, não apenas como exercício técnico"

---

## Perguntas Frequentes em Entrevista

### "Qual foi o maior desafio técnico?"
> "Fazer o pipeline de áudio funcionar de ponta a ponta em tempo real. Gravação, transcrição, envio para IA, síntese e reprodução — cada etapa tem suas nuances. O Whisper, por exemplo, exige FFmpeg e cuidado com formatos de áudio. A integração dos três serviços exigiu tratamento de erros robusto, já que qualquer falha em uma etapa compromete todo o fluxo."

### "Por que game design?"
> "Porque o desafio original é o que todos vão entregar. Game design foi a forma que encontrei de diferenciar o projeto sem aumentar complexidade desnecessária. Adicionar personas e XP é elegante — usa a mesma IA, o mesmo áudio, mas entrega uma experiência completamente diferente."

### "O que você faria diferente?"
> "Usaria um TTS mais avançado, como ElevenLabs ou Azure Neural, para dar vozes distintas a cada persona. Também implementaria uma interface web com Streamlit para tornar o projeto mais acessível para demonstração."

### "Que tecnologias você aprendeu?"
> "Whisper para transcrição, a API da OpenAI para conversação contextual com system prompts, gTTS para síntese de voz, SoundDevice para captura de áudio, Rich para interfaces de terminal, Click para CLI, e princípios de game design aplicados a software."

---

## Como Apresentar no GitHub

### Checklist de Portfólio

- [x] README detalhado com diagramas e exemplos
- [x] Badges visuais de tecnologias
- [x] Estrutura de pastas clara e comentada
- [x] Código limpo com docstrings e type hints
- [x] Documentação complementar na pasta docs/
- [x] Configuração via .env (sem credenciais expostas)
- [x] .gitignore configurado adequadamente
- [ ] GIF do terminal em execução (recomendado)
- [ ] Screenshot do painel de status (recomendado)
- [ ] Vídeo curto de demonstração (diferencial)

### Dica: GIF de Demonstração

Use ferramentas como [asciinema](https://asciinema.org/), [Terminalizer](https://terminalizer.com/) ou simplesmente grave a tela com OBS e converta para GIF. Uma demonstração visual de 30 segundos vale mais que 30 parágrafos de texto.

---

## Habilidades Demonstradas

| Habilidade | Evidência no Projeto |
|---|---|
| Python avançado | Módulos, classes, dataclasses, type hints, CLI |
| Integração de APIs | OpenAI Whisper, ChatGPT, gTTS |
| Processamento de áudio | Gravação, transcrição, síntese, reprodução |
| Prompt engineering | System prompts com personalidade e regras |
| Arquitetura de software | Modular, config centralizada, separation of concerns |
| Design de experiência | Game design aplicado, feedback visual, progressão |
| Documentação | README profissional, docs complementares |
| Versionamento | Git, .gitignore, .env.example |
| Criatividade aplicada | Conceito original, identidade do projeto |

---

## Onde Compartilhar

- **GitHub** — Repositório principal com README elaborado
- **LinkedIn** — Post sobre o conceito criativo do projeto
- **Dev.to / Medium** — Artigo técnico sobre como criar NPCs com IA
- **Twitter/X** — Thread mostrando exemplos de conversas com NPCs
- **Portfólio pessoal** — Seção dedicada com GIF de demonstração
- **DIO** — Entrega do desafio com destaque para o diferencial criativo

---

*"A melhor forma de se destacar não é fazer mais — é fazer diferente."*

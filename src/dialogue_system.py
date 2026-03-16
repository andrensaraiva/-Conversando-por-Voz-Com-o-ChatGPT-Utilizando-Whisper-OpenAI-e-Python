"""
╔══════════════════════════════════════════════════════════════╗
║           VoxNPC — Sistema de Diálogo Interativo             ║
╚══════════════════════════════════════════════════════════════╝

Módulo responsável por:
- Orquestrar o fluxo completo de conversa por voz
- Integrar todos os módulos (STT, TTS, IA, NPC, Game)
- Gerenciar os modos de interação
- Controlar o loop principal de diálogo
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from src.ai_engine import AIEngine
from src.npc_manager import NPCManager
from src.game_mechanics import GameMechanics
from src.speech_to_text import listen
from src.text_to_speech import speak

import config

console = Console()


class DialogueSystem:
    """Sistema central que orquestra toda a experiência VoxNPC."""

    # Comandos especiais que o usuário pode falar
    COMMANDS = {
        "status": "📊 Mostra seu status e progresso",
        "missões": "📜 Lista as missões disponíveis",
        "persona": "🎭 Troca a persona do NPC",
        "limpar": "🗑️  Limpa o histórico de conversa",
        "ajuda": "❓ Mostra os comandos disponíveis",
        "sair": "👋 Encerra a conversa",
    }

    def __init__(self):
        self.npc_manager = NPCManager()
        self.ai_engine = AIEngine()
        self.game = GameMechanics()
        self.running = False
        self.use_voice = True  # Modo voz ativado por padrão

    def setup(self, persona_id: str = None):
        """
        Configura o sistema com a persona escolhida.

        Args:
            persona_id: ID da persona a usar. Se None, usa o padrão.
        """
        persona_id = persona_id or config.DEFAULT_PERSONA

        try:
            persona = self.npc_manager.set_persona(persona_id)
            self.ai_engine.set_system_prompt(persona.build_system_prompt())

            # Carrega missões da persona
            missions = self.npc_manager.get_missions()
            if missions:
                self.game.load_missions(missions)

        except ValueError as e:
            console.print(f"[red]❌ {e}[/red]")
            console.print("[yellow]Usando persona padrão...[/yellow]")

    def _show_welcome(self):
        """Exibe a tela de boas-vindas."""
        welcome_text = (
            "[bold cyan]╔══════════════════════════════════════════════╗[/bold cyan]\n"
            "[bold cyan]║[/bold cyan]     [bold white]VoxNPC — NPC Inteligente por Voz[/bold white]      [bold cyan]║[/bold cyan]\n"
            "[bold cyan]║[/bold cyan]  [dim]Protótipo de Assistente com Personalidade[/dim]  [bold cyan]║[/bold cyan]\n"
            "[bold cyan]╚══════════════════════════════════════════════╝[/bold cyan]\n"
        )
        console.print(welcome_text)

        # Saudação do NPC
        greeting = self.npc_manager.get_greeting()
        persona = self.npc_manager.active_persona

        if persona:
            console.print(
                Panel(
                    f"[italic]{greeting}[/italic]",
                    title=f"{persona.emoji} {persona.name}",
                    border_style="magenta",
                )
            )
        else:
            console.print(f"\n[italic]{greeting}[/italic]\n")

        # Fala a saudação
        if self.use_voice:
            speak(greeting)

    def _show_help(self):
        """Exibe os comandos disponíveis."""
        help_text = "\n".join(
            f"  [bold cyan]{cmd}[/bold cyan] — {desc}"
            for cmd, desc in self.COMMANDS.items()
        )
        console.print(
            Panel(
                help_text,
                title="❓ Comandos Disponíveis",
                subtitle="Fale ou digite um comando",
                border_style="cyan",
            )
        )

    def _handle_command(self, text: str) -> bool:
        """
        Verifica e executa comandos especiais.

        Args:
            text: Texto do usuário.

        Returns:
            True se um comando foi executado.
        """
        text_lower = text.lower().strip()

        if text_lower in ("sair", "tchau", "encerrar", "exit", "quit"):
            farewell = self.npc_manager.active_persona.farewell if self.npc_manager.active_persona else "Até a próxima!"
            console.print(f"\n[italic magenta]{farewell}[/italic magenta]\n")
            if self.use_voice:
                speak(farewell)
            self.game.show_status()
            self.running = False
            return True

        if text_lower in ("status", "meu status", "progresso"):
            self.game.show_status()
            return True

        if text_lower in ("missões", "missoes", "quests", "missão"):
            self.game.show_missions()
            return True

        if text_lower in ("ajuda", "help", "comandos"):
            self._show_help()
            return True

        if text_lower in ("limpar", "resetar", "reset"):
            self.ai_engine.clear_history()
            self.setup(self.npc_manager.active_persona.id if self.npc_manager.active_persona else None)
            console.print("[green]✅ Conversa reiniciada.[/green]")
            return True

        if text_lower in ("persona", "trocar persona", "trocar npc"):
            self._change_persona()
            return True

        return False

    def _change_persona(self):
        """Permite ao usuário trocar a persona ativa."""
        self.npc_manager.list_personas()
        persona_ids = list(self.npc_manager.personas.keys())

        choice = Prompt.ask(
            "\n[cyan]Digite o ID da persona desejada[/cyan]",
            choices=persona_ids,
            default=config.DEFAULT_PERSONA,
        )

        self.ai_engine.clear_history()
        self.setup(choice)

        greeting = self.npc_manager.get_greeting()
        persona = self.npc_manager.active_persona
        console.print(
            Panel(
                f"[italic]{greeting}[/italic]",
                title=f"{persona.emoji} {persona.name}",
                border_style="magenta",
            )
        )
        if self.use_voice:
            speak(greeting)

    def _process_interaction(self, user_text: str):
        """
        Processa uma interação completa: texto -> IA -> resposta -> áudio.

        Args:
            user_text: Texto do usuário (transcrito ou digitado).
        """
        persona = self.npc_manager.active_persona
        persona_emoji = persona.emoji if persona else "🤖"
        persona_name = persona.name if persona else "Assistente"

        # Envia para a IA
        response = self.ai_engine.send_message(user_text)

        # Exibe a resposta
        console.print(
            Panel(
                f"[italic]{response}[/italic]",
                title=f"{persona_emoji} {persona_name}",
                border_style="magenta",
            )
        )

        # Registra interação no sistema de game
        self.game.register_interaction(user_text, response)

        # Converte resposta em áudio
        if self.use_voice:
            speak(response)

    def _select_input_mode(self) -> str:
        """Permite ao usuário escolher o modo de entrada."""
        mode = Prompt.ask(
            "\n[cyan]Modo de entrada[/cyan]",
            choices=["voz", "texto", "ambos"],
            default="voz",
        )
        return mode

    def run(self, persona_id: str = None, input_mode: str = "voz"):
        """
        Inicia o loop principal de diálogo.

        Args:
            persona_id: ID da persona a usar.
            input_mode: Modo de entrada — 'voz', 'texto' ou 'ambos'.
        """
        self.running = True
        self.use_voice = input_mode in ("voz", "ambos")

        # Configuração inicial
        self.setup(persona_id)
        self._show_welcome()
        self._show_help()

        console.print(
            f"\n[dim]Modo de entrada: {'🎙️ Voz' if input_mode == 'voz' else '⌨️ Texto' if input_mode == 'texto' else '🎙️+⌨️ Ambos'}[/dim]"
        )

        # Loop principal de diálogo
        while self.running:
            try:
                console.print("\n" + "─" * 50)

                # Captura entrada do usuário
                if input_mode == "texto":
                    user_text = Prompt.ask("[bold cyan]Você[/bold cyan]")
                elif input_mode == "voz":
                    user_text = listen()
                    console.print(f'[bold cyan]Você disse:[/bold cyan] "{user_text}"')
                else:  # ambos
                    choice = Prompt.ask(
                        "[dim]Falar (v) ou digitar (t)?[/dim]",
                        choices=["v", "t"],
                        default="v",
                    )
                    if choice == "v":
                        user_text = listen()
                        console.print(f'[bold cyan]Você disse:[/bold cyan] "{user_text}"')
                    else:
                        user_text = Prompt.ask("[bold cyan]Você[/bold cyan]")

                # Ignora entradas vazias
                if not user_text or not user_text.strip():
                    console.print("[dim]Não entendi... tente novamente.[/dim]")
                    continue

                # Verifica se é um comando especial
                if self._handle_command(user_text):
                    continue

                # Processa a interação normal
                self._process_interaction(user_text)

            except KeyboardInterrupt:
                console.print("\n\n[yellow]Sessão interrompida pelo usuário.[/yellow]")
                self.game.show_status()
                break
            except Exception as e:
                console.print(f"[red]❌ Erro inesperado: {e}[/red]")
                if config.DEBUG:
                    import traceback
                    traceback.print_exc()
                continue

        console.print("\n[bold]Obrigado por jogar VoxNPC! 🎮[/bold]\n")

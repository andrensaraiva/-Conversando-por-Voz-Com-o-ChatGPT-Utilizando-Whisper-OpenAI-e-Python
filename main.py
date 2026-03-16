"""
╔══════════════════════════════════════════════════════════════╗
║                  VoxNPC — Ponto de Entrada                   ║
║         Protótipo de NPC Inteligente por Voz com IA          ║
╚══════════════════════════════════════════════════════════════╝

E se você pudesse conversar por voz com um personagem de jogo
alimentado por inteligência artificial?

Uso:
    python main.py                          # Modo padrão (voz + persona sage)
    python main.py --persona cyberpunk      # Persona cyberpunk
    python main.py --mode texto             # Modo texto (sem microfone)
    python main.py --mode ambos             # Escolhe voz ou texto a cada turno
    python main.py --list-personas          # Lista personas disponíveis
"""

import click
from rich.console import Console

import config
from src.dialogue_system import DialogueSystem
from src.npc_manager import NPCManager

console = Console()

# Banner ASCII do projeto
BANNER = r"""
[bold cyan]
██╗   ██╗ ██████╗ ██╗  ██╗███╗   ██╗██████╗  ██████╗
██║   ██║██╔═══██╗╚██╗██╔╝████╗  ██║██╔══██╗██╔════╝
██║   ██║██║   ██║ ╚███╔╝ ██╔██╗ ██║██████╔╝██║
╚██╗ ██╔╝██║   ██║ ██╔██╗ ██║╚██╗██║██╔═══╝ ██║
 ╚████╔╝ ╚██████╔╝██╔╝ ██╗██║ ╚████║██║     ╚██████╗
  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝
[/bold cyan]
[dim]Protótipo de NPC Inteligente por Voz com IA[/dim]
[dim]Whisper · ChatGPT · gTTS · Python[/dim]
"""


@click.command()
@click.option(
    "--persona", "-p",
    default=None,
    help="ID da persona do NPC (ex: sage, cyberpunk, medieval)."
)
@click.option(
    "--mode", "-m",
    type=click.Choice(["voz", "texto", "ambos"], case_sensitive=False),
    default="voz",
    help="Modo de entrada: voz, texto ou ambos."
)
@click.option(
    "--list-personas", "-l",
    is_flag=True,
    help="Lista todas as personas disponíveis e sai."
)
@click.option(
    "--debug", "-d",
    is_flag=True,
    help="Ativa o modo de depuração."
)
def main(persona, mode, list_personas, debug):
    """
    VoxNPC — Converse por voz com NPCs inteligentes alimentados por IA.

    Um protótipo que transforma a interação por voz com IA em uma
    experiência inspirada em game design, com personagens, missões
    e progressão.
    """
    # Exibe banner
    console.print(BANNER)

    # Modo debug
    if debug:
        config.DEBUG = True
        console.print("[yellow]🐛 Modo debug ativado.[/yellow]\n")

    # Validação de configuração
    if not config.validate_config():
        console.print(
            "\n[red]❌ Configure suas credenciais no arquivo .env[/red]"
        )
        console.print(
            "[dim]Copie .env.example para .env e preencha a OPENAI_API_KEY[/dim]"
        )
        return

    # Listar personas
    if list_personas:
        manager = NPCManager()
        manager.list_personas()
        return

    # Iniciar sistema de diálogo
    dialogue = DialogueSystem()

    try:
        dialogue.run(persona_id=persona, input_mode=mode.lower())
    except Exception as e:
        console.print(f"\n[red]❌ Erro fatal: {e}[/red]")
        if config.DEBUG:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()

"""
╔══════════════════════════════════════════════════════════════╗
║           VoxNPC — Mecânicas de Game Design                  ║
╚══════════════════════════════════════════════════════════════╝

Módulo responsável por:
- Sistema de pontuação (XP) por interação
- Sistema de missões/desafios falados
- Progressão e níveis do usuário
- Tracking de estatísticas da sessão
"""

import time
from dataclasses import dataclass, field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import config

console = Console()


# ============================================================
# Níveis de Progressão
# ============================================================
LEVELS = [
    {"level": 1, "name": "Aprendiz",        "min_xp": 0,    "emoji": "🌱"},
    {"level": 2, "name": "Explorador",       "min_xp": 50,   "emoji": "🗺️"},
    {"level": 3, "name": "Aventureiro",      "min_xp": 120,  "emoji": "⚔️"},
    {"level": 4, "name": "Veterano",         "min_xp": 250,  "emoji": "🛡️"},
    {"level": 5, "name": "Mestre das Vozes", "min_xp": 500,  "emoji": "👑"},
]


@dataclass
class Mission:
    """Representa uma missão/desafio para o usuário."""
    id: str
    title: str
    description: str
    goal: str
    xp_reward: int = 25
    completed: bool = False
    emoji: str = "📜"


@dataclass
class PlayerStats:
    """Estatísticas do jogador/usuário durante a sessão."""
    xp: int = 0
    level: int = 1
    level_name: str = "Aprendiz"
    interactions: int = 0
    missions_completed: int = 0
    words_spoken: int = 0
    session_start: float = field(default_factory=time.time)
    active_missions: list = field(default_factory=list)
    completed_missions: list = field(default_factory=list)


class GameMechanics:
    """Gerencia as mecânicas de gamificação do VoxNPC."""

    def __init__(self):
        self.stats = PlayerStats()

    def add_xp(self, amount: int, reason: str = ""):
        """
        Adiciona XP ao jogador e verifica level up.

        Args:
            amount: Quantidade de XP a adicionar.
            reason: Motivo do ganho de XP.
        """
        old_level = self.stats.level
        self.stats.xp += amount

        if reason and config.DEBUG:
            console.print(f"[dim]✨ +{amount} XP ({reason})[/dim]")

        # Verifica level up
        new_level = self._calculate_level()
        if new_level > old_level:
            self.stats.level = new_level
            level_info = LEVELS[new_level - 1]
            self.stats.level_name = level_info["name"]
            self._show_level_up(level_info)

    def _calculate_level(self) -> int:
        """Calcula o nível atual baseado no XP."""
        current_level = 1
        for level_data in LEVELS:
            if self.stats.xp >= level_data["min_xp"]:
                current_level = level_data["level"]
        return current_level

    def _show_level_up(self, level_info: dict):
        """Exibe mensagem de level up."""
        console.print(
            Panel(
                f"[bold yellow]⬆️  LEVEL UP![/bold yellow]\n\n"
                f"{level_info['emoji']} Você alcançou o nível {level_info['level']}: "
                f"[bold]{level_info['name']}[/bold]!",
                title="🎮 Progressão",
                border_style="yellow",
            )
        )

    def register_interaction(self, user_text: str, response_text: str):
        """
        Registra uma interação e calcula XP ganho.

        Args:
            user_text: Texto falado pelo usuário.
            response_text: Texto da resposta da IA.
        """
        self.stats.interactions += 1
        self.stats.words_spoken += len(user_text.split())

        # XP base por interação
        xp = config.XP_PER_INTERACTION
        reason = "interação"

        # Bônus por mensagem longa (engajamento)
        if len(user_text.split()) > 15:
            xp += config.XP_BONUS_LONG_RESPONSE
            reason = "interação detalhada"

        self.add_xp(xp, reason)

    def load_missions(self, missions_data: list):
        """
        Carrega missões da persona ativa.

        Args:
            missions_data: Lista de dicionários com dados das missões.
        """
        self.stats.active_missions = []
        for mission_data in missions_data:
            mission = Mission(
                id=mission_data.get("id", "m0"),
                title=mission_data.get("title", "Missão"),
                description=mission_data.get("description", ""),
                goal=mission_data.get("goal", ""),
                xp_reward=mission_data.get("xp_reward", config.MISSION_BONUS_XP),
                emoji=mission_data.get("emoji", "📜"),
            )
            self.stats.active_missions.append(mission)

    def complete_mission(self, mission_id: str) -> bool:
        """
        Marca uma missão como concluída e dá XP de recompensa.

        Args:
            mission_id: ID da missão a completar.

        Returns:
            True se a missão foi encontrada e completada.
        """
        for mission in self.stats.active_missions:
            if mission.id == mission_id and not mission.completed:
                mission.completed = True
                self.stats.missions_completed += 1
                self.stats.completed_missions.append(mission)
                self.add_xp(mission.xp_reward, f"missão: {mission.title}")
                console.print(
                    f"[bold green]🏆 Missão concluída: {mission.emoji} "
                    f"{mission.title} (+{mission.xp_reward} XP)[/bold green]"
                )
                return True
        return False

    def show_status(self):
        """Exibe o painel de status do jogador."""
        level_info = LEVELS[self.stats.level - 1]
        next_level = LEVELS[self.stats.level] if self.stats.level < len(LEVELS) else None

        # Calcula tempo de sessão
        elapsed = time.time() - self.stats.session_start
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        # Progress bar para próximo nível
        if next_level:
            progress = self.stats.xp - level_info["min_xp"]
            needed = next_level["min_xp"] - level_info["min_xp"]
            bar_length = 20
            filled = int(bar_length * progress / needed) if needed > 0 else bar_length
            bar = "█" * filled + "░" * (bar_length - filled)
            xp_text = f"[{bar}] {self.stats.xp}/{next_level['min_xp']} XP"
        else:
            xp_text = f"⭐ {self.stats.xp} XP (Nível Máximo!)"

        status_text = (
            f"{level_info['emoji']} [bold]{level_info['name']}[/bold] "
            f"(Nível {self.stats.level})\n\n"
            f"✨ {xp_text}\n"
            f"💬 Interações: {self.stats.interactions}\n"
            f"📝 Palavras ditas: {self.stats.words_spoken}\n"
            f"🏆 Missões concluídas: {self.stats.missions_completed}\n"
            f"⏱️  Tempo de sessão: {minutes}m {seconds}s"
        )

        console.print(
            Panel(status_text, title="📊 Status do Aventureiro", border_style="cyan")
        )

    def show_missions(self):
        """Exibe as missões disponíveis."""
        if not self.stats.active_missions:
            console.print("[dim]Nenhuma missão disponível para esta persona.[/dim]")
            return

        table = Table(
            title="📜 Missões Disponíveis",
            show_header=True,
            header_style="bold yellow",
        )
        table.add_column("", justify="center", width=3)
        table.add_column("Missão", style="bold")
        table.add_column("Descrição", style="dim")
        table.add_column("XP", justify="right", style="green")
        table.add_column("Status", justify="center")

        for mission in self.stats.active_missions:
            status = "✅" if mission.completed else "⬜"
            table.add_row(
                mission.emoji,
                mission.title,
                mission.description,
                f"+{mission.xp_reward}",
                status,
            )

        console.print(table)

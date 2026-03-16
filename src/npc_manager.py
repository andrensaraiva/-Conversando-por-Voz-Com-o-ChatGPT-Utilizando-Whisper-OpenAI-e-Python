"""
╔══════════════════════════════════════════════════════════════╗
║              VoxNPC — Gerenciador de Personas/NPCs           ║
╚══════════════════════════════════════════════════════════════╝

Módulo responsável por:
- Carregar e gerenciar personas de NPCs a partir de arquivos JSON
- Construir prompts de sistema baseados na personalidade do NPC
- Permitir troca dinâmica de persona durante a conversa
- Listar personas disponíveis
"""

import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

import config

console = Console()


class Persona:
    """Representa a identidade e personalidade de um NPC."""

    def __init__(self, data: dict):
        self.id = data.get("id", "unknown")
        self.name = data.get("name", "NPC Desconhecido")
        self.title = data.get("title", "")
        self.theme = data.get("theme", "general")
        self.greeting = data.get("greeting", "Olá, aventureiro.")
        self.personality = data.get("personality", "")
        self.speech_style = data.get("speech_style", "")
        self.backstory = data.get("backstory", "")
        self.rules = data.get("rules", [])
        self.missions = data.get("missions", [])
        self.emoji = data.get("emoji", "🎭")
        self.farewell = data.get("farewell", "Até a próxima, aventureiro.")

    def build_system_prompt(self) -> str:
        """
        Constrói o prompt de sistema completo para o ChatGPT
        com base na persona do NPC.
        """
        prompt_parts = [
            f"Você é {self.name}, {self.title}.",
            f"\n## Personalidade\n{self.personality}",
            f"\n## Estilo de Fala\n{self.speech_style}",
        ]

        if self.backstory:
            prompt_parts.append(f"\n## História\n{self.backstory}")

        if self.rules:
            rules_text = "\n".join(f"- {rule}" for rule in self.rules)
            prompt_parts.append(f"\n## Regras de Comportamento\n{rules_text}")

        prompt_parts.extend([
            "\n## Instruções Gerais",
            "- Responda SEMPRE em português do Brasil.",
            "- Mantenha respostas com no máximo 3 parágrafos.",
            "- NUNCA quebre o personagem.",
            "- Use o estilo de fala definido acima.",
            "- Seja envolvente e interativo.",
            f"- Se o usuário quiser sair, despeça-se dizendo: '{self.farewell}'",
        ])

        return "\n".join(prompt_parts)

    def __repr__(self):
        return f"Persona(id='{self.id}', name='{self.name}')"


class NPCManager:
    """Gerencia o carregamento e troca de personas de NPCs."""

    def __init__(self):
        self.personas: dict[str, Persona] = {}
        self.active_persona: Persona | None = None
        self._load_all_personas()

    def _load_all_personas(self):
        """Carrega todas as personas dos arquivos JSON na pasta personas/."""
        personas_path = config.PERSONAS_DIR

        if not personas_path.exists():
            console.print("[yellow]⚠️  Pasta de personas não encontrada.[/yellow]")
            return

        for json_file in personas_path.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                persona = Persona(data)
                self.personas[persona.id] = persona

                if config.DEBUG:
                    console.print(f"[dim]📂 Persona carregada: {persona.name}[/dim]")

            except (json.JSONDecodeError, KeyError) as e:
                console.print(
                    f"[yellow]⚠️  Erro ao carregar {json_file.name}: {e}[/yellow]"
                )

        console.print(
            f"[green]✅ {len(self.personas)} persona(s) carregada(s).[/green]"
        )

    def set_persona(self, persona_id: str) -> Persona:
        """
        Define a persona ativa pelo ID.

        Args:
            persona_id: Identificador da persona.

        Returns:
            A persona ativada.

        Raises:
            ValueError: Se a persona não for encontrada.
        """
        if persona_id not in self.personas:
            available = ", ".join(self.personas.keys())
            raise ValueError(
                f"Persona '{persona_id}' não encontrada. "
                f"Disponíveis: {available}"
            )

        self.active_persona = self.personas[persona_id]
        console.print(
            f"\n[bold magenta]{self.active_persona.emoji} "
            f"Persona ativada: {self.active_persona.name} — "
            f"{self.active_persona.title}[/bold magenta]"
        )
        return self.active_persona

    def get_active_prompt(self) -> str:
        """Retorna o prompt de sistema da persona ativa."""
        if not self.active_persona:
            return "Você é um assistente útil que responde em português do Brasil."
        return self.active_persona.build_system_prompt()

    def get_greeting(self) -> str:
        """Retorna a saudação da persona ativa."""
        if not self.active_persona:
            return "Olá! Como posso ajudar?"
        return self.active_persona.greeting

    def list_personas(self):
        """Exibe uma tabela formatada com todas as personas disponíveis."""
        table = Table(
            title="🎭 Personas Disponíveis",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("ID", style="bold")
        table.add_column("Nome", style="magenta")
        table.add_column("Título", style="dim")
        table.add_column("Tema", style="green")
        table.add_column("", justify="center")

        for persona in self.personas.values():
            table.add_row(
                persona.id,
                persona.name,
                persona.title,
                persona.theme,
                persona.emoji,
            )

        console.print(table)

    def get_missions(self) -> list:
        """Retorna as missões da persona ativa."""
        if not self.active_persona:
            return []
        return self.active_persona.missions

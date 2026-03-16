"""
╔══════════════════════════════════════════════════════════════╗
║              VoxNPC — Motor de IA (OpenAI/ChatGPT)           ║
╚══════════════════════════════════════════════════════════════╝

Módulo responsável por:
- Gerenciar a comunicação com a API da OpenAI
- Manter o histórico de conversa (contexto)
- Enviar mensagens com system prompt personalizado
- Processar respostas da IA com personalidade de NPC
"""

from openai import OpenAI
from rich.console import Console

import config

console = Console()


class AIEngine:
    """Motor de IA que gerencia a comunicação com o ChatGPT."""

    def __init__(self, system_prompt: str = None):
        """
        Inicializa o motor de IA.

        Args:
            system_prompt: Prompt de sistema que define a personalidade do NPC.
        """
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
        self.conversation_history = []

        if system_prompt:
            self.set_system_prompt(system_prompt)

    def set_system_prompt(self, prompt: str):
        """
        Define ou atualiza o prompt de sistema (personalidade do NPC).

        Args:
            prompt: Texto que define como a IA deve se comportar.
        """
        # Remove system prompt anterior se existir
        self.conversation_history = [
            msg for msg in self.conversation_history if msg["role"] != "system"
        ]
        # Adiciona novo system prompt no início
        self.conversation_history.insert(0, {
            "role": "system",
            "content": prompt
        })

    def send_message(self, user_message: str) -> str:
        """
        Envia uma mensagem do usuário e retorna a resposta da IA.

        Args:
            user_message: Texto da mensagem do usuário.

        Returns:
            Texto da resposta gerada pela IA.
        """
        # Adiciona mensagem do usuário ao histórico
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        console.print("[dim]🤖 Pensando...[/dim]")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.8,
                max_tokens=500,
            )

            assistant_message = response.choices[0].message.content.strip()

            # Adiciona resposta ao histórico (memória de conversa)
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            if config.DEBUG:
                console.print(f"[dim]🧠 Tokens usados: {response.usage.total_tokens}[/dim]")

            return assistant_message

        except Exception as e:
            error_msg = f"Erro ao comunicar com a IA: {str(e)}"
            console.print(f"[red]❌ {error_msg}[/red]")
            return "Perdão, aventureiro... minha mente se turvou por um momento. Tente novamente."

    def get_conversation_length(self) -> int:
        """Retorna o número de trocas de mensagem (excluindo system prompt)."""
        return len([
            msg for msg in self.conversation_history
            if msg["role"] != "system"
        ]) // 2

    def clear_history(self):
        """Limpa o histórico de conversa, mantendo o system prompt."""
        system_msgs = [
            msg for msg in self.conversation_history if msg["role"] == "system"
        ]
        self.conversation_history = system_msgs
        console.print("[dim]🗑️  Histórico de conversa limpo.[/dim]")

    def get_summary(self) -> dict:
        """Retorna um resumo do estado atual da conversa."""
        return {
            "model": self.model,
            "total_messages": len(self.conversation_history),
            "exchanges": self.get_conversation_length(),
            "has_persona": any(
                msg["role"] == "system" for msg in self.conversation_history
            ),
        }

"""
╔══════════════════════════════════════════════════════════════╗
║              VoxNPC — Testes Básicos                         ║
╚══════════════════════════════════════════════════════════════╝

Testes unitários para verificar a integridade dos módulos principais.
Execute com: python -m pytest tests/ -v
"""

import json
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from src.npc_manager import Persona, NPCManager
from src.game_mechanics import GameMechanics, PlayerStats, LEVELS
from src.ai_engine import AIEngine


# ============================================================
# Testes de Configuração
# ============================================================

def test_config_directories_exist():
    """Verifica se os diretórios configurados existem ou podem ser criados."""
    assert config.BASE_DIR.exists()
    assert config.PERSONAS_DIR.exists()


def test_config_defaults():
    """Verifica se os valores padrão estão definidos."""
    assert config.WHISPER_MODEL in ("tiny", "base", "small", "medium", "large")
    assert config.TTS_LANGUAGE == "pt-br"
    assert config.SAMPLE_RATE > 0
    assert config.RECORD_SECONDS > 0


# ============================================================
# Testes de Persona
# ============================================================

def test_persona_loading():
    """Verifica se as personas podem ser carregadas dos arquivos JSON."""
    personas_dir = config.PERSONAS_DIR
    json_files = list(personas_dir.glob("*.json"))
    assert len(json_files) >= 3, "Deve haver pelo menos 3 personas"


def test_persona_structure():
    """Verifica se cada persona tem os campos obrigatórios."""
    required_fields = ["id", "name", "title", "personality", "speech_style", "greeting"]

    for json_file in config.PERSONAS_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for field in required_fields:
            assert field in data, f"Campo '{field}' ausente em {json_file.name}"
            assert data[field], f"Campo '{field}' vazio em {json_file.name}"


def test_persona_system_prompt():
    """Verifica se o system prompt é gerado corretamente."""
    sample_data = {
        "id": "test",
        "name": "NPC Teste",
        "title": "Personagem de Teste",
        "personality": "Amigável e prestativo",
        "speech_style": "Informal e direto",
        "greeting": "Olá!",
    }
    persona = Persona(sample_data)
    prompt = persona.build_system_prompt()

    assert "NPC Teste" in prompt
    assert "Amigável e prestativo" in prompt
    assert "português do Brasil" in prompt


def test_npc_manager_loads_personas():
    """Verifica se o NPCManager carrega todas as personas."""
    manager = NPCManager()
    assert len(manager.personas) >= 3
    assert "sage" in manager.personas
    assert "cyberpunk" in manager.personas
    assert "medieval" in manager.personas


def test_npc_manager_set_persona():
    """Verifica se é possível ativar uma persona."""
    manager = NPCManager()
    persona = manager.set_persona("sage")
    assert persona.id == "sage"
    assert manager.active_persona is not None
    assert "Eldrin" in persona.name


# ============================================================
# Testes de Game Mechanics
# ============================================================

def test_initial_stats():
    """Verifica se as estatísticas iniciais estão corretas."""
    game = GameMechanics()
    assert game.stats.xp == 0
    assert game.stats.level == 1
    assert game.stats.interactions == 0


def test_xp_gain():
    """Verifica se o ganho de XP funciona."""
    game = GameMechanics()
    game.add_xp(25, "teste")
    assert game.stats.xp == 25


def test_level_up():
    """Verifica se o level up funciona corretamente."""
    game = GameMechanics()
    game.add_xp(50)  # Nível 2: Explorador
    assert game.stats.level == 2
    assert game.stats.level_name == "Explorador"


def test_interaction_registration():
    """Verifica se o registro de interação funciona."""
    game = GameMechanics()
    game.register_interaction("Olá, como vai?", "Estou bem, obrigado!")
    assert game.stats.interactions == 1
    assert game.stats.xp > 0
    assert game.stats.words_spoken == 3


def test_levels_are_ordered():
    """Verifica se os níveis estão em ordem crescente de XP."""
    for i in range(1, len(LEVELS)):
        assert LEVELS[i]["min_xp"] > LEVELS[i - 1]["min_xp"]
        assert LEVELS[i]["level"] == LEVELS[i - 1]["level"] + 1


def test_mission_system():
    """Verifica se o sistema de missões funciona."""
    game = GameMechanics()
    game.load_missions([
        {
            "id": "test_m1",
            "title": "Missão Teste",
            "description": "Teste de missão",
            "goal": "Completar teste",
            "xp_reward": 50,
        }
    ])
    assert len(game.stats.active_missions) == 1
    assert not game.stats.active_missions[0].completed

    result = game.complete_mission("test_m1")
    assert result is True
    assert game.stats.missions_completed == 1
    assert game.stats.xp >= 50


# ============================================================
# Testes do AI Engine (sem chamada real à API)
# ============================================================

def test_ai_engine_init():
    """Verifica se o AI Engine inicializa corretamente."""
    engine = AIEngine(system_prompt="Teste")
    assert len(engine.conversation_history) == 1
    assert engine.conversation_history[0]["role"] == "system"


def test_ai_engine_system_prompt():
    """Verifica se o system prompt pode ser atualizado."""
    engine = AIEngine(system_prompt="Prompt 1")
    engine.set_system_prompt("Prompt 2")
    system_msgs = [m for m in engine.conversation_history if m["role"] == "system"]
    assert len(system_msgs) == 1
    assert system_msgs[0]["content"] == "Prompt 2"


def test_ai_engine_clear_history():
    """Verifica se o histórico pode ser limpo mantendo o system prompt."""
    engine = AIEngine(system_prompt="Teste")
    engine.conversation_history.append({"role": "user", "content": "Oi"})
    engine.conversation_history.append({"role": "assistant", "content": "Olá!"})

    engine.clear_history()
    assert len(engine.conversation_history) == 1
    assert engine.conversation_history[0]["role"] == "system"


def test_ai_engine_conversation_length():
    """Verifica a contagem de trocas de mensagem."""
    engine = AIEngine(system_prompt="Teste")
    assert engine.get_conversation_length() == 0

    engine.conversation_history.append({"role": "user", "content": "Oi"})
    engine.conversation_history.append({"role": "assistant", "content": "Olá!"})
    assert engine.get_conversation_length() == 1


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

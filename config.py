"""
╔══════════════════════════════════════════════════════════════╗
║                    VoxNPC — Configuração                     ║
║         Protótipo de NPC Inteligente por Voz com IA          ║
╚══════════════════════════════════════════════════════════════╝

Módulo central de configuração do projeto.
Carrega variáveis de ambiente e define constantes globais.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# ============================================================
# Diretórios do Projeto
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"
PERSONAS_DIR = BASE_DIR / "personas"
LOGS_DIR = BASE_DIR / "logs"

# Garante que os diretórios existam
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# OpenAI / ChatGPT
# ============================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# ============================================================
# Whisper (Speech-to-Text)
# ============================================================
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# ============================================================
# gTTS (Text-to-Speech)
# ============================================================
TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "pt-br")

# ============================================================
# NPC / Persona
# ============================================================
DEFAULT_PERSONA = os.getenv("DEFAULT_PERSONA", "sage")

# ============================================================
# Áudio
# ============================================================
SAMPLE_RATE = 16000          # Taxa de amostragem para gravação
RECORD_SECONDS = 8           # Duração padrão da gravação em segundos
INPUT_AUDIO_FILE = AUDIO_DIR / "input.wav"
OUTPUT_AUDIO_FILE = AUDIO_DIR / "response.mp3"

# ============================================================
# Game Mechanics
# ============================================================
XP_PER_INTERACTION = 10      # XP ganho por interação
XP_BONUS_LONG_RESPONSE = 5   # Bônus por resposta longa
MISSION_BONUS_XP = 25        # XP por completar uma missão

# ============================================================
# Debug
# ============================================================
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# ============================================================
# Validação
# ============================================================
def validate_config():
    """Verifica se as configurações essenciais estão definidas."""
    errors = []
    if not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY não definida. Configure no arquivo .env")
    if errors:
        for error in errors:
            print(f"⚠️  {error}")
        return False
    return True

"""
╔══════════════════════════════════════════════════════════════╗
║              VoxNPC — Text-to-Speech (gTTS)                  ║
╚══════════════════════════════════════════════════════════════╝

Módulo responsável por:
- Converter texto em áudio usando Google Text-to-Speech (gTTS)
- Reproduzir o áudio gerado para o usuário
- Salvar histórico de áudios gerados
"""

import os
import time
from pathlib import Path
from rich.console import Console

import config

console = Console()

# Flags para imports lazy
_tts_deps_loaded = False
_audio_deps_loaded = False


def _import_tts_deps():
    """Importa gTTS sob demanda."""
    global gTTS, _tts_deps_loaded
    if not _tts_deps_loaded:
        try:
            from gtts import gTTS as _gTTS
            gTTS = _gTTS
            _tts_deps_loaded = True
        except ImportError as e:
            console.print(f"[red]❌ gTTS não encontrado: {e}[/red]")
            console.print("[dim]Instale com: pip install gTTS[/dim]")
            raise


def _import_audio_deps():
    """Importa pygame sob demanda e inicializa o mixer."""
    global pygame, _audio_deps_loaded
    if not _audio_deps_loaded:
        try:
            import pygame as _pygame
            pygame = _pygame
            pygame.mixer.init()
            _audio_deps_loaded = True
        except ImportError as e:
            console.print(f"[red]❌ pygame não encontrado: {e}[/red]")
            console.print("[dim]Instale com: pip install pygame[/dim]")
            raise


def synthesize_speech(text: str, output_path: str = None, language: str = None) -> str:
    """
    Converte texto em áudio usando gTTS e salva em arquivo MP3.

    Args:
        text: Texto a ser convertido em fala.
        output_path: Caminho de saída. Se None, usa o padrão.
        language: Código do idioma (padrão: config.TTS_LANGUAGE).

    Returns:
        Caminho do arquivo de áudio gerado.
    """
    output_path = output_path or str(config.OUTPUT_AUDIO_FILE)
    language = language or config.TTS_LANGUAGE

    _import_tts_deps()
    console.print("[dim]🔊 Gerando áudio da resposta...[/dim]")

    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_path)

    console.print("[green]✅ Áudio gerado com sucesso.[/green]")
    return output_path


def play_audio(audio_path: str = None):
    """
    Reproduz um arquivo de áudio.

    Args:
        audio_path: Caminho do arquivo de áudio. Se None, usa o padrão.
    """
    audio_path = audio_path or str(config.OUTPUT_AUDIO_FILE)

    if not os.path.exists(audio_path):
        console.print("[red]❌ Arquivo de áudio não encontrado.[/red]")
        return

    console.print("[bold cyan]🔊 Reproduzindo resposta...[/bold cyan]")
    try:
        _import_audio_deps()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        console.print(f"[yellow]⚠️  Erro ao reproduzir: {e}[/yellow]")


def speak(text: str, save_history: bool = False) -> str:
    """
    Pipeline completo: converte texto em áudio e reproduz.

    Args:
        text: Texto para converter em fala.
        save_history: Se True, salva uma cópia com timestamp.

    Returns:
        Caminho do arquivo de áudio gerado.
    """
    output_path = synthesize_speech(text)

    # Salva cópia com timestamp se solicitado
    if save_history:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        history_path = config.AUDIO_DIR / f"response_{timestamp}.mp3"
        import shutil
        shutil.copy2(output_path, str(history_path))
        console.print(f"[dim]💾 Cópia salva: {history_path.name}[/dim]")

    play_audio(output_path)
    return output_path

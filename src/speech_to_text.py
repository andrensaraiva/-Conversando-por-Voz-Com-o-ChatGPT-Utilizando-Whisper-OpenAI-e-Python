"""
╔══════════════════════════════════════════════════════════════╗
║              VoxNPC — Speech-to-Text (Whisper)               ║
╚══════════════════════════════════════════════════════════════╝

Módulo responsável por:
- Gravar áudio do microfone do usuário
- Transcrever áudio em texto utilizando OpenAI Whisper
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

import config

console = Console()

# Cache do modelo Whisper (carregado uma única vez)
_whisper_model = None

# Import lazy das dependências de áudio (só necessárias no modo voz)
def _import_audio_deps():
    """Importa dependências de áudio sob demanda."""
    global np, sd, sf, whisper
    try:
        import numpy as np
        import sounddevice as sd
        import soundfile as sf
        import whisper
    except ImportError as e:
        console.print(f"[red]❌ Dependência de áudio não encontrada: {e}[/red]")
        console.print("[dim]Instale com: pip install numpy sounddevice soundfile openai-whisper[/dim]")
        raise


def _load_model():
    """Carrega o modelo Whisper sob demanda e mantém em cache."""
    _import_audio_deps()
    global _whisper_model
    if _whisper_model is None:
        console.print(
            f"[dim]🔄 Carregando modelo Whisper ({config.WHISPER_MODEL})...[/dim]"
        )
        _whisper_model = whisper.load_model(config.WHISPER_MODEL)
        console.print("[green]✅ Modelo Whisper carregado com sucesso.[/green]")
    return _whisper_model


def record_audio(duration: int = None, sample_rate: int = None) -> str:
    """
    Grava áudio do microfone e salva em arquivo WAV.

    Args:
        duration: Duração da gravação em segundos (padrão: config.RECORD_SECONDS)
        sample_rate: Taxa de amostragem (padrão: config.SAMPLE_RATE)

    Returns:
        Caminho do arquivo de áudio gravado.
    """
    _import_audio_deps()
    duration = duration or config.RECORD_SECONDS
    sample_rate = sample_rate or config.SAMPLE_RATE
    audio_path = str(config.INPUT_AUDIO_FILE)

    console.print(f"\n[bold cyan]🎙️  Gravando... Fale por {duration} segundos.[/bold cyan]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task(description="Ouvindo...", total=None)
        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()

    # Normaliza o áudio
    audio_data = audio_data / (np.max(np.abs(audio_data)) + 1e-7)
    sf.write(audio_path, audio_data, sample_rate)

    console.print("[green]✅ Áudio capturado com sucesso.[/green]")
    return audio_path


def transcribe_audio(audio_path: str = None) -> str:
    """
    Transcreve um arquivo de áudio em texto usando Whisper.

    Args:
        audio_path: Caminho do arquivo de áudio. Se None, usa o padrão.

    Returns:
        Texto transcrito do áudio.
    """
    audio_path = audio_path or str(config.INPUT_AUDIO_FILE)
    model = _load_model()

    console.print("[dim]🔄 Transcrevendo áudio...[/dim]")
    result = model.transcribe(audio_path, language="pt", fp16=False)
    text = result["text"].strip()

    if config.DEBUG:
        console.print(f"[dim]📝 Transcrição: {text}[/dim]")

    console.print("[green]✅ Transcrição concluída.[/green]")
    return text


def listen() -> str:
    """
    Pipeline completo: grava áudio e transcreve em texto.

    Returns:
        Texto transcrito da fala do usuário.
    """
    audio_path = record_audio()
    text = transcribe_audio(audio_path)
    return text

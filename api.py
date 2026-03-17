"""
╔══════════════════════════════════════════════════════════════╗
║              VoxNPC — API Web (FastAPI)                       ║
╚══════════════════════════════════════════════════════════════╝

API REST que expõe o VoxNPC como serviço web.
Permite conversar com NPCs via navegador.

Uso local:
    uvicorn api:app --reload --port 8000

Acesse: http://localhost:8000
"""

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field
from pathlib import Path
from openai import OpenAI
import io
import tempfile
import os

import config
from src.ai_engine import AIEngine
from src.npc_manager import NPCManager, Persona
from src.game_mechanics import GameMechanics

app = FastAPI(
    title="VoxNPC API",
    description="Converse com NPCs inteligentes alimentados por IA",
    version="1.0.0",
)

# Servir arquivos estáticos (frontend)
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Estado global das sessões (em produção, usar Redis/DB)
sessions: dict[str, dict] = {}
npc_manager = NPCManager()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    persona_id: str = "sage"
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    persona_name: str
    persona_emoji: str
    stats: dict


class PersonaInfo(BaseModel):
    id: str
    name: str
    title: str
    theme: str
    emoji: str
    greeting: str


def _get_or_create_session(session_id: str, persona_id: str) -> dict:
    """Obtém ou cria uma sessão de conversa."""
    if session_id not in sessions or sessions[session_id]["persona_id"] != persona_id:
        persona = npc_manager.set_persona(persona_id)
        engine = AIEngine(system_prompt=persona.build_system_prompt())
        game = GameMechanics()

        missions = persona.missions if hasattr(persona, "missions") else []
        if missions:
            game.load_missions(missions)

        sessions[session_id] = {
            "engine": engine,
            "game": game,
            "persona": persona,
            "persona_id": persona_id,
        }
    return sessions[session_id]


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve a página principal."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return HTMLResponse("<h1>VoxNPC</h1><p>Coloque index.html em /static/</p>")


@app.get("/api/personas", response_model=list[PersonaInfo])
async def list_personas():
    """Lista todas as personas disponíveis."""
    result = []
    for pid, persona in npc_manager.personas.items():
        result.append(PersonaInfo(
            id=persona.id,
            name=persona.name,
            title=persona.title,
            theme=persona.theme,
            emoji=persona.emoji,
            greeting=persona.greeting,
        ))
    return result


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Envia uma mensagem e recebe a resposta do NPC."""
    session = _get_or_create_session(req.session_id, req.persona_id)

    engine: AIEngine = session["engine"]
    game: GameMechanics = session["game"]
    persona: Persona = session["persona"]

    # Gera resposta da IA
    response = engine.send_message(req.message)

    # Registra interação no sistema de game
    game.register_interaction(req.message, response)

    return ChatResponse(
        response=response,
        persona_name=persona.name,
        persona_emoji=persona.emoji,
        stats={
            "xp": game.stats.xp,
            "level": game.stats.level,
            "level_name": game.stats.level_name,
            "interactions": game.stats.interactions,
        },
    )


@app.post("/api/reset")
async def reset_session(session_id: str = "default"):
    """Reseta uma sessão de conversa."""
    if session_id in sessions:
        del sessions[session_id]
    return {"status": "ok"}


@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcreve áudio enviado pelo navegador usando a API Whisper da OpenAI."""
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    # Salva o áudio em arquivo temporário com a extensão correta
    suffix = ".webm"
    if audio.content_type:
        ext_map = {
            "audio/webm": ".webm",
            "audio/ogg": ".ogg",
            "audio/wav": ".wav",
            "audio/mp4": ".m4a",
            "audio/mpeg": ".mp3",
        }
        suffix = ext_map.get(audio.content_type, ".webm")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="pt",
            )
        return {"text": transcription.text}
    finally:
        os.unlink(tmp_path)


@app.post("/api/tts")
async def text_to_speech(request: Request):
    """Converte texto em áudio usando a API TTS da OpenAI."""
    body = await request.json()
    text = body.get("text", "")
    if not text:
        return {"error": "Texto vazio"}

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
        response_format="mp3",
    )

    audio_bytes = response.content
    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=response.mp3"},
    )

# api/index.py
import os
import logging
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# =========================
# Setup FastAPI + CORS
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # atur sesuai kebutuhan produksi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

# =========================
# Konfigurasi API (isi nanti sesuai project baru)
# =========================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # <- isi di environment
OPENROUTER_URL = ""  # <- kosong, isi sesuai API tujuan
MODEL_NAME = ""       # <- kosong, isi sesuai model yang dipakai

# =========================
# System Prompt (kosong dulu)
# =========================
BASE_SYSTEM_PROMPT = {
    "role": "system",
    "content": ""  # isi sesuai karakter bot/project baru
}

# =========================
# Preset Mode (isi default saja, bisa diubah)
# =========================
MODE_SETTINGS = {
    "qa": {
        "max_tokens": 1000,
        "temperature": 0.5,
        "top_p": 0.9
    },
    "creative": {
        "max_tokens": 2000,
        "temperature": 0.9,
        "top_p": 0.95
    }
}

# =========================
# Memory Percakapan (opsional)
# =========================
CONVERSATIONS = {}
MAX_HISTORY = 10

def add_to_conversation(session_id: str, role: str, content: str):
    if session_id not in CONVERSATIONS:
        CONVERSATIONS[session_id] = []
    CONVERSATIONS[session_id].append({"role": role, "content": content})

    if len(CONVERSATIONS[session_id]) > MAX_HISTORY * 2:
        CONVERSATIONS[session_id] = CONVERSATIONS[session_id][-MAX_HISTORY*2:]

def call_openrouter_api_with_history(messages: list, mode: str = "qa") -> str:
    if not OPENROUTER_API_KEY:
        logging.error("OPENROUTER_API_KEY is not set.")
        return "❌ Error: API key tidak ditemukan."

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            # isi sesuai kebutuhan project (opsional)
            # "HTTP-Referer": "https://your-app.com",
            # "X-Title": "Nama Project"
        }

        params = MODE_SETTINGS.get(mode, MODE_SETTINGS["qa"])

        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": params["max_tokens"],
            "temperature": params["temperature"],
            "top_p": params["top_p"]
        }

        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        logging.error(f"API request error: {e}")
        return "❌ Error saat menghubungi AI."
    except Exception as e:
        logging.error(f"API processing error: {e}")
        return "❌ Error saat memproses respons AI."


# =========================
# Endpoint Dasar
# =========================
@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message", "").strip()
        extra_instruction = body.get("instruction", "").strip()
        mode = body.get("mode", "qa").lower()
        session_id = body.get("session_id", "default")

        if not user_message:
            return JSONResponse({"error": "Pesan kosong"}, status_code=400)

        add_to_conversation(session_id, "user", user_message)

        messages = [BASE_SYSTEM_PROMPT]
        if extra_instruction:
            messages.append({"role": "system", "content": extra_instruction})
        messages.extend(CONVERSATIONS[session_id])

        reply = call_openrouter_api_with_history(messages, mode)
        add_to_conversation(session_id, "assistant", reply)

        return {"reply": reply, "mode": mode, "session_id": session_id}

    except Exception as e:
        logging.error(f"Request body error: {e}")
        return JSONResponse({"error": "Bad request body"}, status_code=400)


@app.get("/welcome")
async def welcome():
    """Template pesan awal (kosong dulu)."""
    welcome_message = (
        "👋 Selamat datang di bot baru Anda.\n\n"
        "Silakan atur pesan awal di sini sesuai kebutuhan project."
    )
    return {"reply": welcome_message}

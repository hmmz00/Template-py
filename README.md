📌 README.md (Template Project FastAPI Bot di Vercel)

# 🤖 FastAPI Bot Template (Vercel Ready)

Template ini adalah kerangka dasar untuk membuat chatbot berbasis **FastAPI** yang bisa dijalankan di **Vercel**.  
Struktur sudah disiapkan dengan endpoint standar (`/ping`, `/chat`, `/welcome`) dan siap dihubungkan ke API LLM (OpenRouter, OpenAI, Anthropic, dsb).

---

## 🚀 Cara Deploy ke Vercel

1. **Clone project** ke lokal
   ```bash
   git clone <repo-url>
   cd <repo-folder>

2. Pastikan struktur folder:

/api/index.py   # endpoint utama FastAPI
requirements.txt # daftar dependency
README.md


3. Install dependency lokal (opsional untuk testing lokal)

pip install -r requirements.txt

isi requirements.txt minimal:

fastapi
uvicorn
requests


4. Deploy ke Vercel

Login ke Vercel

Import repo dari GitHub

Pastikan root project berisi folder api/

Vercel otomatis mendeteksi FastAPI dan menjalankannya.



5. Atur Environment Variables di dashboard Vercel:

OPENROUTER_API_KEY=xxxxxx

(opsional) MODEL_NAME=openai/gpt-4

(opsional) OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions





---

⚙️ Konfigurasi Template

🔑 API Config (index.py)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = ""   # isi sesuai endpoint API yang dipakai
MODEL_NAME = ""       # isi sesuai model, contoh: "openai/gpt-4"

🧠 System Prompt

Atur gaya/karakter bot:

BASE_SYSTEM_PROMPT = {
    "role": "system",
    "content": "Kamu adalah asisten ramah siap membantu user."
}

📜 Welcome Message

Ubah pesan sambutan di endpoint /welcome:

@app.get("/welcome")
async def welcome():
    welcome_message = (
        "👋 Selamat datang di bot baru Anda.\n\n"
        "Silakan atur pesan awal di sini sesuai kebutuhan project."
    )
    return {"reply": welcome_message}


---

📡 Endpoint yang Tersedia

GET /ping → cek status bot ({"status": "ok"})

GET /welcome → pesan awal sambutan

POST /chat → kirim pesan ke bot

{
  "message": "Halo bot",
  "instruction": "",
  "mode": "qa",
  "session_id": "user1"
}



---

🛠️ Customisasi

1. Tambah mode baru di MODE_SETTINGS (misal: story, poetry, dll).


2. Ganti BASE_SYSTEM_PROMPT sesuai persona bot.


3. Tambah endpoint baru jika butuh (contoh: /summarize, /translate).




---

📌 Catatan

Template ini sengaja kosongkan hal-hal spesifik (model, prompt, welcome message) supaya bisa dipakai ulang untuk project apa saja.

Semua logika memory percakapan (CONVERSATIONS) tetap ada, jadi bisa langsung dipakai jika ingin chatbot dengan konteks.



---

✍️ Dibuat sebagai template siap pakai. Tinggal isi prompt & model sesuai projectmu 🚀

---

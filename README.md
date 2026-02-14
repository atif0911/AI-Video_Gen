# AstroNova AI Video Pipeline 🎥

An automated, end-to-end AI video generation system built for the **ASTRONOVA SYNERGIES LLP** technical assignment. This application takes a single topic and produces a fully edited YouTube video with script, voiceover, stock footage, subtitles, and SEO metadata.

---

## 🚀 Features

- **AI Scripting:** Automated script generation using **Gemini 1.5 Flash**
- **Neural Voiceover:** High-quality TTS using **Edge-TTS**
- **Smart Visuals:** Context-aware stock footage fetching via **Pexels API**
- **Automated Editing:** Seamless video stitching and subtitle overlay using **MoviePy**
- **Real-time Dashboard:** Flask-based UI with background processing and live status updates
- **Smart Resume:** Asset-aware pipeline that skips existing files to optimize API usage
- **YouTube Integration:** Automated SEO metadata generation and YouTube upload

---

## 🛠️ Tech Stack

**Backend:** Python, Flask  
**Database:** SQLite (SQLAlchemy)  
**Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)  
**Video Engine:** MoviePy, FFmpeg  

---

## 📦 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/atif0911/AI-Video_Gen.git
cd astronova_pipeline
2️⃣ Create Virtual Environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Environment Configuration
Create a .env file in the root directory and add your API keys:

GEMINI_API_KEY=your_key_here
PEXELS_API_KEY=your_key_here
SECRET_KEY=dev_key_123

5️⃣ Initialize & Run
python app.py

Visit:
http://127.0.0.1:5000

📌 Notes
Ensure FFmpeg is installed and added to your system PATH.
Make sure your API keys are valid and have sufficient quota.
The pipeline automatically skips already-generated assets to optimize performance.

🧠 Technical Highlights: "Smart Resume"
The pipeline includes a custom checkpoint system. Before calling external APIs, the engine verifies the local existence of script_text in the database and asset files in the project directory. This ensures resilience against network failures and optimizes API quota usage.

📄 License
This project was developed as part of a technical assessment for ASTRONOVA SYNERGIES LLP.

---

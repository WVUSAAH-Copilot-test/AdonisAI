# 🤖 AdonisAI – Persönlicher KI-Assistent

Ein kostenloser, Open-Source KI-Assistent, der Text- und Sprachbefehle versteht, Kalender-Termine verwaltet und über verschiedene Plattformen erreichbar ist.

## 📋 Features

- ✅ **Telegram Bot Integration** – Steuerung über Telegram-Nachrichten
- 📅 **Google Calendar Integration** – Termine erstellen, lesen und löschen
- 🎤 **Speech-to-Text** – Sprachnachrichten verstehen (Vosk/Whisper)
- 🔊 **Text-to-Speech** – Antworten als Sprachausgabe (gTTS/Coqui TTS)
- 🧠 **KI-Modelle** – Kostenfreie Nutzung via Hugging Face & OpenRouter
- 🔐 **Privacy-First** – Alle Daten bleiben unter deiner Kontrolle

## 🚀 Installation

### Voraussetzungen

- Python 3.10 oder höher
- Telegram Account
- (Optional) Google Account für Calendar-Integration

### Lokale Installation

1. **Repository klonen**
```bash
git clone https://github.com/wvusaah/AdonisAI.git
cd AdonisAI
```

2. **Virtuelle Umgebung erstellen**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# oder
venv\Scripts\activate     # Windows
```

3. **Abhängigkeiten installieren**
```bash
pip install -r requirements.txt
```

4. **Umgebungsvariablen konfigurieren**
```bash
cp .env.example .env
# Bearbeite .env und füge deine API-Keys ein
```

5. **Bot starten**
```bash
python src/main.py
```

## 🤖 Telegram Bot einrichten

1. Öffne Telegram und suche nach [@BotFather](https://t.me/botfather)
2. Sende `/newbot` und folge den Anweisungen
3. Kopiere den Bot-Token
4. Füge den Token in `.env` ein:
   ```
   TELEGRAM_BOT_TOKEN=dein_token_hier
   ```
5. Starte den Bot mit `python src/main.py`
6. Suche deinen Bot in Telegram und sende `/start`

## 📅 Google Calendar Integration (Optional)

1. Gehe zur [Google Cloud Console](https://console.cloud.google.com/)
2. Erstelle ein neues Projekt
3. Aktiviere die Google Calendar API
4. Erstelle OAuth 2.0 Credentials (Desktop App)
5. Lade die `credentials.json` herunter und speichere sie im Projektverzeichnis
6. Beim ersten Start wird ein Browser geöffnet für die Autorisierung

## 🌐 Deployment

### Replit

1. Erstelle ein neues Repl und importiere das Repository
2. Füge die Secrets (Umgebungsvariablen) in den Secrets-Tab ein
3. Klicke auf "Run"

### Render.com

1. Erstelle einen neuen Web Service
2. Verbinde dein GitHub Repository
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python src/main.py`
5. Füge Environment Variables in den Settings hinzu

## 🗺️ Roadmap

### Phase 1: Grundgerüst ✅
- [x] Telegram Bot Basis-Integration
- [x] Projektstruktur aufsetzen
- [ ] Einfache Textverarbeitung

### Phase 2: KI-Integration 🚧
- [ ] Hugging Face API anbinden
- [ ] OpenRouter Integration
- [ ] Kontextverständnis implementieren
- [ ] Intent-Erkennung für Befehle

### Phase 3: Calendar-Funktionen 📅
- [ ] Google Calendar API Setup
- [ ] Termine auslesen
- [ ] Neue Termine erstellen
- [ ] Termine bearbeiten/löschen
- [ ] Natürlichsprachliche Datumserkennung

### Phase 4: Sprachverarbeitung 🎤
- [ ] Speech-to-Text (Vosk) Integration
- [ ] Sprachnachrichten in Telegram verarbeiten
- [ ] Text-to-Speech (gTTS) für Antworten
- [ ] Sprachausgabe-Optimierung

### Phase 5: Erweiterte Features 🔮
- [ ] Siri Shortcuts Integration
- [ ] Web-UI (Flask/FastAPI)
- [ ] Erinnerungen & Notifications
- [ ] Multi-User Support
- [ ] Konversations-Historie
- [ ] Plugin-System für Erweiterungen

## 📁 Projektstruktur

```
AdonisAI/
├── README.md
├── .env.example
├── requirements.txt
├── src/
│   ├── main.py                    # Haupteinstiegspunkt
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── telegram_bot.py        # Telegram Bot Logik
│   │   └── handlers.py            # Command Handler
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── ai_client.py           # KI-Client Interface
│   │   ├── hf_provider.py         # Hugging Face Provider
│   │   └── openrouter_provider.py # OpenRouter Provider
│   ├── calendar/
│   │   ├── __init__.py
│   │   └── calendar_client.py     # Google Calendar API
│   ├── speech/
│   │   ├── __init__.py
│   │   ├── stt_vosk.py            # Speech-to-Text
│   │   └── tts_gtts.py            # Text-to-Speech
│   ├── storage/
│   │   ├── __init__.py
│   │   └── store.py               # Datenbank/Storage
│   └── utils/
│       ├── __init__.py
│       └── nlp_utils.py           # NLP Hilfsfunktionen
└── tests/
    └── ...
```

## 🛠️ Technologie-Stack

- **Python 3.10+** – Programmiersprache
- **python-telegram-bot** – Telegram Bot Framework
- **google-api-python-client** – Google Calendar API
- **requests** – HTTP Client
- **python-dotenv** – Umgebungsvariablen
- **vosk / whisper.cpp** – Speech-to-Text
- **gTTS / Coqui TTS** – Text-to-Speech
- **sqlite-utils** – Lokale Datenhaltung
- **dateparser** – Natürliche Datumserkennung

## 🤝 Mitwirken

Contributions sind willkommen! Bitte erstelle ein Issue oder einen Pull Request.

1. Fork das Projekt
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📄 Lizenz

MIT License – siehe [LICENSE](LICENSE) für Details.

## 💡 Inspiration

Dieses Projekt entstand aus dem Wunsch nach einem vollständig kostenlosen, selbst-gehosteten KI-Assistenten, der die Privatsphäre respektiert und keine monatlichen Gebühren verursacht.

## 📞 Kontakt

Bei Fragen oder Anregungen, erstelle gerne ein Issue auf GitHub!

---

**Made with ❤️ by the AdonisAI Community**

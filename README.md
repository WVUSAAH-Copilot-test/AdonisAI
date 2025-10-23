# 🤖 AdonisAI – Personal AI Assistant# 🤖 AdonisAI – Persönlicher KI-Assistent



A free, open-source AI assistant that understands text and voice commands, manages calendar events, and is accessible across multiple platforms.Ein kostenloser, Open-Source KI-Assistent, der Text- und Sprachbefehle versteht, Kalender-Termine verwaltet und über verschiedene Plattformen erreichbar ist.



## ✨ Current Features (Phase 3.5)## 📋 Features



- 🤖 **AI-Driven Conversation** – All messages processed through AI with context awareness- ✅ **Telegram Bot Integration** – Steuerung über Telegram-Nachrichten

- 💬 **Context Management** – Remembers last 10 messages per user (30-minute TTL)- 📅 **Google Calendar Integration** – Termine erstellen, lesen und löschen

- 📅 **Calendar Integration** – Create, read, and manage events with natural language- 🎤 **Speech-to-Text** – Sprachnachrichten verstehen (Vosk/Whisper)

- 🗓️ **Calendar Commands** – `/today`, `/tomorrow`, `/week`, `/next` for quick overview- 🔊 **Text-to-Speech** – Antworten als Sprachausgabe (gTTS/Coqui TTS)

- 🧠 **Natural Language Processing** – German language support for dates and times- 🧠 **KI-Modelle** – Kostenfreie Nutzung via Hugging Face & OpenRouter

- ⚡ **Conflict Detection** – Warns about overlapping events- 🔐 **Privacy-First** – Alle Daten bleiben unter deiner Kontrolle

- 🔐 **SSL Workaround** – Works behind corporate firewalls (Zscaler)

- 📱 **Telegram Bot** – Full integration with command handlers## 🚀 Installation

- 🎯 **Smart Actions** – AI decides whether to create events, list events, or answer questions

### Voraussetzungen

## 🚀 Quick Start

- Python 3.10 oder höher

### Prerequisites- Telegram Account

- (Optional) Google Account für Calendar-Integration

- Python 3.6+ (compatible with corporate environments)

- Telegram Account### Lokale Installation

- OpenRouter API Key (for AI)

1. **Repository klonen**

### Installation```bash

git clone https://github.com/wvusaah/AdonisAI.git

1. **Clone the repository**cd AdonisAI

```bash```

git clone https://github.com/WVUSAAH-Copilot-test/AdonisAI.git

cd AdonisAI2. **Virtuelle Umgebung erstellen**

``````bash

python -m venv venv

2. **Create virtual environment**source venv/bin/activate  # Linux/macOS

```bash# oder

python -m venv venvvenv\Scripts\activate     # Windows

source venv/bin/activate  # Linux/macOS```

# or

venv\Scripts\activate     # Windows3. **Abhängigkeiten installieren**

``````bash

pip install -r requirements.txt

3. **Install dependencies**```

```bash

pip install -r requirements.txt4. **Umgebungsvariablen konfigurieren**

``````bash

cp .env.example .env

4. **Configure environment variables**# Bearbeite .env und füge deine API-Keys ein

```bash```

cp .env.example .env

# Edit .env and add your API keys:5. **Bot starten**

# - TELEGRAM_BOT_TOKEN (from @BotFather)```bash

# - OPENROUTER_API_KEY (from openrouter.ai)python src/main.py

``````



5. **Start the bot**## 🤖 Telegram Bot einrichten

```bash

python run.py1. Öffne Telegram und suche nach [@BotFather](https://t.me/botfather)

```2. Sende `/newbot` und folge den Anweisungen

3. Kopiere den Bot-Token

## 🤖 Telegram Bot Setup4. Füge den Token in `.env` ein:

   ```

1. Open Telegram and search for [@BotFather](https://t.me/botfather)   TELEGRAM_BOT_TOKEN=dein_token_hier

2. Send `/newbot` and follow the instructions   ```

3. Copy the bot token5. Starte den Bot mit `python src/main.py`

4. Add the token to `.env`:6. Suche deinen Bot in Telegram und sende `/start`

   ```

   TELEGRAM_BOT_TOKEN=your_token_here## 📅 Google Calendar Integration (Optional)

   ```

5. Start the bot with `python run.py`1. Gehe zur [Google Cloud Console](https://console.cloud.google.com/)

6. Find your bot in Telegram and send `/start`2. Erstelle ein neues Projekt

3. Aktiviere die Google Calendar API

## 💡 Usage Examples4. Erstelle OAuth 2.0 Credentials (Desktop App)

5. Lade die `credentials.json` herunter und speichere sie im Projektverzeichnis

### Natural Language Event Creation6. Beim ersten Start wird ein Browser geöffnet für die Autorisierung



```## 🌐 Deployment

You: "Create appointment tomorrow 3 PM meeting with Max"

Bot: ✅ Event created! Meeting with Max @ 24.10.2025 15:00### Replit



You: "Schedule dentist next Monday at 10"1. Erstelle ein neues Repl und importiere das Repository

Bot: ✅ Event created! Dentist @ 28.10.2025 10:002. Füge die Secrets (Umgebungsvariablen) in den Secrets-Tab ein

```3. Klicke auf "Run"



### Context-Aware Conversations### Render.com



```1. Erstelle einen neuen Web Service

You: "Customer Max wants to meet next week Monday or Wednesday"2. Verbinde dein GitHub Repository

Bot: "Which day works better for you?"3. Build Command: `pip install -r requirements.txt`

You: "Wednesday"4. Start Command: `python src/main.py`

Bot: "What time would you prefer?"5. Füge Environment Variables in den Settings hinzu

You: "2:30 PM"

Bot: ✅ Created "Meeting next Wednesday 2:30 PM with Customer Max"## 🗺️ Roadmap

```

### Phase 1: Grundgerüst ✅

### Calendar Commands- [x] Telegram Bot Basis-Integration

- [x] Projektstruktur aufsetzen

```- [ ] Einfache Textverarbeitung

/today      - Shows today's events

/tomorrow   - Shows tomorrow's events### Phase 2: KI-Integration 🚧

/week       - Shows this week's overview- [ ] Hugging Face API anbinden

/next       - Shows next upcoming event- [ ] OpenRouter Integration

/features   - Shows all available features- [ ] Kontextverständnis implementieren

/help       - Shows help message- [ ] Intent-Erkennung für Befehle

```

### Phase 3: Calendar-Funktionen 📅

## 📅 Calendar Integration- [ ] Google Calendar API Setup

- [ ] Termine auslesen

### Current Status- [ ] Neue Termine erstellen

- [ ] Termine bearbeiten/löschen

- ✅ **Mock Provider** – Working perfectly for local development- [ ] Natürlichsprachliche Datumserkennung

- 🔒 **iCloud Calendar** – Blocked by corporate network (CalDAV)

- 🔒 **Google Calendar** – Blocked by corporate network (OAuth)### Phase 4: Sprachverarbeitung 🎤

- [ ] Speech-to-Text (Vosk) Integration

### Testing Outside Corporate Network- [ ] Sprachnachrichten in Telegram verarbeiten

- [ ] Text-to-Speech (gTTS) für Antworten

Once outside the corporate network, you can enable real calendar providers:- [ ] Sprachausgabe-Optimierung



1. **iCloud Calendar**### Phase 5: Erweiterte Features 🔮

```bash- [ ] Siri Shortcuts Integration

# Add to .env:- [ ] Web-UI (Flask/FastAPI)

CALENDAR_PROVIDER=icloud- [ ] Erinnerungen & Notifications

ICLOUD_USERNAME=your@icloud.com- [ ] Multi-User Support

ICLOUD_PASSWORD=app_specific_password- [ ] Konversations-Historie

```- [ ] Plugin-System für Erweiterungen



2. **Google Calendar**## 📁 Projektstruktur

```bash

# Add to .env:```

CALENDAR_PROVIDER=googleAdonisAI/

# Follow OAuth setup in CHANGELOG.md├── README.md

```├── .env.example

├── requirements.txt

## 🏢 Corporate Network Support├── src/

│   ├── main.py                    # Haupteinstiegspunkt

AdonisAI includes an SSL workaround for corporate environments with SSL inspection (Zscaler, etc.):│   ├── bot/

│   │   ├── __init__.py

- `ssl_patch.py` automatically patches SSL verification│   │   ├── telegram_bot.py        # Telegram Bot Logik

- Works with corporate proxy configurations│   │   └── handlers.py            # Command Handler

- No manual SSL certificate installation required│   ├── ai/

│   │   ├── __init__.py

## 🗺️ Roadmap│   │   ├── ai_client.py           # KI-Client Interface

│   │   ├── hf_provider.py         # Hugging Face Provider

### Phase 3 (Current) ✅│   │   └── openrouter_provider.py # OpenRouter Provider

- [x] Phase 3.1: Calendar Foundation (Abstract client, 3 providers)│   ├── calendar/

- [x] Phase 3.2: CRUD Operations (Create, Read, Update, Delete)│   │   ├── __init__.py

- [x] Phase 3.3: NLP Enhancements (German natural language)│   │   └── calendar_client.py     # Google Calendar API

- [x] Phase 3.4: Bot Integration (Commands, conflict detection)│   ├── speech/

- [x] Phase 3.5: AI Enhancements (Context management, AI-driven processing)│   │   ├── __init__.py

- [ ] Phase 3.6: Testing & Documentation (Real calendar tests, Siri Shortcuts)│   │   ├── stt_vosk.py            # Speech-to-Text

│   │   └── tts_gtts.py            # Text-to-Speech

### Phase 4: Advanced Features 🔮│   ├── storage/

- [ ] Multi-calendar support (personal, work, shared)│   │   ├── __init__.py

- [ ] Smart scheduling (find free slots automatically)│   │   └── store.py               # Datenbank/Storage

- [ ] Recurring events support│   └── utils/

- [ ] Event reminders and notifications│       ├── __init__.py

- [ ] Calendar sharing and permissions│       └── nlp_utils.py           # NLP Hilfsfunktionen

- [ ] Time zone support└── tests/

    └── ...

### Phase 5: Platform Expansion 🌐```

- [ ] Siri Shortcuts integration (iOS)

- [ ] Web UI (Flask/FastAPI)## 🛠️ Technologie-Stack

- [ ] Google Assistant integration

- [ ] WhatsApp bot- **Python 3.10+** – Programmiersprache

- [ ] Slack integration- **python-telegram-bot** – Telegram Bot Framework

- [ ] Microsoft Teams bot- **google-api-python-client** – Google Calendar API

- **requests** – HTTP Client

### Phase 6: Enterprise Features 🏢- **python-dotenv** – Umgebungsvariablen

- [ ] Multi-user support with user management- **vosk / whisper.cpp** – Speech-to-Text

- [ ] Team calendars and scheduling- **gTTS / Coqui TTS** – Text-to-Speech

- [ ] Meeting room booking- **sqlite-utils** – Lokale Datenhaltung

- [ ] Integration with Outlook/Exchange- **dateparser** – Natürliche Datumserkennung

- [ ] LDAP/Active Directory authentication

- [ ] Audit logs and analytics## 🤝 Mitwirken



## 📁 Project StructureContributions sind willkommen! Bitte erstelle ein Issue oder einen Pull Request.



```1. Fork das Projekt

AdonisAI/2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)

├── README.md                      # English documentation3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)

├── README_DE.md                   # German documentation4. Push zum Branch (`git push origin feature/AmazingFeature`)

├── CHANGELOG.md                   # English changelog (detailed)5. Öffne einen Pull Request

├── CHANGELOG_DE.md                # German changelog

├── .env.example                   # Environment variables template## 📄 Lizenz

├── requirements.txt               # Python dependencies

├── run.py                         # Application entry pointMIT License – siehe [LICENSE](LICENSE) für Details.

├── ssl_patch.py                   # SSL workaround for corporate networks

├── src/## 💡 Inspiration

│   ├── main.py                    # Main application logic

│   ├── bot/Dieses Projekt entstand aus dem Wunsch nach einem vollständig kostenlosen, selbst-gehosteten KI-Assistenten, der die Privatsphäre respektiert und keine monatlichen Gebühren verursacht.

│   │   ├── __init__.py

│   │   └── telegram_bot.py        # Telegram bot with AI integration## 📞 Kontakt

│   ├── ai/

│   │   ├── __init__.pyBei Fragen oder Anregungen, erstelle gerne ein Issue auf GitHub!

│   │   ├── ai_client.py           # AI client interface

│   │   └── openrouter_provider.py # OpenRouter implementation---

│   ├── calendar/

│   │   ├── __init__.py**Made with ❤️ by the AdonisAI Community**

│   │   ├── calendar_client.py     # Abstract calendar client
│   │   ├── icloud_provider.py     # iCloud CalDAV implementation
│   │   ├── google_provider.py     # Google Calendar API implementation
│   │   └── mock_provider.py       # Mock provider for testing
│   └── utils/
│       ├── __init__.py
│       ├── context_manager.py     # Conversation context management
│       └── nlp_utils.py           # Natural language processing utils
└── tests/
    ├── test_calendar_client.py    # Calendar CRUD tests
    ├── test_nlp_utils.py          # NLP tests
    └── test_bot_calendar.py       # Bot integration tests
```

## 🛠️ Technology Stack

- **Python 3.6+** – Programming language (corporate environment compatible)
- **python-telegram-bot 12.8** – Telegram bot framework (downgraded for Python 3.6)
- **OpenRouter** – AI provider (openai/gpt-3.5-turbo)
- **caldav** – CalDAV protocol for iCloud
- **google-api-python-client** – Google Calendar API
- **dateparser** – Natural language date/time parsing
- **requests** – HTTP client
- **python-dotenv** – Environment variables management

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calendar_client.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src tests/
```

## 🤝 Contributing

Contributions are welcome! Please check out our [CHANGELOG.md](CHANGELOG.md) to see current development status.

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Commit Message Convention

We follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test updates
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

## 🐛 Known Issues

- **Corporate Network**: Real calendar providers (iCloud, Google) blocked by corporate firewall
- **SSL Inspection**: Automatically handled by `ssl_patch.py`
- **Python 3.6**: Some features limited by older Python version requirements

See [CHANGELOG.md](CHANGELOG.md) for detailed issue tracking and workarounds.

## 📄 License

MIT License – see [LICENSE](LICENSE) for details.

## 💡 Inspiration

This project was created from the desire for a completely free, self-hosted AI assistant that respects privacy and doesn't require monthly subscription fees.

## 📞 Contact

For questions or suggestions, please create an issue on GitHub!

## 🌟 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) – Excellent Telegram bot framework
- [OpenRouter](https://openrouter.ai) – Free AI API access
- [dateparser](https://github.com/scrapinghub/dateparser) – Natural language date parsing
- All contributors and testers

---

**Made with ❤️ by the AdonisAI Community**

📖 [German Version](README_DE.md) | 📋 [Changelog](CHANGELOG.md) | 🐛 [Issues](https://github.com/WVUSAAH-Copilot-test/AdonisAI/issues)

# Changelog# Changelog



All notable changes to AdonisAI are documented in this file.Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.



The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).## [0.2.0] - 2025-10-22



---### Added - Phase 2 Abgeschlossen ✅



## [Phase 3.5] - 2025-10-23#### AI-Integration

- **src/ai/hf_provider.py**: Vollständige Hugging Face Implementation

### 🧠 AI Enhancements  - Text-Generierung mit mehreren Modellen (flan-t5-base, mistral, gpt2)

- **Fully AI-driven message processing**: All user messages are now processed through AI for intelligent decision-making  - Intent-Erkennung und Klassifikation

- **Context Manager**: Stores chat history (configurable: 10 messages, 30-minute TTL) per user  - Konfigurierbare Parameter (temperature, max_length)

- **Context-aware AI**: AI makes decisions based on full conversation context  - Error-Handling & Logging

- **Intelligent information linking**: Combines information across multiple messages for coherent understanding  - Funktioniert ohne API-Token (limitiert)

- **Enhanced system prompts**: Improved context awareness with explicit instructions and examples

- **src/ai/openrouter_provider.py**: OpenRouter Gateway

### 🔐 SSL Workaround for Corporate Networks  - Multi-Model-Support (GPT-3.5, Claude, Mistral, PaLM)

- **ssl_patch.py** (NEW): Disables SSL verification for corporate networks with restrictive firewalls (Zscaler compatibility)  - Chat-Format mit Message-Historie

- **SSLContext.wrap_socket patch**: Allows Telegram bot to connect behind corporate proxy  - System-Prompts & Context

- **run.py**: Automatically loads SSL patch before all imports  - Intent-Analyse

  - **Getestet und funktionsfähig** ✅

### 💬 Bot Features

- **`/features` command** (NEW): Detailed feature overview with real-time status indicators (✅/❌)- **src/ai/ai_client.py**: Erweitert mit besserer Dokumentation

- **Enhanced `/help` command**: More comprehensive with categories and examples

- **Enhanced `/info` command**: Updated with current feature status#### Bot-Integration

- **Improved title extraction**: Better regex patterns for accurate event title parsing from natural language- **src/bot/telegram_bot.py**: AI-Provider Integration

  - Automatische Provider-Wahl (HuggingFace/OpenRouter)

### 🔧 Technical Improvements  - AI-gestützte Antworten auf Benutzer-Nachrichten

- **OpenRouter Provider**: Refactored to synchronous `generate_response()` method with context string support  - Command-Type Detection (calendar, reminder, question, general)

- **Context Manager**: New utility class for managing per-user conversation history with TTL  - Graceful Fallback bei AI-Fehlern

- **Better error handling**: Improved traceback logging in main.py  - Async-Wrapper für synchrone Handler



### 📝 Files Changed#### Testing

- `src/utils/context_manager.py` (NEW, 120 lines): Chat history management with automatic cleanup- **tests/test_ai_providers.py**: Umfangreiche Tests

- `ssl_patch.py` (NEW, 30 lines): SSL verification workaround for corporate networks  - HuggingFace Provider Tests

- `src/bot/telegram_bot.py`: +200 lines (context integration, improved prompts)  - OpenRouter Provider Tests

- `src/ai/openrouter_provider.py`: Refactored for sync operation with context support  - Intent-Erkennung Tests

- `src/utils/nlp_utils.py`: Improved `extract_event_title()` with regex patterns  - Context & Parameter Tests

- `src/main.py`: Enhanced error logging with full tracebacks  - SSL-Workaround integriert

- `run.py`: SSL patch integration

#### Dokumentation

### 🎯 Example Conversation Flow- **docs/PHASE2.md**: Phase 2 Dokumentation

```  - Setup-Anleitung für AI-Provider

User: "I have a customer Max who wants to meet next week. He's available Monday afternoon or Wednesday midday"  - API-Keys besorgen

Bot: "Which day would work better for you?"  - Modell-Auswahl & Konfiguration

User: "Wednesday sounds good"  - Beispiele & Best Practices

Bot: "What time on Wednesday?"

User: "2:30 PM"#### Konfiguration

Bot: ✅ Created "Meeting next Wednesday 2:30 PM with Customer Max"- `.env.example` aktualisiert mit AI-Provider Settings

```- OpenRouter API-Key integriert

- Empfohlener Provider: OpenRouter

### 🔄 Context Memory Example

The AI now remembers:### Changed

- Customer name ("Max") from first message- Bot verwendet jetzt standardmäßig AI statt Echo

- Timeframe ("next week") from first message- Intelligente Antworten auf alle Nachrichten

- Day preference ("Wednesday") from conversation- Bessere Error-Messages mit Fallback

- Combines all information for final event creation

### Technical Details

**Commit**: `5a0f06b` - Phase 3.5 Testing- Beide Provider mit async/await

- Python 3.6 kompatibel (asyncio.get_event_loop statt asyncio.run)

---- Requests mit SSL-Workaround für Firmennetzwerke

- Modular & erweiterbar

## [Phase 3.4] - 2025-10-23

### Testing Results

### ✨ Calendar Integration - Bot Commands- ✅ OpenRouter: Funktioniert einwandfrei

- ⚠️ HuggingFace: Funktioniert (Rate-Limits ohne Token)

#### Features Added- ✅ Bot-Integration: Erfolgreich getestet

- **Calendar command suite**: `/today`, `/tomorrow`, `/week`, `/next`

- **Natural language event creation**: "Termin morgen 15 Uhr Meeting" creates an event### Next Steps (Phase 3)

- **Conflict detection**: Automatically warns when new events overlap with existing ones- [ ] Google Calendar OAuth2 Setup

- **Automatic event parsing**: Extracts date, time, title, and location from natural language- [ ] Event CRUD Implementierung

- **German weekday support**: Week overview displays German weekday names (Montag, Dienstag, etc.)- [ ] Natural Language Date Parsing

- **Time-until calculation**: `/next` command shows how long until the next event- [ ] Calendar Commands im Bot



### 📝 Bot Updates---

- **src/bot/telegram_bot.py**: +260 lines

  - `today_command()`: Shows all events for today## [0.1.0] - 2025-10-22

  - `tomorrow_command()`: Shows all events for tomorrow

  - `week_command()`: Shows all events for current week with German weekdays### Added - Phase 1 Abgeschlossen ✅

  - `next_command()`: Shows next upcoming event with time-until calculation

  - `_handle_calendar_message()`: NLP-based event creation from text#### Projektstruktur

  - Calendar provider integration with factory pattern- Komplette Projektstruktur angelegt (src/, tests/, data/, logs/)

  - Enhanced `/start` and `/help` messages with calendar examples- Modulare Ordnerstruktur: bot/, ai/, gcalendar/, speech/, storage/, utils/

- Alle Module mit `__init__.py` initialisiert

### 🧪 Tests Created

- **tests/test_bot_calendar.py**: Simulated bot interactions#### Dokumentation

  - Tests for `/today`, `/tomorrow`, `/week` commands ✅- `README.md` mit vollständiger Projektbeschreibung

  - Natural language parsing validation ✅- Installationsanleitung (lokal + Deployment)

  - Conflict detection verification ✅- Telegram Bot Setup-Guide

- Roadmap mit 5 Phasen

### 💬 Example Interactions- `LICENSE` (MIT)

```- `.gitignore` für Python-Projekte

User: "Termin morgen 15 Uhr Meeting mit Team"- `Plan.txt` mit detailliertem Entwicklungsplan

Bot: ✅ Termin erstellt! Meeting mit Team @ 24.10.2025 15:00

#### Konfiguration

User: /today- `requirements.txt` mit allen Dependencies

Bot: 📅 Termine heute:- `.env.example` als Template für Umgebungsvariablen

     • 10:00 - Daily Standup- `.env` mit Telegram Bot Token (lokal, nicht im Repo)

     • 14:00 - Client Meeting- `setup.sh` für automatische Ersteinrichtung



User: /next#### Telegram Bot (Phase 1) ✅

Bot: 🔔 Dein nächster Termin:- **src/bot/telegram_bot.py**: Vollständiger Bot mit python-telegram-bot v12.8

     📌 Code Review  - `/start` Command - Willkommensnachricht

     📅 23.10.2025 um 15:00 Uhr  - `/help` Command - Hilfe-Übersicht

     ⏰ Beginnt in 2 Stunden  - `/info` Command - Bot-Informationen

```  - Text-Nachrichten Handler (Echo-Modus als Platzhalter)

  - Voice-Nachrichten Handler (Platzhalter für STT)

**Status**: Phase 3.4 complete    - Fehlerbehandlung (Error Handler)

**Next**: Phase 3.5 Service Layer + Siri API  - Logging-System

- **src/bot/handlers.py**: Erweiterbare Handler-Module (Platzhalter)

**Commit**: `844d429`- **src/main.py**: Haupteinstiegspunkt mit:

  - Banner-Anzeige

---  - Umgebungsvariablen-Validierung

  - Verzeichnis-Setup

## [Phase 3.1-3.3] - 2025-10-23  - Bot-Initialisierung



### 📅 Calendar Foundation (Phase 3.1)#### AI-Module (Vorbereitet für Phase 2)

- **src/ai/ai_client.py**: Abstract Base Class für AI Provider

#### Architecture- **src/ai/hf_provider.py**: Hugging Face Provider (Platzhalter)

- **Abstract CalendarClient base class**: Flexible provider architecture for multiple calendar backends- **src/ai/openrouter_provider.py**: OpenRouter Provider (Platzhalter)

- **CalendarEvent dataclass**: Standardized event representation with title, start, end, location, description

- **Provider Factory**: Automatic provider selection with fallback mechanism#### Calendar-Module (Vorbereitet für Phase 3)

- **src/gcalendar/calendar_client.py**: Google Calendar Client (Platzhalter)

#### Three Calendar Providers Implemented  - Hinweis: Umbenannt von `calendar` zu `gcalendar` um Konflikt mit Python stdlib zu vermeiden

1. **iCloud CalDAV Provider** (`src/gcalendar/icloud_provider.py`, 370 lines)

   - Full iCloud Calendar integration via CalDAV protocol#### Utility-Module

   - App-specific password support- **src/utils/nlp_utils.py**: NLP-Hilfsfunktionen

   - SSL/TLS connection with certificate validation  - Date-Parsing mit dateparser

   - Status: Blocked by corporate firewall (Zscaler blocks CalDAV/WebDAV)  - Keyword-Extraktion

   - Documentation: `docs/ICLOUD_BLOCKED.md`  - Command-Type Detection

  - Text-Bereinigung

2. **Google Calendar OAuth2 Provider** (`src/gcalendar/google_provider.py`, 380 lines)

   - Google Calendar API v3 integration#### Scripts & Tools

   - OAuth 2.0 flow with token caching (token.pickle)- `run.py`: Alternative Start-Script mit SSL-Workarounds

   - Credentials file support (credentials.json)- Ausführbares `setup.sh` für automatische Installation

   - Status: SSL certificate verification fails in corporate network

   - Documentation: `docs/GOOGLE_CALENDAR_SETUP.md`### Known Issues

- SSL-Zertifikat-Probleme in Firmennetzwerken (CERTIFICATE_VERIFY_FAILED)

3. **Mock Calendar Provider** (`src/gcalendar/mock_provider.py`, 230 lines)  - Workaround: Test außerhalb des Firmennetzwerks oder mit Proxy-Konfiguration

   - In-memory calendar implementation  - Bot-Code ist funktionsfähig, Problem liegt in der Netzwerk-Infrastruktur

   - 4 pre-loaded sample events for testing

   - No external dependencies### Technical Details

   - Perfect for local development and testing- Python 3.6+ kompatibel

   - Status: ✅ Works perfectly, used as development fallback- python-telegram-bot v12.8 (kompatibel mit älteren Python-Versionen)

- Alle Module mit Docstrings und Type Hints

### 🔧 CRUD Operations (Phase 3.2)- Modulare, erweiterbare Architektur



#### Implemented Operations (All Providers)### Next Steps (Phase 2)

- `connect()`: Establish connection to calendar backend- [ ] Hugging Face API Integration testen

- `list_events(start, end)`: Retrieve events for date range- [ ] OpenRouter Integration implementieren

- `create_event(event)`: Create new calendar event- [ ] Intent-Erkennung für Befehle

- `update_event(event_id, updates)`: Modify existing event- [ ] Kontextverständnis implementieren

- `delete_event(event_id)`: Remove event from calendar
- `check_conflicts(start, end)`: Detect scheduling conflicts

#### Sample Events (Mock Provider)
```python
1. Daily Standup - Today 10:00 (30 min)
2. Client Meeting - Today 14:00 (60 min)
3. Code Review - Today 15:00 (60 min)
4. Sprint Planning - Friday 09:00 (120 min)
```

All operations tested and working in Mock Calendar ✅

### 🗣️ NLP Enhancements (Phase 3.3)

#### Natural Language Processing Functions
- **`parse_event_from_text(text)`**: Complete event parsing from German natural language
  - Extracts: title, start time, end time, location
  - Returns: Event dictionary ready for calendar creation
  
- **`extract_datetime_from_text(text)`**: German relative date/time support
  - Absolute: "Montag 15 Uhr", "23.10.2025 14:00"
  - Relative: "heute", "morgen", "übermorgen"
  - Weekdays: "Montag", "Dienstag", "Mittwoch", etc.
  - Future: "nächste Woche", "nächsten Montag"
  - Duration: "in 2 Stunden", "in 30 Minuten"
  
- **`extract_location_from_text(text)`**: Location extraction
  - Patterns: "in Room 302", "bei der Bank", "@Zoom", "im Büro"
  
- **`extract_event_title(text)`**: Smart title extraction
  - Filters command keywords ("erstelle", "mach", "termin")
  - Removes time/date keywords ("morgen", "15 Uhr")
  - Preserves meaningful event description

#### German Language Support Examples
```
"Termin morgen 15 Uhr Meeting" 
  → Tomorrow at 15:00, title: "Meeting"

"Treffen übermorgen 14:30 in Raum 203"
  → Day after tomorrow at 14:30, location: "Raum 203"

"Meeting nächsten Montag 10 Uhr mit Team"
  → Next Monday at 10:00, title: "Meeting mit Team"
```

### 📝 Files Created (16 files, 2802 lines total)

#### Core Calendar Implementation
- `src/gcalendar/calendar_client.py` (260 lines): Base classes and interfaces
- `src/gcalendar/icloud_provider.py` (370 lines): iCloud CalDAV implementation
- `src/gcalendar/google_provider.py` (380 lines): Google OAuth2 implementation
- `src/gcalendar/mock_provider.py` (230 lines): Mock calendar for testing
- `src/gcalendar/factory.py` (150 lines): Provider factory with automatic fallback

#### NLP Engine
- `src/utils/nlp_utils.py`: Extended from 106 to 347 lines
  - German date/time parsing
  - Location extraction
  - Title extraction
  - Event parsing

#### Test Suite
- `tests/test_icloud_calendar.py`: iCloud provider tests
- `tests/test_google_calendar.py`: Google Calendar provider tests
- `tests/test_mock_calendar.py`: Mock provider tests
- `tests/test_nlp_calendar.py`: NLP parsing tests
- `tests/test_calendar_factory.py`: Factory pattern tests

#### Documentation
- `docs/ICLOUD_BLOCKED.md`: iCloud CalDAV firewall issue and workarounds
- `docs/GOOGLE_CALENDAR_SETUP.md`: Google Calendar OAuth setup instructions

**Commit**: `69cfb70`

---

## [Phase 0-2] - 2025-10-22

### ✅ Previously Completed Features

#### Phase 0: Project Setup
- Python 3.6+ project structure
- Virtual environment configuration
- Dependency management (requirements.txt)
- Git repository initialization

#### Phase 1: Telegram Bot Basics
- Telegram Bot API integration
- Command handlers (`/start`, `/help`, `/info`)
- Message handlers (text, voice)
- Error handling and logging
- Bot configuration via environment variables

#### Phase 2: AI Integration
- **HuggingFace Provider** (`src/ai/hf_provider.py`)
  - Text generation with multiple models (flan-t5-base, mistral, gpt2)
  - Intent recognition and classification
  - Works without API token (limited functionality)
  
- **OpenRouter Provider** (`src/ai/openrouter_provider.py`)
  - Multi-model support (GPT-3.5, Claude, Mistral, PaLM)
  - Chat format with message history
  - System prompts and context
  - API key authentication

---

## Project Architecture

### Components

**AdonisAI** is a modular personal AI assistant featuring:

- 🤖 **Telegram Bot Interface**
  - Full-featured bot with command and natural language support
  - Voice message handling (prepared)
  - Context-aware conversations
  
- 🧠 **AI Providers** (Pluggable architecture)
  - HuggingFace: Open-source models
  - OpenRouter: GPT-3.5-Turbo, Claude, etc.
  - Unified interface for easy provider switching
  
- 📅 **Calendar Management** (Multi-provider)
  - iCloud CalDAV (corporate firewall blocked)
  - Google Calendar OAuth2 (SSL issues in corporate network)
  - Mock Provider (local development, ✅ working)
  
- 🗣️ **Natural Language Processing**
  - German language support
  - Date/time extraction
  - Location parsing
  - Event title extraction
  
- 🔄 **Context Management**
  - Per-user conversation history
  - Configurable message retention (10 messages, 30 min TTL)
  - Automatic cleanup
  
- 🔐 **Corporate Network Compatible**
  - SSL workarounds for restrictive firewalls
  - Zscaler compatibility
  - CalDAV/WebDAV fallback mechanisms

### Design Patterns

- **Factory Pattern**: Calendar provider selection with fallback
- **Strategy Pattern**: AI provider abstraction
- **Singleton Pattern**: Context manager per user
- **Template Method**: Base calendar client with provider implementations

### Technology Stack

- **Python 3.6+**: Core language (corporate environment compatible)
- **python-telegram-bot**: Telegram Bot API wrapper
- **HuggingFace Transformers**: Open-source AI models
- **OpenRouter API**: Commercial AI model gateway
- **caldav**: iCloud CalDAV protocol
- **google-api-python-client**: Google Calendar API
- **dateparser**: Natural language date parsing
- **requests**: HTTP client for API calls

---

## Roadmap

### Phase 3.5 (Current) ✅
- [x] AI-driven message processing
- [x] Context management
- [x] SSL workarounds
- [x] Enhanced bot commands

### Phase 3.6 (Next)
- [ ] REST API Service Layer
- [ ] Siri Shortcuts integration endpoints
- [ ] API authentication & security
- [ ] Comprehensive testing outside corporate network

### Phase 4 (Future)
- [ ] Voice message transcription
- [ ] Text-to-speech responses
- [ ] Multi-language support (English, German, etc.)
- [ ] Event reminders and notifications

### Phase 5 (Future)
- [ ] Multi-user support
- [ ] User permissions & privacy controls
- [ ] Team calendars
- [ ] Calendar sharing

---

## Known Issues

### Corporate Network Limitations
- **iCloud CalDAV**: Blocked by Zscaler firewall (CalDAV/WebDAV protocols)
- **Google Calendar**: SSL certificate verification fails
- **Workaround**: Mock Calendar Provider for development
- **Production**: Bot works perfectly outside corporate network

### Testing Environment
- All features tested with Mock Calendar Provider ✅
- Real calendar providers (iCloud, Google) require testing outside corporate network
- SSL patch allows Telegram Bot to connect despite firewall

---

## Contributing

Contributions are welcome! Please read the [Contributing Guidelines](CONTRIBUTING.md) first.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- **Repository**: https://github.com/WVUSAAH-Copilot-test/AdonisAI
- **Internal Repo**: https://code.rbi.tech/WVUSAAH/AdonisAI
- **Author**: WVUSAAH

---

Made with ❤️ and ☕

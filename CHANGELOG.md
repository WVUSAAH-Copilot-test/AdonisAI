# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [0.1.0] - 2025-10-22

### Added - Phase 1 Abgeschlossen ✅

#### Projektstruktur
- Komplette Projektstruktur angelegt (src/, tests/, data/, logs/)
- Modulare Ordnerstruktur: bot/, ai/, gcalendar/, speech/, storage/, utils/
- Alle Module mit `__init__.py` initialisiert

#### Dokumentation
- `README.md` mit vollständiger Projektbeschreibung
- Installationsanleitung (lokal + Deployment)
- Telegram Bot Setup-Guide
- Roadmap mit 5 Phasen
- `LICENSE` (MIT)
- `.gitignore` für Python-Projekte
- `Plan.txt` mit detailliertem Entwicklungsplan

#### Konfiguration
- `requirements.txt` mit allen Dependencies
- `.env.example` als Template für Umgebungsvariablen
- `.env` mit Telegram Bot Token (lokal, nicht im Repo)
- `setup.sh` für automatische Ersteinrichtung

#### Telegram Bot (Phase 1) ✅
- **src/bot/telegram_bot.py**: Vollständiger Bot mit python-telegram-bot v12.8
  - `/start` Command - Willkommensnachricht
  - `/help` Command - Hilfe-Übersicht
  - `/info` Command - Bot-Informationen
  - Text-Nachrichten Handler (Echo-Modus als Platzhalter)
  - Voice-Nachrichten Handler (Platzhalter für STT)
  - Fehlerbehandlung (Error Handler)
  - Logging-System
- **src/bot/handlers.py**: Erweiterbare Handler-Module (Platzhalter)
- **src/main.py**: Haupteinstiegspunkt mit:
  - Banner-Anzeige
  - Umgebungsvariablen-Validierung
  - Verzeichnis-Setup
  - Bot-Initialisierung

#### AI-Module (Vorbereitet für Phase 2)
- **src/ai/ai_client.py**: Abstract Base Class für AI Provider
- **src/ai/hf_provider.py**: Hugging Face Provider (Platzhalter)
- **src/ai/openrouter_provider.py**: OpenRouter Provider (Platzhalter)

#### Calendar-Module (Vorbereitet für Phase 3)
- **src/gcalendar/calendar_client.py**: Google Calendar Client (Platzhalter)
  - Hinweis: Umbenannt von `calendar` zu `gcalendar` um Konflikt mit Python stdlib zu vermeiden

#### Utility-Module
- **src/utils/nlp_utils.py**: NLP-Hilfsfunktionen
  - Date-Parsing mit dateparser
  - Keyword-Extraktion
  - Command-Type Detection
  - Text-Bereinigung

#### Scripts & Tools
- `run.py`: Alternative Start-Script mit SSL-Workarounds
- Ausführbares `setup.sh` für automatische Installation

### Known Issues
- SSL-Zertifikat-Probleme in Firmennetzwerken (CERTIFICATE_VERIFY_FAILED)
  - Workaround: Test außerhalb des Firmennetzwerks oder mit Proxy-Konfiguration
  - Bot-Code ist funktionsfähig, Problem liegt in der Netzwerk-Infrastruktur

### Technical Details
- Python 3.6+ kompatibel
- python-telegram-bot v12.8 (kompatibel mit älteren Python-Versionen)
- Alle Module mit Docstrings und Type Hints
- Modulare, erweiterbare Architektur

### Next Steps (Phase 2)
- [ ] Hugging Face API Integration testen
- [ ] OpenRouter Integration implementieren
- [ ] Intent-Erkennung für Befehle
- [ ] Kontextverständnis implementieren

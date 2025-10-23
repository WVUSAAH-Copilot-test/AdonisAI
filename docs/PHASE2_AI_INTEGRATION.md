# Phase 2: LLM-Integration 🤖

## Übersicht

Phase 2 implementiert die KI-Integration in AdonisAI. Der Bot kann jetzt mit echten AI-Modellen kommunizieren und intelligente Antworten generieren.

## Features ✨

### AI Provider
- **Hugging Face Provider** - Kostenfreie Inference API
  - Modelle: flan-t5-base, mistral-7b, gpt2
  - Funktioniert ohne API-Token (limitiert)
  - Empfohlen für Start

- **OpenRouter Provider** - Gateway zu verschiedenen Modellen
  - Modelle: GPT-3.5, Claude, PaLM, Mistral
  - Benötigt API-Key
  - Bessere Qualität, mehr Optionen

### Funktionen
- ✅ Intelligente Antwort-Generierung
- ✅ Intent-Erkennung (calendar, reminder, question, general)
- ✅ Kontext-aware Responses
- ✅ Fehlerbehandlung & Fallbacks
- ✅ SSL-Workarounds für Firmennetzwerke

## Installation

### 1. API-Keys besorgen

#### Hugging Face (empfohlen für Start)
1. Gehe zu https://huggingface.co/
2. Erstelle einen kostenlosen Account
3. Gehe zu Settings → Access Tokens
4. Erstelle ein neues Token (read)
5. Füge in `.env` ein: `HF_API_TOKEN=hf_...`

#### OpenRouter (optional)
1. Gehe zu https://openrouter.ai/
2. Erstelle Account
3. Hole API Key
4. Füge in `.env` ein: `OPENROUTER_API_KEY=sk-or-...`

### 2. Konfiguration

Bearbeite `.env`:

```bash
# Wähle Provider
AI_PROVIDER=huggingface  # oder "openrouter"

# Hugging Face Settings
HF_API_TOKEN=hf_your_token_here
AI_MODEL=flan-t5-base    # schnell und zuverlässig

# OpenRouter Settings (optional)
OPENROUTER_API_KEY=sk-or-your_key_here
OPENROUTER_MODEL=gpt-3.5
```

### 3. Dependencies installieren

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Verwendung

### Bot starten

```bash
# Mit AI
python src/main.py

# Oder ohne AI (Echo-Modus)
python src/main.py --no-ai
```

### AI Provider testen

```bash
# Teste Hugging Face
python tests/test_ai_providers.py

# Oder direkt
source venv/bin/activate
python tests/test_ai_providers.py
```

### Beispiel-Konversation

```
User: Hallo, wer bist du?
Bot: Ich bin AdonisAI, dein persönlicher KI-Assistent. Ich kann...

User: Was ist die Hauptstadt von Deutschland?
Bot: Die Hauptstadt von Deutschland ist Berlin.

User: Erstelle einen Termin für morgen um 15 Uhr
Bot: 📅 Kalender-Anfrage erkannt
     [AI-Antwort]
     Hinweis: Kalender-Integration kommt in Phase 3
```

## Verfügbare Modelle

### Hugging Face

| Modell | Typ | Geschwindigkeit | Qualität | Empfehlung |
|--------|-----|----------------|----------|------------|
| **flan-t5-base** | text2text | ⚡⚡⚡ Sehr schnell | ⭐⭐⭐ Gut | ✅ **Empfohlen** |
| mistral-7b | text-gen | ⚡⚡ Mittel | ⭐⭐⭐⭐ Sehr gut | Für längere Antworten |
| gpt2 | text-gen | ⚡⚡⚡ Sehr schnell | ⭐⭐ OK | Fallback |

### OpenRouter

| Modell | Provider | Kosten | Qualität |
|--------|----------|--------|----------|
| gpt-3.5 | OpenAI | Free Tier | ⭐⭐⭐⭐ |
| claude | Anthropic | Free Tier | ⭐⭐⭐⭐⭐ |
| mistral | Mistral AI | Free | ⭐⭐⭐⭐ |

## API Limits

### Hugging Face (ohne Token)
- ~30 Requests/Stunde
- Kann "Model Loading" dauern (1-2 Min beim ersten Request)

### Hugging Face (mit Token)
- ~1000 Requests/Stunde (Free Tier)
- Schnellerer Model-Load

### OpenRouter
- Varies by model
- Check: https://openrouter.ai/docs

## Troubleshooting

### "Model is currently loading"
```python
# Warte 1-2 Minuten und versuche erneut
# HF muss Modell erst laden bei erstem Request
```

### "API Token fehlt"
```bash
# Setze in .env:
HF_API_TOKEN=hf_your_token_here
```

### SSL-Fehler
```bash
# Siehe docs/SSL_PROBLEM.md
# TL;DR: Teste außerhalb Firmennetzwerk
```

### AI antwortet nicht
```python
# Check Logs für Fehler:
# - API Rate Limit?
# - Token gültig?
# - Netzwerk-Verbindung OK?
```

## Architektur

```
User Input
    ↓
Telegram Bot
    ↓
detect_command_type() ← NLP Utils
    ↓
AI Provider (HF oder OpenRouter)
    ↓
generate_response()
    ↓
Intent Detection (optional)
    ↓
Response to User
```

## Code-Beispiele

### Provider direkt verwenden

```python
from src.ai.hf_provider import HuggingFaceProvider
import asyncio

async def test():
    hf = HuggingFaceProvider()
    response = await hf.generate_response("Was ist Python?")
    print(response)

asyncio.run(test())
```

### Mit Kontext

```python
context = {
    'max_length': 200,
    'temperature': 0.7
}
response = await provider.generate_response(
    "Erkläre Machine Learning",
    context=context
)
```

### Intent-Analyse

```python
result = await provider.analyze_intent(
    "Erstelle einen Termin für morgen"
)
# → {'intent': 'calendar', 'confidence': 0.8, ...}
```

## Nächste Schritte (Phase 3)

- [ ] Google Calendar Integration
- [ ] Termine erstellen via Natural Language
- [ ] Intent → Action Mapping
- [ ] Context-Storage (Session-Memory)

## Links

- **Hugging Face Docs:** https://huggingface.co/docs/api-inference/
- **OpenRouter Docs:** https://openrouter.ai/docs
- **Supported Models:** https://huggingface.co/models
- **Project Repo:** https://github.com/WVUSAAH-Copilot-test/AdonisAI

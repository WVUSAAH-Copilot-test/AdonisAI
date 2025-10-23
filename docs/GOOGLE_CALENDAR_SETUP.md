# Google Calendar Setup - Funktioniert im Corporate Network! ✅

## Warum Google Calendar statt iCloud?

- ✅ **Funktioniert im Corporate Network** (Zscaler blockiert iCloud CalDAV)
- ✅ OAuth2-Authentifizierung (sicherer als App-Passwörter)
- ✅ Bessere API-Dokumentation
- ✅ Mehr Features (Farben, Notifications, Sharing)

## Setup in 3 Schritten

### 1. Google Cloud Projekt erstellen

1. Gehe zu: https://console.cloud.google.com/
2. Klicke auf **"Neues Projekt"** (oder wähle existierendes)
3. Projektname: **"AdonisAI"**

### 2. Calendar API aktivieren

1. Im Projekt-Dashboard: **APIs & Services** → **Bibliothek**
2. Suche nach: **"Google Calendar API"**
3. Klicke auf **"Aktivieren"**

### 3. OAuth2 Credentials erstellen

1. **APIs & Services** → **Anmeldedaten** (Credentials)
2. Klicke **"+ ANMELDEDATEN ERSTELLEN"**
3. Wähle **"OAuth-Client-ID"**
4. Falls gefragt: OAuth-Zustimmungsbildschirm konfigurieren
   - User Type: **Extern**
   - App-Name: **AdonisAI**
   - User-Support-E-Mail: **ahmadzai.sahel18@gmail.com**
   - Scopes: Keine hinzufügen (wir nutzen nur Calendar)
   - Test-Nutzer: **ahmadzai.sahel18@gmail.com** hinzufügen
   - Speichern
5. Zurück zu **Anmeldedaten erstellen**:
   - Anwendungstyp: **Desktop-App**
   - Name: **AdonisAI Desktop Client**
   - Erstellen
6. **Download JSON** → Speichern als `credentials.json` im Projekt-Root

```bash
cd /home/wvusaah/Work/AdonisAI
# credentials.json hier ablegen
```

### 4. Test ausführen

```bash
cd /home/wvusaah/Work/AdonisAI
source venv/bin/activate
python tests/test_google_calendar.py
```

**Was passiert:**
1. Browser öffnet sich automatisch
2. Google Login-Seite erscheint
3. Nach Login: Berechtigung für Calendar-Zugriff erteilen
4. Token wird in `token.pickle` gespeichert
5. Zukünftig keine Login-Aufforderung mehr (Token wird wiederverwendet)

## .env Konfiguration

```bash
# Calendar Provider (google oder icloud)
CALENDAR_PROVIDER=google

# Google Calendar (optional - defaults funktionieren)
GOOGLE_CREDENTIALS_FILE=./credentials.json
GOOGLE_TOKEN_FILE=./token.pickle
```

## Vorteile gegenüber iCloud

| Feature | Google Calendar | iCloud CalDAV |
|---------|----------------|---------------|
| Corporate Network | ✅ Funktioniert | ❌ Blockiert |
| Authentifizierung | OAuth2 (sicher) | App-Passwort |
| API-Qualität | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Recurring Events | ✅ Nativ | Via recurring-ical-events |
| Event-Farben | ✅ | ❌ |
| Notifications | ✅ | ❌ |
| Sharing | ✅ | Limited |

## Troubleshooting

### "credentials.json nicht gefunden"
→ Stelle sicher dass credentials.json im Projekt-Root liegt

### "Access blocked: AdonisAI hasn't completed verification"
→ Normal für neue Apps! Klicke auf **"Erweitert"** → **"Zu AdonisAI wechseln (unsicher)"**
→ Dies ist deine eigene App, daher sicher!

### Browser öffnet nicht
→ Terminal zeigt URL an - manuell im Browser öffnen

### "Calendar API not enabled"
→ Stelle sicher dass Calendar API im Google Cloud Projekt aktiviert ist

## Code-Integration

```python
from src.gcalendar.google_provider import GoogleCalendarProvider

# Provider erstellen
provider = GoogleCalendarProvider()

# Verbinden (öffnet Browser beim ersten Mal)
provider.connect()

# Events abrufen
from datetime import datetime, timedelta
events = provider.list_events(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=7)
)

# Event erstellen
event = provider.create_event(
    title="Meeting mit Team",
    start=datetime(2025, 10, 24, 15, 0),
    end=datetime(2025, 10, 24, 16, 0),
    location="Conference Room A",
    description="Wöchentliches Team-Sync"
)
```

## Nächste Schritte

Nach erfolgreichem Test:
1. ✅ Phase 3.1-3.2 abgeschlossen (Google statt iCloud)
2. → Phase 3.3: NLP Enhancements
3. → Phase 3.4: Bot Integration
4. → Phase 3.5: Service Layer + Siri API

---

**Fazit:** Google Calendar ist die bessere Wahl für Corporate Networks!

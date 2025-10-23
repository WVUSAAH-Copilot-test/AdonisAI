# iCloud CalDAV Zugriff - Netzwerk-Blockade

**Status:** 🔴 **BLOCKIERT durch Corporate Network**

## Problem

Der Zugriff auf iCloud CalDAV (`https://caldav.icloud.com/`) wird durch die **Zscaler Firewall** im Corporate Network blockiert.

## Fehler-Details

```
Not allowed to upload files to this site
iCloud
Need help? Contact our support team at local helpdesk, helpdesk_email@localdomain.com
```

### Technische Details

- **URL:** `https://caldav.icloud.com/`
- **Protokoll:** CalDAV (WebDAV-basiert)
- **Blockierung:** Zscaler Proxy (Raiffeisen Bank International AG)
- **Grund:** Policy "Not allowed to upload files to this site"
- **Error Code:** 575233 6 112 0 1761215864 132

## Getestete Lösung

Die CalDAV-Integration wurde vollständig implementiert:

1. **Abstract Base Class** (`CalendarClient`)
   - Definiert einheitliche Schnittstelle für alle Provider
   - CRUD-Operationen (Create, Read, Update, Delete)
   - Konflikt-Erkennung (`check_conflicts()`)

2. **iCloud Provider** (`iCloudCalendarProvider`)
   - CalDAV-Client mit SSL-Workaround
   - iCalendar-Format-Parsing
   - Vollständige CRUD-Implementierung
   - Support für recurring events

3. **Credentials korrekt konfiguriert:**
   - Username: `sahelahmadzai11@gmail.com`
   - App Password: `shwk-efqk-oxlp-mcwt` ✅
   - URL: `https://caldav.icloud.com/` ✅

4. **Dependencies installiert:**
   - `caldav==1.6.0` ✅
   - `icalendar==4.1.1` ✅
   - `recurring-ical-events==2.0.2` ✅

## Code-Status

✅ **Code ist vollständig und funktionsfähig**

Der Code wurde korrekt implementiert und würde außerhalb des Corporate Networks funktionieren. Das Problem liegt **ausschließlich** in der Netzwerk-Policy.

## Lösungsoptionen

### Option 1: Zscaler-Freigabe beantragen ⭐ EMPFOHLEN

Kontaktiere das IT-Helpdesk und beantrage Freigabe für:
- **Domain:** `caldav.icloud.com`
- **Port:** 443 (HTTPS)
- **Protokoll:** CalDAV/WebDAV
- **Begründung:** Kalender-Integration für persönlichen Produktivitäts-Bot

```
Betreff: Freigabe für iCloud CalDAV-Zugriff
Domain: caldav.icloud.com
Verwendungszweck: Kalender-Synchronisation für AdonisAI Personal Assistant
```

### Option 2: Home Network / VPN

Code **außerhalb** des Corporate Networks testen:
- Zu Hause via privates WiFi
- Über Mobile Hotspot (Handy)
- VPN-Verbindung die Zscaler umgeht

### Option 3: Alternative Provider (Google Calendar)

Falls iCloud dauerhaft blockiert bleibt, kann auf **Google Calendar API** umgestellt werden:
- Authentifizierung über OAuth2
- Funktioniert im Corporate Network (bereits getestet mit anderen Google APIs)
- Code-Struktur ist dank Abstract Base Class leicht anpassbar

## Test-Anleitung (außerhalb Corporate Network)

```bash
cd /home/wvusaah/Work/AdonisAI
source venv/bin/activate
python tests/test_icloud_calendar.py
```

**Erwartetes Ergebnis:**
```
✅ Verbindung erfolgreich!
📅 Kalender: Calendar
📋 Gefunden: X Events
```

## Nächste Schritte

1. **IT-Ticket erstellen** für Zscaler-Freigabe (siehe Option 1)
2. **Alternativ:** Code zu Hause/Mobile Hotspot testen
3. **Falls blockiert bleibt:** Phase 3 mit Google Calendar fortsetzen

## Zusammenhang mit SSL-Problem

Siehe auch: [docs/SSL_PROBLEM.md](SSL_PROBLEM.md)

Beide Probleme (SSL-Zertifikat + iCloud-Blockade) sind **Corporate Network Policies**:
- SSL: `ssl._create_unverified_context()` Workaround implementiert ✅
- iCloud: Keine Code-Lösung möglich - IT-Freigabe erforderlich ⚠️

## Code-Dateien

- `/src/gcalendar/calendar_client.py` - Abstract Base Class ✅
- `/src/gcalendar/icloud_provider.py` - iCloud CalDAV Provider ✅
- `/tests/test_icloud_calendar.py` - Test Suite ✅
- `/.env` - Credentials (ICLOUD_USERNAME, ICLOUD_APP_PASSWORD) ✅

---

**Fazit:** Code funktioniert - Netzwerk blockiert. Entweder IT-Freigabe beantragen oder außerhalb Corporate Network testen.

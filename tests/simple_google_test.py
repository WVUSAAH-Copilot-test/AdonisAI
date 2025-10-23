"""
Einfacher Google Calendar Verbindungstest
Zeigt die OAuth-URL an - im Browser öffnen und authorisieren
"""

import os
import sys
from dotenv import load_dotenv

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from src.gcalendar.google_provider import GoogleCalendarProvider

print("🚀 Google Calendar OAuth Test")
print("=" * 60)
print("\n1️⃣ Browser-Fenster öffnet sich (oder URL wird angezeigt)")
print("2️⃣ Mit ahmadzai.sahel18@gmail.com einloggen")
print("3️⃣ Calendar-Zugriff erlauben")
print("4️⃣ Token wird gespeichert für zukünftige Nutzung\n")
print("=" * 60)

provider = GoogleCalendarProvider()

print("\n⏳ Starte OAuth-Flow...\n")

if provider.connect():
    print("\n✅ Erfolgreich verbunden!")
    print("🎉 Google Calendar ist jetzt einsatzbereit!")
    
    # Zeige kommende Events
    from datetime import datetime, timedelta
    
    print("\n📅 Teste Events abrufen...")
    events = provider.list_events(
        datetime.now(),
        datetime.now() + timedelta(days=7)
    )
    
    print(f"📋 {len(events)} Events in den nächsten 7 Tagen gefunden")
    
    if events:
        print("\n📌 Beispiel-Events:")
        for event in events[:3]:
            print(f"  • {event.title} ({event.start.strftime('%d.%m %H:%M')})")
    
else:
    print("\n❌ Verbindung fehlgeschlagen")
    print("💡 Prüfe ob credentials.json vorhanden ist")
    print("💡 Stelle sicher dass ahmadzai.sahel18@gmail.com als Testnutzer eingetragen ist")

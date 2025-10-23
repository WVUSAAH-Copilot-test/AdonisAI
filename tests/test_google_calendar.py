"""
Test für Google Calendar Provider (funktioniert im Corporate Network!)
"""

import os
import sys
import ssl
from datetime import datetime, timedelta
from dotenv import load_dotenv

# SSL Fix für Corporate Network
ssl._create_default_https_context = ssl._create_unverified_context

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# .env laden
load_dotenv()

from src.gcalendar.google_provider import GoogleCalendarProvider


def test_connection():
    """Test: Verbindung zu Google Calendar"""
    print("=" * 60)
    print("🧪 Test: Google Calendar OAuth2 Verbindung")
    print("=" * 60)
    
    provider = GoogleCalendarProvider()
    
    print(f"\n📁 Credentials: {provider.credentials_file}")
    print(f"🔐 Token: {provider.token_file}")
    
    print("\n⏳ Verbinde zu Google Calendar...")
    print("💡 Falls Browser öffnet: Login mit Google Account")
    
    success = provider.connect()
    
    if success:
        print(f"✅ Verbindung erfolgreich!")
        return provider
    else:
        print(f"❌ Verbindung fehlgeschlagen")
        print("\n💡 Setup-Anleitung:")
        print("   1. Gehe zu: https://console.cloud.google.com/apis/credentials")
        print("   2. Erstelle OAuth 2.0 Client ID (Desktop App)")
        print("   3. Download als 'credentials.json' im Projekt-Root")
        return None


def test_list_events(provider):
    """Test: Events auflisten"""
    if not provider:
        print("\n⚠️ Überspringe Test - keine Verbindung")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Test: Events auflisten")
    print("=" * 60)
    
    # Nächste 7 Tage
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    
    print(f"\n📅 Zeitraum: {start_date.date()} - {end_date.date()}")
    print("⏳ Lade Events...")
    
    events = provider.list_events(start_date, end_date)
    
    print(f"\n📋 Gefunden: {len(events)} Events")
    
    for i, event in enumerate(events, 1):
        print(f"\n{i}. {event.title}")
        print(f"   📅 {event.start.strftime('%Y-%m-%d %H:%M')} - {event.end.strftime('%H:%M')}")
        if event.location:
            print(f"   📍 {event.location}")
        if event.description:
            desc = event.description[:50]
            print(f"   📝 {desc}...")
        print(f"   🆔 {event.uid}")


def test_create_event(provider):
    """Test: Event erstellen"""
    if not provider:
        print("\n⚠️ Überspringe Test - keine Verbindung")
        return None
    
    print("\n" + "=" * 60)
    print("🧪 Test: Event erstellen")
    print("=" * 60)
    
    # Test-Event morgen um 15:00
    start = datetime.now().replace(hour=15, minute=0, second=0, microsecond=0) + timedelta(days=1)
    end = start + timedelta(hours=1)
    
    print(f"\n📝 Erstelle Test-Event:")
    print(f"   Titel: AdonisAI Google Calendar Test")
    print(f"   Start: {start}")
    print(f"   Ende: {end}")
    
    try:
        event = provider.create_event(
            title="AdonisAI Google Calendar Test",
            start=start,
            end=end,
            description="Automatisch erstellt von AdonisAI Test Suite (Google Calendar)",
            location="Corporate Network Test"
        )
        
        print(f"\n✅ Event erstellt!")
        print(f"   🆔 UID: {event.uid}")
        return event
        
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        return None


def test_check_conflicts(provider):
    """Test: Konflikt-Erkennung"""
    if not provider:
        print("\n⚠️ Überspringe Test - keine Verbindung")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Test: Konflikt-Erkennung")
    print("=" * 60)
    
    # Morgen 15:00 - 16:00
    start = datetime.now().replace(hour=15, minute=0, second=0, microsecond=0) + timedelta(days=1)
    end = start + timedelta(hours=1)
    
    print(f"\n⏳ Prüfe Zeitraum: {start} - {end}")
    
    result = provider.check_conflicts(start, end)
    
    if result['has_conflict']:
        print(f"\n⚠️ {result['count']} Konflikt(e) gefunden:")
        for conflict in result['conflicts']:
            print(f"   - {conflict.title} ({conflict.start.strftime('%H:%M')} - {conflict.end.strftime('%H:%M')})")
    else:
        print(f"\n✅ Keine Konflikte - Zeitraum ist frei")


def main():
    """Führt alle Tests aus"""
    print("\n🚀 AdonisAI Google Calendar Tests")
    print("💡 Funktioniert IM Corporate Network!")
    print("=" * 60)
    
    # Test 1: Verbindung
    provider = test_connection()
    
    if not provider:
        print("\n❌ Verbindungstest fehlgeschlagen")
        print("\n💡 Mögliche Ursachen:")
        print("   - credentials.json fehlt")
        print("   - Google Cloud Projekt nicht eingerichtet")
        print("   - Calendar API nicht aktiviert")
        return
    
    # Test 2: Events auflisten
    test_list_events(provider)
    
    # Test 3: Event erstellen
    created_event = test_create_event(provider)
    
    # Test 4: Konflikte prüfen
    test_check_conflicts(provider)
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("✅ Tests abgeschlossen")
    print("=" * 60)
    
    if created_event:
        print(f"\n⚠️ Test-Event wurde erstellt:")
        print(f"   Titel: {created_event.title}")
        print(f"   UID: {created_event.uid}")
        print(f"\n💡 Bitte in Google Calendar überprüfen und ggf. löschen")
        print(f"   https://calendar.google.com")


if __name__ == "__main__":
    main()

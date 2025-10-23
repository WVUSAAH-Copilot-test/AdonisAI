"""
Test für iCloud Calendar Provider
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

from src.gcalendar.icloud_provider import iCloudCalendarProvider


def test_connection():
    """Test: Verbindung zu iCloud CalDAV"""
    print("=" * 60)
    print("🧪 Test: iCloud CalDAV Verbindung")
    print("=" * 60)
    
    provider = iCloudCalendarProvider()
    
    print(f"\n📧 Username: {provider.username}")
    print(f"🔐 Password: {'*' * len(provider.password) if provider.password else 'NICHT GESETZT'}")
    print(f"🌐 URL: {provider.calendar_url}")
    
    print("\n⏳ Verbinde zu iCloud...")
    success = provider.connect()
    
    if success:
        print(f"✅ Verbindung erfolgreich!")
        print(f"📅 Kalender: {provider.calendar.name}")
        return provider
    else:
        print(f"❌ Verbindung fehlgeschlagen")
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
            print(f"   📝 {event.description[:50]}...")
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
    print(f"   Titel: AdonisAI Test Event")
    print(f"   Start: {start}")
    print(f"   Ende: {end}")
    
    try:
        event = provider.create_event(
            title="AdonisAI Test Event",
            start=start,
            end=end,
            description="Automatisch erstellt von AdonisAI Test Suite",
            location="Virtuell"
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
    print("\n🚀 AdonisAI iCloud Calendar Tests")
    print("=" * 60)
    
    # Test 1: Verbindung
    provider = test_connection()
    
    if not provider:
        print("\n❌ Verbindungstest fehlgeschlagen - breche ab")
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
        print(f"\n💡 Bitte manuell in iCloud Calendar überprüfen und ggf. löschen")


if __name__ == "__main__":
    main()

"""
Test für Mock Calendar Provider - Funktioniert OHNE Internet!
"""

import os
import sys
from datetime import datetime, timedelta

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gcalendar.mock_provider import MockCalendarProvider


def test_connection():
    """Test: Verbindung zu Mock Calendar"""
    print("=" * 60)
    print("🧪 Test: Mock Calendar Verbindung")
    print("=" * 60)
    
    provider = MockCalendarProvider()
    
    print("\n⏳ Verbinde zu Mock Calendar...")
    success = provider.connect()
    
    if success:
        print(f"✅ Verbindung erfolgreich!")
        print(f"📅 {len(provider.events)} Beispiel-Events vorhanden")
        return provider
    else:
        print(f"❌ Verbindung fehlgeschlagen")
        return None


def test_list_all_events(provider):
    """Test: Alle Events anzeigen"""
    if not provider:
        print("\n⚠️ Überspringe Test - keine Verbindung")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Test: Alle Events anzeigen")
    print("=" * 60)
    
    events = provider.get_all_events()
    
    print(f"\n📋 Gesamt: {len(events)} Events\n")
    
    for i, event in enumerate(events, 1):
        print(f"{i}. {event.title}")
        print(f"   📅 {event.start.strftime('%Y-%m-%d %H:%M')} - {event.end.strftime('%H:%M')}")
        if event.location:
            print(f"   📍 {event.location}")
        if event.description:
            print(f"   📝 {event.description}")
        print(f"   🆔 {event.uid[:8]}...")
        print()


def test_list_events(provider):
    """Test: Events in Zeitraum"""
    if not provider:
        print("\n⚠️ Überspringe Test - keine Verbindung")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Test: Events heute")
    print("=" * 60)
    
    # Heute
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date.replace(hour=23, minute=59)
    
    print(f"\n📅 Zeitraum: {start_date.date()}")
    
    events = provider.list_events(start_date, end_date)
    
    print(f"\n📋 Gefunden: {len(events)} Events heute\n")
    
    for event in events:
        print(f"• {event.title} ({event.start.strftime('%H:%M')} - {event.end.strftime('%H:%M')})")


def test_create_event(provider):
    """Test: Event erstellen"""
    if not provider:
        print("\n⚠️ Überspringe Test - keine Verbindung")
        return None
    
    print("\n" + "=" * 60)
    print("🧪 Test: Event erstellen")
    print("=" * 60)
    
    # Test-Event morgen um 10:00
    start = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
    end = start + timedelta(hours=1, minutes=30)
    
    print(f"\n📝 Erstelle Test-Event:")
    print(f"   Titel: AdonisAI Demo Meeting")
    print(f"   Start: {start}")
    print(f"   Ende: {end}")
    
    event = provider.create_event(
        title="AdonisAI Demo Meeting",
        start=start,
        end=end,
        description="Demo für Mock Calendar Provider",
        location="Virtual Meeting Room"
    )
    
    print(f"\n✅ Event erstellt!")
    print(f"   🆔 UID: {event.uid}")
    
    return event


def test_update_event(provider, event):
    """Test: Event aktualisieren"""
    if not provider or not event:
        print("\n⚠️ Überspringe Test - keine Verbindung oder Event")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Test: Event aktualisieren")
    print("=" * 60)
    
    print(f"\n📝 Original: {event.title}")
    print(f"   Zeit: {event.start.strftime('%H:%M')} - {event.end.strftime('%H:%M')}")
    
    # Update
    new_start = event.start + timedelta(hours=1)
    new_end = event.end + timedelta(hours=1)
    
    updated = provider.update_event(
        event_uid=event.uid,
        title="AdonisAI Demo Meeting (Verschoben)",
        start=new_start,
        end=new_end
    )
    
    print(f"\n✅ Aktualisiert: {updated.title}")
    print(f"   Zeit: {updated.start.strftime('%H:%M')} - {updated.end.strftime('%H:%M')}")


def test_check_conflicts(provider):
    """Test: Konflikt-Erkennung"""
    if not provider:
        print("\n⚠️ Überspringe Test - keine Verbindung")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Test: Konflikt-Erkennung")
    print("=" * 60)
    
    # Test 1: Freier Zeitraum
    start = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=1)
    
    print(f"\n1️⃣ Prüfe Zeitraum: {start.strftime('%H:%M')} - {end.strftime('%H:%M')}")
    
    result = provider.check_conflicts(start, end)
    
    if result['has_conflict']:
        print(f"   ⚠️ {result['count']} Konflikt(e)")
    else:
        print(f"   ✅ Keine Konflikte")
    
    # Test 2: Konflikt mit Daily Standup (10:00)
    start2 = datetime.now().replace(hour=10, minute=30, second=0, microsecond=0)
    end2 = start2 + timedelta(hours=1)
    
    print(f"\n2️⃣ Prüfe Zeitraum: {start2.strftime('%H:%M')} - {end2.strftime('%H:%M')}")
    
    result2 = provider.check_conflicts(start2, end2)
    
    if result2['has_conflict']:
        print(f"   ⚠️ {result2['count']} Konflikt(e):")
        for conflict in result2['conflicts']:
            print(f"      - {conflict.title}")
    else:
        print(f"   ✅ Keine Konflikte")


def test_delete_event(provider, event):
    """Test: Event löschen"""
    if not provider or not event:
        print("\n⚠️ Überspringe Test - keine Verbindung oder Event")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Test: Event löschen")
    print("=" * 60)
    
    print(f"\n🗑️ Lösche: {event.title}")
    
    success = provider.delete_event(event.uid)
    
    if success:
        print(f"✅ Event gelöscht")
    else:
        print(f"❌ Löschen fehlgeschlagen")


def main():
    """Führt alle Tests aus"""
    print("\n🚀 AdonisAI Mock Calendar Tests")
    print("💡 Funktioniert OHNE Internet - perfekt für lokale Tests!")
    print("=" * 60)
    
    # Test 1: Verbindung
    provider = test_connection()
    
    if not provider:
        print("\n❌ Tests abgebrochen")
        return
    
    # Test 2: Alle Events anzeigen
    test_list_all_events(provider)
    
    # Test 3: Events heute
    test_list_events(provider)
    
    # Test 4: Event erstellen
    created_event = test_create_event(provider)
    
    # Test 5: Event aktualisieren
    test_update_event(provider, created_event)
    
    # Test 6: Konflikte prüfen
    test_check_conflicts(provider)
    
    # Test 7: Event löschen
    test_delete_event(provider, created_event)
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("✅ Alle Tests abgeschlossen")
    print("=" * 60)
    print(f"\n💡 Mock Calendar hat jetzt {len(provider.events)} Events")
    print("💡 Perfekt für lokale Entwicklung ohne API-Limits!")


if __name__ == "__main__":
    main()

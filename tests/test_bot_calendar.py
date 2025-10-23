"""
Test für Telegram Bot mit Calendar Integration
Simuliert Bot-Interaktionen (ohne echten Telegram Server)
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from src.gcalendar.mock_provider import MockCalendarProvider
from src.utils.nlp_utils import parse_event_from_text


def test_calendar_commands():
    """Test: Calendar Command Simulation"""
    print("=" * 60)
    print("🧪 Test: Calendar Commands (Mock)")
    print("=" * 60)
    
    # Mock Calendar Provider erstellen
    calendar = MockCalendarProvider()
    calendar.connect()
    
    # Test 1: /today
    print("\n1️⃣ /today Command:")
    print("-" * 60)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    events = calendar.list_events(today, tomorrow)
    
    print(f"📅 Termine heute ({today.strftime('%d.%m.%Y')})")
    for event in events:
        print(f"  • {event.start.strftime('%H:%M')} - {event.title}")
    
    # Test 2: /tomorrow
    print("\n2️⃣ /tomorrow Command:")
    print("-" * 60)
    tomorrow_start = today + timedelta(days=1)
    day_after = tomorrow_start + timedelta(days=1)
    events = calendar.list_events(tomorrow_start, day_after)
    
    print(f"📅 Termine morgen ({tomorrow_start.strftime('%d.%m.%Y')})")
    for event in events:
        print(f"  • {event.start.strftime('%H:%M')} - {event.title}")
    
    # Test 3: /next
    print("\n3️⃣ /next Command:")
    print("-" * 60)
    now = datetime.now()
    week_later = now + timedelta(days=30)
    events = calendar.list_events(now, week_later)
    
    next_event = None
    for event in events:
        if event.start > now:
            next_event = event
            break
    
    if next_event:
        time_until = next_event.start - now
        hours = time_until.seconds // 3600
        print(f"📅 Nächster Termin (in ~{hours}h)")
        print(f"  {next_event.title} @ {next_event.start.strftime('%d.%m %H:%M')}")
    
    return calendar


def test_natural_language_parsing():
    """Test: Natürlichsprachliche Event-Erstellung"""
    print("\n" + "=" * 60)
    print("🧪 Test: Natürliche Sprache → Event")
    print("=" * 60)
    
    test_messages = [
        "Termin morgen 15 Uhr Meeting mit Team",
        "Arztbesuch übermorgen 9:30 in der Klinik",
        "Code Review Montag 14 Uhr 2 Stunden",
    ]
    
    calendar = MockCalendarProvider()
    calendar.connect()
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. 💬 User: '{message}'")
        print("-" * 60)
        
        # Parse Event
        event_data = parse_event_from_text(message)
        
        if event_data['start']:
            # Prüfe Konflikte
            conflicts = calendar.check_conflicts(
                event_data['start'],
                event_data['end']
            )
            
            # Erstelle Event
            event = calendar.create_event(
                title=event_data['title'],
                start=event_data['start'],
                end=event_data['end'],
                location=event_data['location'],
                description="Erstellt via Bot Test"
            )
            
            print(f"✅ Bot: Termin erstellt!")
            print(f"   📌 {event.title}")
            print(f"   📅 {event.start.strftime('%d.%m.%Y um %H:%M')}")
            print(f"   ⏱ {event_data['duration_minutes']} Minuten")
            
            if conflicts['has_conflict']:
                print(f"   ⚠️ {conflicts['count']} Konflikt(e) gefunden")
        else:
            print("❌ Bot: Konnte kein Datum erkennen")


def test_week_overview():
    """Test: Wochenübersicht"""
    print("\n" + "=" * 60)
    print("🧪 Test: /week Command")
    print("=" * 60)
    
    calendar = MockCalendarProvider()
    calendar.connect()
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = today + timedelta(days=7)
    
    events = calendar.list_events(today, week_end)
    
    print(f"\n📅 Termine diese Woche ({today.strftime('%d.%m')} - {week_end.strftime('%d.%m')})\n")
    
    current_day = None
    for event in events:
        event_day = event.start.strftime('%d.%m.%Y')
        
        if event_day != current_day:
            current_day = event_day
            weekday = event.start.strftime('%A')
            weekday_de = {
                'Monday': 'Montag',
                'Tuesday': 'Dienstag',
                'Wednesday': 'Mittwoch',
                'Thursday': 'Donnerstag',
                'Friday': 'Freitag',
                'Saturday': 'Samstag',
                'Sunday': 'Sonntag'
            }.get(weekday, weekday)
            
            print(f"\n{weekday_de}, {event_day}")
        
        print(f"  {event.start.strftime('%H:%M')} - {event.title}")


def main():
    """Führt alle Tests aus"""
    print("\n🚀 AdonisAI Bot Calendar Integration Tests")
    print("💡 Simuliert Bot-Interaktionen mit Mock Calendar")
    print("=" * 60)
    
    # Test 1: Calendar Commands
    calendar = test_calendar_commands()
    
    # Test 2: Natural Language
    test_natural_language_parsing()
    
    # Test 3: Week Overview
    test_week_overview()
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("✅ Bot Integration Tests abgeschlossen")
    print("=" * 60)
    print(f"\n📊 Mock Calendar Status:")
    print(f"   Gesamt Events: {len(calendar.events)}")
    print("\n💡 Der Bot ist jetzt bereit für:")
    print("   • /today, /tomorrow, /week, /next Commands")
    print("   • Natürliche Sprache: 'Termin morgen 15 Uhr'")
    print("   • Konflikt-Erkennung")
    print("\n🚀 Starte den Bot mit: python run.py")


if __name__ == "__main__":
    main()

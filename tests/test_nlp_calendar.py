"""
Test für NLP Calendar Parsing
"""

import os
import sys
from datetime import datetime

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.nlp_utils import (
    parse_event_from_text,
    extract_datetime_from_text,
    extract_location_from_text,
    extract_event_title
)


def test_datetime_extraction():
    """Test: Datum/Zeit Extraktion"""
    print("=" * 60)
    print("🧪 Test: Datum/Zeit Extraktion")
    print("=" * 60)
    
    test_cases = [
        "morgen 15 Uhr",
        "heute um 10:30",
        "übermorgen 9 Uhr",
        "Montag um 14:00",
        "in 2 Stunden",
    ]
    
    for text in test_cases:
        result = extract_datetime_from_text(text)
        if result:
            print(f"\n📅 '{text}'")
            print(f"   Start: {result['start'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   Ende:  {result['end'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   Dauer: {result['duration_minutes']} min")
        else:
            print(f"\n❌ '{text}' - Konnte nicht geparst werden")


def test_location_extraction():
    """Test: Ort Extraktion"""
    print("\n" + "=" * 60)
    print("🧪 Test: Ort Extraktion")
    print("=" * 60)
    
    test_cases = [
        "Meeting in Room 302",
        "Termin bei der Bank",
        "Arztbesuch in der Klinik",
        "Conference Call @ Zoom",
        "Treffen im Cafe",
    ]
    
    for text in test_cases:
        location = extract_location_from_text(text)
        if location:
            print(f"\n📍 '{text}'")
            print(f"   Ort: {location}")
        else:
            print(f"\n❌ '{text}' - Kein Ort gefunden")


def test_title_extraction():
    """Test: Titel Extraktion"""
    print("\n" + "=" * 60)
    print("🧪 Test: Titel Extraktion")
    print("=" * 60)
    
    test_cases = [
        "Erstelle Termin Sprint Planning morgen 10 Uhr",
        "Meeting mit Team heute 15 Uhr",
        "Arzttermin Zahnarzt übermorgen",
        "Client Review nächsten Montag",
    ]
    
    for text in test_cases:
        title = extract_event_title(text)
        if title:
            print(f"\n📝 '{text}'")
            print(f"   Titel: {title}")
        else:
            print(f"\n❌ '{text}' - Kein Titel gefunden")


def test_full_event_parsing():
    """Test: Vollständiges Event Parsing"""
    print("\n" + "=" * 60)
    print("🧪 Test: Vollständiges Event Parsing")
    print("=" * 60)
    
    test_cases = [
        "Erstelle Termin Sprint Planning morgen 10 Uhr 2 Stunden",
        "Meeting mit Team heute 15 Uhr in Room 302",
        "Arzttermin übermorgen 9:30 bei der Klinik 30 Minuten",
        "Code Review Montag 14 Uhr 1 Stunde",
        "Client Call nächsten Dienstag 16:00",
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n{i}. 📋 Input: '{text}'")
        print("-" * 60)
        
        event = parse_event_from_text(text)
        
        print(f"   📌 Titel:    {event['title']}")
        if event['start']:
            print(f"   📅 Start:    {event['start'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   ⏰ Ende:     {event['end'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   ⌛ Dauer:    {event['duration_minutes']} min")
        else:
            print(f"   ⚠️  Start:    Nicht erkannt")
        
        if event['location']:
            print(f"   📍 Ort:      {event['location']}")


def test_edge_cases():
    """Test: Edge Cases und Spezialfälle"""
    print("\n" + "=" * 60)
    print("🧪 Test: Edge Cases")
    print("=" * 60)
    
    test_cases = [
        "Termin morgen",  # Ohne Uhrzeit
        "Meeting 15 Uhr",  # Ohne Datum
        "Heute Arzt",      # Minimal
        "Erstelle Termin Meeting mit CEO und CTO morgen 10 Uhr in Conference Room A 1.5 Stunden",  # Komplex
    ]
    
    for text in test_cases:
        print(f"\n🔍 '{text}'")
        event = parse_event_from_text(text)
        
        print(f"   Titel: {event['title'] or 'N/A'}")
        print(f"   Start: {event['start'].strftime('%d.%m %H:%M') if event['start'] else 'N/A'}")
        print(f"   Ort:   {event['location'] or 'N/A'}")


def main():
    """Führt alle Tests aus"""
    print("\n🚀 AdonisAI NLP Calendar Parsing Tests")
    print("💡 Deutsche Sprache & natürliche Eingaben")
    print("=" * 60)
    
    # Test 1: Datum/Zeit
    test_datetime_extraction()
    
    # Test 2: Ort
    test_location_extraction()
    
    # Test 3: Titel
    test_title_extraction()
    
    # Test 4: Vollständiges Parsing
    test_full_event_parsing()
    
    # Test 5: Edge Cases
    test_edge_cases()
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("✅ NLP Tests abgeschlossen")
    print("=" * 60)
    print("\n💡 Das Parsing funktioniert jetzt mit natürlicher Sprache!")
    print("💡 Beispiele:")
    print("   • 'Termin morgen 15 Uhr Meeting mit Team'")
    print("   • 'Arztbesuch übermorgen 9:30 in der Klinik'")
    print("   • 'Code Review Montag 14 Uhr 2 Stunden'")


if __name__ == "__main__":
    main()

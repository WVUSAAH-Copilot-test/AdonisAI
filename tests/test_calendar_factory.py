"""
Test für Calendar Factory - Automatische Provider-Auswahl
"""

import os
import sys
from dotenv import load_dotenv

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# .env laden
load_dotenv()

from src.gcalendar.factory import create_calendar_provider, get_available_providers


def test_available_providers():
    """Zeigt verfügbare Provider"""
    print("=" * 60)
    print("🧪 Test: Verfügbare Calendar Provider")
    print("=" * 60)
    
    providers = get_available_providers()
    
    for name, info in providers.items():
        status = "✅ Verfügbar" if info['available'] else "❌ Nicht konfiguriert"
        print(f"\n📅 {name.upper()}: {status}")
        print(f"   {info['description']}")
        
        if info['requires']:
            print(f"   Benötigt: {', '.join(info['requires'])}")


def test_create_provider():
    """Test: Provider erstellen"""
    print("\n" + "=" * 60)
    print("🧪 Test: Provider aus .env erstellen")
    print("=" * 60)
    
    provider_type = os.getenv('CALENDAR_PROVIDER', 'mock')
    print(f"\n📋 CALENDAR_PROVIDER={provider_type}")
    
    print("\n⏳ Erstelle Provider...")
    provider = create_calendar_provider()
    
    print(f"✅ Provider erstellt: {provider.__class__.__name__}")
    
    return provider


def test_provider_switch():
    """Test: Provider manuell wechseln"""
    print("\n" + "=" * 60)
    print("🧪 Test: Provider manuell wechseln")
    print("=" * 60)
    
    # Test Mock
    print("\n1️⃣ Mock Provider:")
    mock = create_calendar_provider('mock')
    print(f"   ✅ {mock.__class__.__name__}")
    
    # Test Google (falls nicht verfügbar → Fallback zu Mock)
    print("\n2️⃣ Google Provider:")
    google = create_calendar_provider('google')
    print(f"   ✅ {google.__class__.__name__}")
    
    # Test iCloud (falls nicht verfügbar → Fallback zu Mock)
    print("\n3️⃣ iCloud Provider:")
    icloud = create_calendar_provider('icloud')
    print(f"   ✅ {icloud.__class__.__name__}")
    
    # Test Unknown (sollte Mock werden)
    print("\n4️⃣ Unknown Provider (sollte Mock werden):")
    unknown = create_calendar_provider('unknown')
    print(f"   ✅ {unknown.__class__.__name__}")


def main():
    """Führt alle Tests aus"""
    print("\n🚀 AdonisAI Calendar Factory Tests")
    print("💡 Intelligente Provider-Auswahl mit Fallback!")
    print("=" * 60)
    
    # Test 1: Verfügbare Provider
    test_available_providers()
    
    # Test 2: Provider aus .env erstellen
    provider = test_create_provider()
    
    # Test 3: Provider manuell wechseln
    test_provider_switch()
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("✅ Factory Tests abgeschlossen")
    print("=" * 60)
    print("\n💡 Die Factory wählt automatisch den besten verfügbaren Provider")
    print("💡 Bei Problemen: Automatischer Fallback zu Mock Provider")


if __name__ == "__main__":
    main()

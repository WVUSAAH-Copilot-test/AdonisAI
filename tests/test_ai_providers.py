#!/usr/bin/env python3
"""
Test-Skript für AI Provider
Testet Hugging Face und OpenRouter Integration ohne Bot
"""

import asyncio
import sys
import os
from pathlib import Path

# Projekt-Root zum Path hinzufügen
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from src.ai.hf_provider import HuggingFaceProvider
from src.ai.openrouter_provider import OpenRouterProvider

# SSL-Workaround
import ssl
import urllib3
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load .env
load_dotenv(project_root / '.env')


async def test_huggingface():
    """Testet Hugging Face Provider"""
    print("\n" + "="*60)
    print("🤖 HUGGING FACE PROVIDER TEST")
    print("="*60)
    
    # Initialisiere Provider
    hf = HuggingFaceProvider(model='flan-t5-base')
    
    # Test 1: Einfache Frage
    print("\n📝 Test 1: Einfache Frage")
    print("-" * 60)
    question = "Was ist die Hauptstadt von Deutschland?"
    print(f"Frage: {question}")
    answer = await hf.generate_response(question)
    print(f"Antwort: {answer}")
    
    # Test 2: Intent-Erkennung
    print("\n🎯 Test 2: Intent-Erkennung")
    print("-" * 60)
    texts = [
        "Erstelle einen Termin für morgen um 15 Uhr",
        "Erinnere mich an den Meeting",
        "Wie wird das Wetter morgen?",
        "Hallo, wie geht es dir?"
    ]
    
    for text in texts:
        result = await hf.analyze_intent(text)
        print(f"Text: {text}")
        print(f"  → Intent: {result['intent']} (Confidence: {result['confidence']})")
    
    print("\n✅ Hugging Face Tests abgeschlossen")


async def test_openrouter():
    """Testet OpenRouter Provider"""
    print("\n" + "="*60)
    print("🌐 OPENROUTER PROVIDER TEST")
    print("="*60)
    
    # Check API Key
    if not os.getenv('OPENROUTER_API_KEY'):
        print("⚠️  OPENROUTER_API_KEY nicht gesetzt - überspringe Tests")
        return
    
    # Initialisiere Provider
    router = OpenRouterProvider(model='gpt-3.5')
    
    # Test 1: Einfache Frage
    print("\n📝 Test 1: Einfache Konversation")
    print("-" * 60)
    question = "Erkläre mir in einem Satz was Python ist."
    print(f"Frage: {question}")
    answer = await router.generate_response(question)
    print(f"Antwort: {answer}")
    
    # Test 2: Mit Context
    print("\n💬 Test 2: Mit Kontext")
    print("-" * 60)
    context = {
        'system_prompt': 'Du bist ein freundlicher Assistent der kurz und präzise antwortet.',
        'temperature': 0.5,
        'max_tokens': 100
    }
    question = "Was kann ich heute unternehmen wenn es regnet?"
    print(f"Frage: {question}")
    answer = await router.generate_response(question, context)
    print(f"Antwort: {answer}")
    
    # Test 3: Intent-Erkennung
    print("\n🎯 Test 3: Intent-Erkennung")
    print("-" * 60)
    texts = [
        "Termin am Freitag 14 Uhr eintragen",
        "Vergiss nicht den Zahnarzt anzurufen"
    ]
    
    for text in texts:
        result = await router.analyze_intent(text)
        print(f"Text: {text}")
        print(f"  → Intent: {result['intent']} (Confidence: {result['confidence']})")
    
    print("\n✅ OpenRouter Tests abgeschlossen")


async def main():
    """Hauptfunktion"""
    print("""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║          🧪 AI Provider Tests 🧪              ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    try:
        # Test Hugging Face (immer verfügbar)
        await test_huggingface()
        
        # Test OpenRouter (nur wenn API Key gesetzt)
        await test_openrouter()
        
        print("\n" + "="*60)
        print("✅ ALLE TESTS ABGESCHLOSSEN")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests abgebrochen")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Python 3.6 kompatibel
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

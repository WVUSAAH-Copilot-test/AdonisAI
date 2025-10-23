"""
AdonisAI - Haupteinstiegspunkt
Startet den Telegram Bot und koordiniert alle Module
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Projektverzeichnis zum Python Path hinzufügen
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.bot.telegram_bot import create_bot

# Logging konfigurieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def load_environment() -> None:
    """
    Lädt Umgebungsvariablen aus .env Datei
    """
    env_path = project_root / '.env'
    
    if not env_path.exists():
        logger.warning("⚠️  .env Datei nicht gefunden!")
        logger.info("📝 Bitte erstelle eine .env Datei basierend auf .env.example")
        logger.info("   cp .env.example .env")
        sys.exit(1)
    
    load_dotenv(env_path)
    logger.info("✅ Umgebungsvariablen geladen")


def validate_config() -> bool:
    """
    Validiert die erforderlichen Konfigurationen
    
    Returns:
        True wenn alle erforderlichen Configs vorhanden sind
    """
    required_vars = ['TELEGRAM_BOT_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error("❌ Fehlende Umgebungsvariablen:")
        for var in missing_vars:
            logger.error(f"   - {var}")
        logger.info("\n💡 Bitte füge diese Variablen in deine .env Datei ein")
        return False
    
    logger.info("✅ Konfiguration validiert")
    return True


def create_directories() -> None:
    """
    Erstellt erforderliche Verzeichnisse falls nicht vorhanden
    """
    directories = [
        project_root / 'data',
        project_root / 'logs'
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
    
    logger.info("✅ Verzeichnisse überprüft")


def print_banner() -> None:
    """
    Zeigt das AdonisAI Banner
    """
    banner = """
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║          🤖  AdonisAI v0.1.0  🤖              ║
    ║                                               ║
    ║      Persönlicher KI-Assistent                ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)


def main() -> None:
    """
    Hauptfunktion - Startet den Bot
    """
    # Banner anzeigen
    print_banner()
    
    # Umgebungsvariablen laden
    logger.info("🔧 Initialisierung...")
    load_environment()
    
    # Konfiguration validieren
    if not validate_config():
        sys.exit(1)
    
    # Verzeichnisse erstellen
    create_directories()
    
    # Telegram Bot Token laden
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Bot erstellen und starten
    try:
        bot = create_bot(telegram_token)
        logger.info("✅ Bot erfolgreich initialisiert")
        logger.info("🚀 Bot wird gestartet...\n")
        
        # Bot im Polling-Modus starten
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("\n⏹️  Bot wurde durch Benutzer gestoppt")
        
    except Exception as e:
        logger.error(f"❌ Fehler beim Starten des Bots: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
    
    finally:
        logger.info("👋 AdonisAI beendet")


if __name__ == '__main__':
    main()

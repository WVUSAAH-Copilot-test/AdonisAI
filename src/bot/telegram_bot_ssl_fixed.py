"""
Telegram Bot - Alternative Version mit direkter urllib3 Konfiguration
Löst SSL-Probleme in Firmennetzwerken
"""

import os
import logging
import ssl
import urllib3
from typing import Optional
from telegram import Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

# SSL-Warnungen deaktivieren
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Logging konfigurieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class AdonisBot:
    """
    Hauptklasse für den AdonisAI Telegram Bot mit SSL-Workarounds
    """
    
    def __init__(self, token: str):
        """
        Initialisiert den Bot mit dem Telegram Token
        
        Args:
            token: Telegram Bot API Token
        """
        self.token = token
        self.updater: Optional[Updater] = None
        
        # SSL-Context konfigurieren
        self._setup_ssl_context()
        
    def _setup_ssl_context(self):
        """Konfiguriert SSL-Context für unsichere Verbindungen"""
        # Erstelle unverified SSL context
        ssl._create_default_https_context = ssl._create_unverified_context
        logger.info("SSL-Context konfiguriert (unverified)")
        
    def start_command(self, update: Update, context: CallbackContext) -> None:
        """Handler für den /start Befehl"""
        user = update.effective_user
        welcome_message = (
            f"Hallo {user.first_name}! 👋\n\n"
            "Ich bin **AdonisAI**, dein persönlicher KI-Assistent.\n\n"
            "**Verfügbare Befehle:**\n"
            "/start - Bot starten\n"
            "/help - Hilfe anzeigen\n"
            "/info - Bot-Informationen\n\n"
            "Schreib mir einfach eine Nachricht und ich helfe dir gerne!"
        )
        update.message.reply_text(welcome_message, parse_mode='Markdown')
        logger.info(f"Bot gestartet von User: {user.id} ({user.username})")
    
    def help_command(self, update: Update, context: CallbackContext) -> None:
        """Handler für den /help Befehl"""
        help_text = (
            "**AdonisAI - Hilfe** 📚\n\n"
            "**Grundlegende Befehle:**\n"
            "/start - Bot starten\n"
            "/help - Diese Hilfe anzeigen\n"
            "/info - Bot-Informationen\n\n"
            "**Kommende Features:**\n"
            "📅 Kalender-Verwaltung (Google Calendar)\n"
            "🎤 Sprachnachrichten verstehen\n"
            "🔊 Sprachausgabe\n"
            "🧠 KI-gestützte Antworten\n\n"
            "Sende mir einfach eine Textnachricht und ich antworte dir!"
        )
        update.message.reply_text(help_text, parse_mode='Markdown')
        logger.info(f"Hilfe angefordert von User: {update.effective_user.id}")
    
    def info_command(self, update: Update, context: CallbackContext) -> None:
        """Handler für den /info Befehl"""
        info_text = (
            "**AdonisAI v0.1.0** 🤖\n\n"
            "Ein kostenloser, Open-Source KI-Assistent.\n\n"
            "**Features:**\n"
            "✅ Telegram Integration\n"
            "🚧 KI-Modelle (in Entwicklung)\n"
            "🚧 Google Calendar (in Entwicklung)\n"
            "🚧 Sprachverarbeitung (in Entwicklung)\n\n"
            "**GitHub:** https://github.com/wvusaah/AdonisAI\n"
            "**Lizenz:** MIT\n\n"
            "Made with ❤️ by the AdonisAI Community"
        )
        update.message.reply_text(info_text, parse_mode='Markdown')
        logger.info(f"Info angefordert von User: {update.effective_user.id}")
    
    def handle_message(self, update: Update, context: CallbackContext) -> None:
        """Handler für eingehende Text-Nachrichten"""
        user = update.effective_user
        message_text = update.message.text
        
        logger.info(f"Nachricht von {user.id} ({user.username}): {message_text}")
        
        response = (
            f"Du hast geschrieben: *{message_text}*\n\n"
            "🚧 Die KI-Integration ist noch in Entwicklung.\n"
            "Bald kann ich intelligente Antworten geben!"
        )
        
        update.message.reply_text(response, parse_mode='Markdown')
    
    def handle_voice(self, update: Update, context: CallbackContext) -> None:
        """Handler für Sprachnachrichten"""
        user = update.effective_user
        logger.info(f"Sprachnachricht von {user.id} ({user.username})")
        
        response = (
            "🎤 Sprachnachricht empfangen!\n\n"
            "🚧 Speech-to-Text ist noch in Entwicklung.\n"
            "Bald kann ich deine Sprachnachrichten verstehen!"
        )
        
        update.message.reply_text(response, parse_mode='Markdown')
    
    def error_handler(self, update: object, context: CallbackContext) -> None:
        """Handler für Fehler"""
        logger.error(f"Update {update} verursachte Fehler: {context.error}")
        
        if isinstance(update, Update) and update.effective_message:
            update.effective_message.reply_text(
                "⚠️ Es ist ein Fehler aufgetreten.\n"
                "Bitte versuche es erneut oder kontaktiere den Support."
            )
    
    def setup_handlers(self) -> None:
        """Registriert alle Command- und Message-Handler"""
        dispatcher = self.updater.dispatcher
        
        dispatcher.add_handler(CommandHandler("start", self.start_command))
        dispatcher.add_handler(CommandHandler("help", self.help_command))
        dispatcher.add_handler(CommandHandler("info", self.info_command))
        
        dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, self.handle_message)
        )
        
        dispatcher.add_handler(
            MessageHandler(Filters.voice, self.handle_voice)
        )
        
        dispatcher.add_error_handler(self.error_handler)
        
        logger.info("Alle Handler wurden registriert")
    
    def run(self) -> None:
        """Startet den Bot im Polling-Modus mit SSL-Workarounds"""
        try:
            # Erstelle Bot mit Request-Objekt für SSL-Workarounds
            from telegram.utils.request import Request
            
            # Request mit deaktivierter SSL-Verifizierung
            req = Request(con_pool_size=8)
            
            # Monkey-patch für SSL
            import requests
            old_request = requests.Session.request
            def new_request(self, *args, **kwargs):
                kwargs.setdefault('verify', False)
                return old_request(self, *args, **kwargs)
            requests.Session.request = new_request
            
            # Bot erstellen
            bot = Bot(token=self.token)
            self.updater = Updater(bot=bot, use_context=True)
            
            logger.info("✅ Bot-Objekt erfolgreich erstellt")
            
        except Exception as e:
            logger.error(f"❌ Fehler beim Erstellen des Bots: {e}")
            # Fallback auf normale Methode
            self.updater = Updater(token=self.token, use_context=True)
            logger.info("⚠️  Fallback auf Standard-Updater")
        
        # Handler registrieren
        self.setup_handlers()
        
        # Bot starten
        logger.info("🤖 AdonisAI Bot wird gestartet...")
        self.updater.start_polling()
        self.updater.idle()


def create_bot(token: str) -> AdonisBot:
    """
    Factory-Funktion zum Erstellen einer Bot-Instanz
    
    Args:
        token: Telegram Bot API Token
        
    Returns:
        AdonisBot Instanz
    """
    return AdonisBot(token)

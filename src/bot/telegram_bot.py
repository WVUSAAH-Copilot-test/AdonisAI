"""
Telegram Bot - Hauptmodul
Verwaltet die Telegram Bot Logik und Nachrichtenverarbeitung
"""

import os
import logging
from typing import Optional
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

# Logging konfigurieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class AdonisBot:
    """
    Hauptklasse für den AdonisAI Telegram Bot
    """
    
    def __init__(self, token: str):
        """
        Initialisiert den Bot mit dem Telegram Token
        
        Args:
            token: Telegram Bot API Token
        """
        self.token = token
        self.updater: Optional[Updater] = None
        
    def start_command(self, update: Update, context: CallbackContext) -> None:
        """
        Handler für den /start Befehl
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
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
        """
        Handler für den /help Befehl
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
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
        """
        Handler für den /info Befehl
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
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
        """
        Handler für eingehende Text-Nachrichten
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
        user = update.effective_user
        message_text = update.message.text
        
        logger.info(f"Nachricht von {user.id} ({user.username}): {message_text}")
        
        # Einfache Echo-Funktion als Platzhalter
        # TODO: Hier wird später die KI-Integration erfolgen
        response = (
            f"Du hast geschrieben: *{message_text}*\n\n"
            "🚧 Die KI-Integration ist noch in Entwicklung.\n"
            "Bald kann ich intelligente Antworten geben!"
        )
        
        update.message.reply_text(response, parse_mode='Markdown')
    
    def handle_voice(self, update: Update, context: CallbackContext) -> None:
        """
        Handler für Sprachnachrichten
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
        user = update.effective_user
        logger.info(f"Sprachnachricht von {user.id} ({user.username})")
        
        # Platzhalter für Speech-to-Text Integration
        response = (
            "🎤 Sprachnachricht empfangen!\n\n"
            "🚧 Speech-to-Text ist noch in Entwicklung.\n"
            "Bald kann ich deine Sprachnachrichten verstehen!"
        )
        
        update.message.reply_text(response, parse_mode='Markdown')
    
    def error_handler(self, update: object, context: CallbackContext) -> None:
        """
        Handler für Fehler
        
        Args:
            update: Update Objekt
            context: Callback Context
        """
        logger.error(f"Update {update} verursachte Fehler: {context.error}")
        
        # Nur bei regulären Updates eine Fehlermeldung senden
        if isinstance(update, Update) and update.effective_message:
            update.effective_message.reply_text(
                "⚠️ Es ist ein Fehler aufgetreten.\n"
                "Bitte versuche es erneut oder kontaktiere den Support."
            )
    
    def setup_handlers(self) -> None:
        """
        Registriert alle Command- und Message-Handler
        """
        dispatcher = self.updater.dispatcher
        
        # Command Handler
        dispatcher.add_handler(CommandHandler("start", self.start_command))
        dispatcher.add_handler(CommandHandler("help", self.help_command))
        dispatcher.add_handler(CommandHandler("info", self.info_command))
        
        # Message Handler
        dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, self.handle_message)
        )
        
        # Voice Message Handler
        dispatcher.add_handler(
            MessageHandler(Filters.voice, self.handle_voice)
        )
        
        # Error Handler
        dispatcher.add_error_handler(self.error_handler)
        
        logger.info("Alle Handler wurden registriert")
    
    def run(self) -> None:
        """
        Startet den Bot im Polling-Modus
        """
        # Updater erstellen
        self.updater = Updater(token=self.token, use_context=True)
        
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

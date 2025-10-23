"""
Telegram Bot - Hauptmodul
Verwaltet die Telegram Bot Logik und Nachrichtenverarbeitung
"""

import os
import logging
from typing import Optional
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

# AI Integration
from src.ai.hf_provider import HuggingFaceProvider
from src.ai.openrouter_provider import OpenRouterProvider
from src.utils.nlp_utils import detect_command_type, parse_event_from_text

# Calendar Integration
from src.gcalendar.factory import create_calendar_provider

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
    
    def __init__(self, token: str, use_ai: bool = True, use_calendar: bool = True):
        """
        Initialisiert den Bot mit dem Telegram Token
        
        Args:
            token: Telegram Bot API Token
            use_ai: Ob AI-Provider verwendet werden sollen
            use_calendar: Ob Calendar-Integration aktiv sein soll
        """
        self.token = token
        self.updater: Optional[Updater] = None
        self.use_ai = use_ai
        self.use_calendar = use_calendar
        self.ai_provider = None
        self.calendar_provider = None
        
        # Initialisiere AI Provider wenn gewünscht
        if self.use_ai:
            self._init_ai_provider()
        
        # Initialisiere Calendar Provider wenn gewünscht
        if self.use_calendar:
            self._init_calendar_provider()
    
    def _init_ai_provider(self):
        """Initialisiert den AI Provider"""
        try:
            # Prüfe welcher Provider verfügbar ist
            provider_type = os.getenv('AI_PROVIDER', 'huggingface').lower()
            
            if provider_type == 'openrouter' and os.getenv('OPENROUTER_API_KEY'):
                logger.info("🌐 Verwende OpenRouter Provider")
                self.ai_provider = OpenRouterProvider()
            else:
                logger.info("🤖 Verwende Hugging Face Provider")
                self.ai_provider = HuggingFaceProvider()
            
            logger.info("✅ AI Provider initialisiert")
            
        except Exception as e:
            logger.warning(f"⚠️  AI Provider konnte nicht initialisiert werden: {e}")
            logger.info("ℹ️  Bot läuft im Echo-Modus")
            self.ai_provider = None
    
    def _init_calendar_provider(self):
        """Initialisiert den Calendar Provider"""
        try:
            self.calendar_provider = create_calendar_provider()
            logger.info(f"✅ Calendar Provider initialisiert: {self.calendar_provider.__class__.__name__}")
        except Exception as e:
            logger.warning(f"⚠️ Calendar Provider konnte nicht initialisiert werden: {e}")
            self.calendar_provider = None
        
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
            "📋 *Allgemein:*\n"
            "/start - Bot starten\n"
            "/help - Hilfe anzeigen\n"
            "/info - Bot-Informationen\n\n"
            "📅 *Kalender:*\n"
            "/today - Termine heute\n"
            "/tomorrow - Termine morgen\n"
            "/week - Termine diese Woche\n"
            "/next - Nächster Termin\n\n"
            "💬 *Natürliche Sprache:*\n"
            "Sag einfach: 'Termin morgen 15 Uhr Meeting'\n"
            "Oder: 'Was habe ich heute?'"
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
    
    def today_command(self, update: Update, context: CallbackContext) -> None:
        """Handler für /today - Zeigt heutige Termine"""
        if not self.calendar_provider:
            update.message.reply_text("❌ Calendar ist nicht verfügbar")
            return
        
        try:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            tomorrow = today + timedelta(days=1)
            
            events = self.calendar_provider.list_events(today, tomorrow)
            
            if not events:
                update.message.reply_text("📅 Keine Termine heute 🎉")
                return
            
            message = f"📅 *Termine heute* ({today.strftime('%d.%m.%Y')})\n\n"
            
            for event in events:
                message += f"📌 *{event.title}*\n"
                message += f"⏰ {event.start.strftime('%H:%M')} - {event.end.strftime('%H:%M')}\n"
                if event.location:
                    message += f"📍 {event.location}\n"
                message += "\n"
            
            update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Fehler bei /today: {e}")
            update.message.reply_text("❌ Fehler beim Abrufen der Termine")
    
    def tomorrow_command(self, update: Update, context: CallbackContext) -> None:
        """Handler für /tomorrow - Zeigt morgige Termine"""
        if not self.calendar_provider:
            update.message.reply_text("❌ Calendar ist nicht verfügbar")
            return
        
        try:
            tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            day_after = tomorrow + timedelta(days=1)
            
            events = self.calendar_provider.list_events(tomorrow, day_after)
            
            if not events:
                update.message.reply_text("📅 Keine Termine morgen 🎉")
                return
            
            message = f"📅 *Termine morgen* ({tomorrow.strftime('%d.%m.%Y')})\n\n"
            
            for event in events:
                message += f"📌 *{event.title}*\n"
                message += f"⏰ {event.start.strftime('%H:%M')} - {event.end.strftime('%H:%M')}\n"
                if event.location:
                    message += f"📍 {event.location}\n"
                message += "\n"
            
            update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Fehler bei /tomorrow: {e}")
            update.message.reply_text("❌ Fehler beim Abrufen der Termine")
    
    def week_command(self, update: Update, context: CallbackContext) -> None:
        """Handler für /week - Zeigt Termine der Woche"""
        if not self.calendar_provider:
            update.message.reply_text("❌ Calendar ist nicht verfügbar")
            return
        
        try:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            week_end = today + timedelta(days=7)
            
            events = self.calendar_provider.list_events(today, week_end)
            
            if not events:
                update.message.reply_text("📅 Keine Termine diese Woche 🎉")
                return
            
            message = f"📅 *Termine diese Woche*\n({today.strftime('%d.%m')} - {week_end.strftime('%d.%m.%Y')})\n\n"
            
            current_day = None
            for event in events:
                event_day = event.start.strftime('%d.%m.%Y')
                
                # Neuer Tag - Überschrift
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
                    
                    message += f"\n*{weekday_de}, {event_day}*\n"
                
                message += f"  ⏰ {event.start.strftime('%H:%M')} - {event.title}\n"
            
            update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Fehler bei /week: {e}")
            update.message.reply_text("❌ Fehler beim Abrufen der Termine")
    
    def next_command(self, update: Update, context: CallbackContext) -> None:
        """Handler für /next - Zeigt nächsten Termin"""
        if not self.calendar_provider:
            update.message.reply_text("❌ Calendar ist nicht verfügbar")
            return
        
        try:
            now = datetime.now()
            week_later = now + timedelta(days=30)
            
            events = self.calendar_provider.list_events(now, week_later)
            
            # Finde nächsten Termin in der Zukunft
            next_event = None
            for event in events:
                if event.start > now:
                    next_event = event
                    break
            
            if not next_event:
                update.message.reply_text("📅 Kein anstehender Termin in den nächsten 30 Tagen")
                return
            
            # Berechne Zeitdifferenz
            time_until = next_event.start - now
            days = time_until.days
            hours = time_until.seconds // 3600
            minutes = (time_until.seconds % 3600) // 60
            
            time_str = ""
            if days > 0:
                time_str = f"in {days} Tag(en)"
            elif hours > 0:
                time_str = f"in {hours} Stunde(n)"
            else:
                time_str = f"in {minutes} Minute(n)"
            
            message = f"📅 *Nächster Termin* ({time_str})\n\n"
            message += f"📌 *{next_event.title}*\n"
            message += f"📅 {next_event.start.strftime('%d.%m.%Y')}\n"
            message += f"⏰ {next_event.start.strftime('%H:%M')} - {next_event.end.strftime('%H:%M')}\n"
            
            if next_event.location:
                message += f"📍 {next_event.location}\n"
            
            if next_event.description:
                message += f"\n📝 {next_event.description}"
            
            update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Fehler bei /next: {e}")
            update.message.reply_text("❌ Fehler beim Abrufen des Termins")
    
    def handle_message(self, update: Update, context: CallbackContext) -> None:
        """
        Handler für Text-Nachrichten
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
        user = update.effective_user
        message_text = update.message.text
        
        logger.info(f"Nachricht von {user.id} ({user.username}): {message_text}")
        
        # Prüfe ob es ein Calendar-Command ist
        command_type = detect_command_type(message_text)
        
        if command_type == 'calendar' and self.calendar_provider:
            self._handle_calendar_message(update, message_text)
            return
        
        # Versuche AI-Antwort zu generieren
        if self.ai_provider:
            try:
                response = self.ai_provider.generate_response(message_text)
                update.message.reply_text(response)
            except Exception as e:
                logger.error(f"AI Provider Fehler: {e}")
                # Fallback zu Echo-Modus
                update.message.reply_text(f"Echo: {message_text}")
        else:
            # Echo-Modus wenn kein AI Provider
            update.message.reply_text(f"Echo: {message_text}")
    
    def _handle_calendar_message(self, update: Update, message_text: str) -> None:
        """
        Verarbeitet Calendar-bezogene Nachrichten
        
        Args:
            update: Telegram Update
            message_text: Nachricht vom User
        """
        try:
            # Parse Event aus Text
            event_data = parse_event_from_text(message_text)
            
            if not event_data['start']:
                update.message.reply_text(
                    "⚠️ Ich konnte kein Datum/Uhrzeit erkennen.\n"
                    "Beispiel: 'Termin morgen 15 Uhr Meeting'"
                )
                return
            
            # Prüfe Konflikte
            conflicts = self.calendar_provider.check_conflicts(
                event_data['start'],
                event_data['end']
            )
            
            conflict_warning = ""
            if conflicts['has_conflict']:
                conflict_warning = f"\n\n⚠️ {conflicts['warning']}\n"
                for conflict in conflicts['conflicts']:
                    conflict_warning += f"  • {conflict.title} ({conflict.start.strftime('%H:%M')} - {conflict.end.strftime('%H:%M')})\n"
            
            # Bestätigung senden
            confirmation = (
                f"📅 *Neuer Termin:*\n\n"
                f"📌 {event_data['title']}\n"
                f"📅 {event_data['start'].strftime('%d.%m.%Y um %H:%M Uhr')}\n"
                f"⏱ {event_data['duration_minutes']} Minuten\n"
            )
            
            if event_data['location']:
                confirmation += f"📍 {event_data['location']}\n"
            
            confirmation += conflict_warning
            confirmation += "\n✅ Termin wurde erstellt!"
            
            # Event erstellen
            event = self.calendar_provider.create_event(
                title=event_data['title'],
                start=event_data['start'],
                end=event_data['end'],
                location=event_data['location'],
                description=f"Erstellt via AdonisAI Telegram Bot"
            )
            
            update.message.reply_text(confirmation, parse_mode='Markdown')
            logger.info(f"Event erstellt: {event.title} @ {event.start}")
            
        except Exception as e:
            logger.error(f"Fehler beim Calendar-Handling: {e}")
            update.message.reply_text(
                "❌ Fehler beim Erstellen des Termins.\n"
                "Bitte versuche es erneut."
            )
    
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
        
        # Command Handler - Allgemein
        dispatcher.add_handler(CommandHandler("start", self.start_command))
        dispatcher.add_handler(CommandHandler("help", self.help_command))
        dispatcher.add_handler(CommandHandler("info", self.info_command))
        
        # Command Handler - Calendar
        dispatcher.add_handler(CommandHandler("today", self.today_command))
        dispatcher.add_handler(CommandHandler("tomorrow", self.tomorrow_command))
        dispatcher.add_handler(CommandHandler("week", self.week_command))
        dispatcher.add_handler(CommandHandler("next", self.next_command))
        
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

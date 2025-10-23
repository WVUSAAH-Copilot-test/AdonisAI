"""
Telegram Bot - Hauptmodul
Verwaltet die Telegram Bot Logik und Nachrichtenverarbeitung
"""

import os
import sys
import logging
from typing import Optional
from datetime import datetime, timedelta
from functools import wraps
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

# Context Management
from src.utils.context_manager import ContextManager

# Interaction Logging
from src.storage.interaction_logger import InteractionLogger

# Logging konfigurieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def admin_only(func):
    """
    Decorator für Admin-only Commands
    Prüft ob User die ADMIN_USER_ID aus .env hat
    """
    @wraps(func)
    def wrapper(self, update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        admin_id = os.getenv('ADMIN_USER_ID', None)
        
        if admin_id is None:
            update.message.reply_text(
                "⚠️ ADMIN_USER_ID nicht in .env konfiguriert!\n"
                "Füge deine User-ID hinzu (siehe /myid)"
            )
            logger.warning("ADMIN_USER_ID nicht konfiguriert")
            return
        
        try:
            admin_id = int(admin_id)
        except ValueError:
            update.message.reply_text("⚠️ ADMIN_USER_ID ist ungültig!")
            logger.error(f"Ungültige ADMIN_USER_ID: {admin_id}")
            return
        
        if user_id != admin_id:
            update.message.reply_text(
                "⛔ **Zugriff verweigert**\n\n"
                "Dieser Befehl ist nur für Admins verfügbar.",
                parse_mode='Markdown'
            )
            logger.warning(f"Unauthorized access attempt by user {user_id}")
            return
        
        return func(self, update, context)
    return wrapper


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
        
        # Context Manager für Chat-Historie
        self.context_manager = ContextManager(max_messages=10, ttl_minutes=30)
        
        # Interaction Logger für Personal AI Training
        self.interaction_logger = InteractionLogger()
        logger.info("🧠 Interaction Logging aktiviert - Sammle Daten für Personal AI")
        
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
            "/info - Bot-Informationen\n"
            "/features - Alle Funktionen im Detail\n"
            "/myid - Deine Telegram User-ID anzeigen\n\n"
            "📅 *Kalender:*\n"
            "/today - Termine heute\n"
            "/tomorrow - Termine morgen\n"
            "/week - Termine diese Woche\n"
            "/next - Nächster Termin\n\n"
            "💬 *Natürliche Sprache:*\n"
            "Sag einfach: 'Termin morgen 15 Uhr Meeting'\n"
            "Oder: 'Was habe ich heute?'\n\n"
            "Tippe /features für die komplette Übersicht! 🚀"
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
            "**📋 Allgemeine Befehle:**\n"
            "/start - Bot starten und Übersicht\n"
            "/help - Diese Hilfe anzeigen\n"
            "/info - Bot-Informationen & Version\n"
            "/features - Alle Funktionen im Detail\n"
            "/myid - Deine User-ID (für Admin-Setup)\n\n"
            
            "**🔒 Admin-Befehle:**\n"
            "/shutdown - Bot herunterfahren (nur Admin)\n"
            "/stats - Training Dataset Statistiken (nur Admin)\n\n"
            
            "**📅 Kalender-Befehle:**\n"
            "/today - Heutige Termine anzeigen\n"
            "/tomorrow - Morgige Termine anzeigen\n"
            "/week - Termine dieser Woche\n"
            "/next - Nächster anstehender Termin\n\n"
            
            "**� Natürliche Sprache:**\n"
            "Du kannst auch einfach schreiben:\n"
            "• 'Termin morgen 15 Uhr Meeting mit Team'\n"
            "• 'Was habe ich heute?'\n"
            "• 'Wann ist mein nächster Termin?'\n\n"
            
            "**🤖 KI-Chat:**\n"
            "Stelle mir Fragen und ich antworte mit KI:\n"
            "• 'Wie wird das Wetter?'\n"
            "• 'Erkläre mir Quantenphysik'\n"
            "• 'Schreibe einen Brief an...'\n\n"
            
            "Für mehr Details: /features"
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
            "✅ KI-Modelle (OpenRouter + HuggingFace)\n"
            "✅ Calendar Management (Google/iCloud/Mock)\n"
            "✅ Natürliche Sprachverarbeitung (Deutsch)\n"
            "🚧 Sprachverarbeitung (in Entwicklung)\n\n"
            "**GitHub:** https://github.com/WVUSAAH-Copilot-test/AdonisAI\n"
            "**Lizenz:** MIT\n\n"
            "Made with ❤️ by WVUSAAH"
        )
        update.message.reply_text(info_text, parse_mode='Markdown')
        logger.info(f"Info angefordert von User: {update.effective_user.id}")
    
    def features_command(self, update: Update, context: CallbackContext) -> None:
        """
        Handler für den /features Befehl - Detaillierte Funktionsübersicht
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
        calendar_status = "✅ Aktiv" if self.calendar_provider else "❌ Inaktiv"
        ai_status = "✅ Aktiv" if self.ai_provider else "❌ Inaktiv"
        
        features_text = (
            "**AdonisAI - Alle Funktionen** 🚀\n\n"
            
            "**📅 KALENDER-MANAGEMENT** " + calendar_status + "\n"
            "• Termine anzeigen (heute/morgen/Woche)\n"
            "• Termine erstellen per Kommando oder Text\n"
            "• Natürliche Sprache verstehen:\n"
            "  'Termin morgen 15 Uhr Meeting'\n"
            "• Automatische Konflikt-Erkennung\n"
            "• Deutsche Datumsangaben:\n"
            "  heute, morgen, übermorgen, Montag...\n"
            "• Support für Google Calendar, iCloud, Mock\n\n"
            
            "**🤖 KI-ASSISTENT** " + ai_status + "\n"
            "• Intelligente Chat-Antworten\n"
            "• Zwei KI-Provider:\n"
            "  - OpenRouter (GPT-3.5-Turbo)\n"
            "  - HuggingFace (Open-Source Modelle)\n"
            "• Kontextverständnis\n"
            "• Deutsche Sprachunterstützung\n\n"
            
            "**💬 NATÜRLICHE SPRACHE**\n"
            "• Erkennt Absichten (Termin/Frage/etc.)\n"
            "• Extrahiert Datum, Zeit, Ort\n"
            "• Deutsche Zeitausdrücke:\n"
            "  'morgen um 15 Uhr'\n"
            "  'nächsten Montag'\n"
            "  'in 2 Stunden'\n\n"
            
            "**🔐 PRIVACY & SICHERHEIT**\n"
            "• Lokale Datenverarbeitung\n"
            "• Keine Daten an Dritte (außer gewählte KI)\n"
            "• Open Source & Transparent\n"
            "• SSL-verschlüsselte Kommunikation\n\n"
            
            "**🚧 IN ENTWICKLUNG**\n"
            "• Siri Shortcuts Integration\n"
            "• Sprachnachrichten verstehen\n"
            "• Sprachausgabe (TTS)\n"
            "• Erinnerungen & Notifications\n"
            "• Multi-User Support\n\n"
            
            "**❓ Fragen?**\n"
            "Schreib einfach eine Nachricht oder nutze /help"
        )
        update.message.reply_text(features_text, parse_mode='Markdown')
        logger.info(f"Features angefordert von User: {update.effective_user.id}")
    
    def myid_command(self, update: Update, context: CallbackContext) -> None:
        """
        Handler für den /myid Befehl - Zeigt User-ID an
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
        user = update.effective_user
        user_id = user.id
        username = user.username or "N/A"
        first_name = user.first_name or "N/A"
        
        myid_text = (
            f"🆔 **Deine Telegram Identität**\n\n"
            f"**User-ID:** `{user_id}`\n"
            f"**Username:** @{username}\n"
            f"**Name:** {first_name}\n\n"
            f"💡 **Für Admin-Zugriff:**\n"
            f"Füge folgende Zeile zu `.env` hinzu:\n"
            f"```\nADMIN_USER_ID={user_id}\n```\n\n"
            f"Danach kannst du Admin-Befehle wie `/shutdown` nutzen."
        )
        update.message.reply_text(myid_text, parse_mode='Markdown')
        logger.info(f"MyID angefordert von User: {user_id} (@{username})")
    
    @admin_only
    def stats_command(self, update: Update, context: CallbackContext) -> None:
        """
        Handler für den /stats Befehl - Zeigt Interaction Statistics (Admin only)
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
        user = update.effective_user
        
        try:
            # Hole Statistiken
            stats = self.interaction_logger.get_statistics(user_id=user.id)
            
            # Format Statistiken
            stats_text = (
                f"📊 **Personal AI Statistics**\n\n"
                f"🧠 **Training Dataset:**\n"
                f"• Total Interaktionen: {stats['total_interactions']}\n"
                f"• Trainierbare: {stats['trainable_interactions']}\n"
                f"• Sensibel (ausgeschlossen): {stats['total_interactions'] - stats['trainable_interactions']}\n\n"
                
                f"📅 **Zeitraum:**\n"
                f"• Von: {stats['date_range']['first'] or 'N/A'}\n"
                f"• Bis: {stats['date_range']['last'] or 'N/A'}\n\n"
                
                f"🎯 **Aktionen:**\n"
            )
            
            for action, count in sorted(stats['actions'].items(), key=lambda x: x[1], reverse=True):
                stats_text += f"• {action}: {count}x\n"
            
            stats_text += (
                f"\n💡 **Tipp:**\n"
                f"Je mehr du den Bot nutzt, desto besser kann\n"
                f"dein persönliches AI-Modell dich verstehen!\n\n"
                f"Aktueller Fortschritt: "
            )
            
            # Progress indicator
            trainable = stats['trainable_interactions']
            if trainable < 50:
                stats_text += f"🟡 {trainable}/50 (Minimum für Training)"
            elif trainable < 200:
                stats_text += f"🟢 {trainable}/200 (Gut für Basis-Training)"
            else:
                stats_text += f"🚀 {trainable}+ (Excellent für Fine-tuning!)"
            
            update.message.reply_text(stats_text, parse_mode='Markdown')
            logger.info(f"Stats angefordert von Admin: {user.id}")
            
        except Exception as e:
            logger.error(f"Stats command error: {e}")
            update.message.reply_text(
                "❌ Fehler beim Laden der Statistiken.\n"
                "Prüfe die Logs für Details."
            )
    
    @admin_only
    def shutdown_command(self, update: Update, context: CallbackContext) -> None:
        """
        Handler für den /shutdown Befehl - Beendet den Bot (Admin only)
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
        user = update.effective_user
        logger.warning(f"🛑 Bot shutdown initiated by admin: {user.id} (@{user.username})")
        
        update.message.reply_text(
            "🛑 **Bot wird heruntergefahren...**\n\n"
            "Auf Wiedersehen! 👋",
            parse_mode='Markdown'
        )
        
        # Kurze Verzögerung damit die Nachricht gesendet wird
        import time
        time.sleep(1)
        
        # Bot beenden
        logger.info("Bot wird beendet...")
        self.updater.stop()
        sys.exit(0)
    
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
        Handler für Textnachrichten - KI-basiert mit Kontext
        
        Args:
            update: Telegram Update Objekt
            context: Callback Context
        """
        user = update.effective_user
        message_text = update.message.text
        
        logger.info(f"Nachricht von {user.id}: {message_text}")
        
        # Speichere User-Nachricht im Kontext
        self.context_manager.add_message(user.id, 'user', message_text)
        
        # Wenn KI verfügbar: Lass KI die Anfrage analysieren und verarbeiten
        if self.ai_provider:
            try:
                # Hole Chat-Historie
                chat_history = self.context_manager.get_context(user.id)
                
                # Erstelle einen Kontext-Prompt für die KI
                system_prompt = self._build_system_prompt(message_text, chat_history)
                
                # KI analysiert die Anfrage MIT Kontext
                response = self.ai_provider.generate_response(
                    message_text,
                    context=system_prompt
                )
                
                # Speichere Bot-Antwort im Kontext
                self.context_manager.add_message(user.id, 'assistant', response)
                
                # 🧠 LOG INTERACTION - Für Personal AI Training
                self._log_interaction(
                    user=user,
                    user_input=message_text,
                    bot_output=response,
                    bot_action='ai_response',
                    chat_history=chat_history
                )
                
                # Verarbeite KI-Response
                self._process_ai_response(update, message_text, response)
                return
                
            except Exception as e:
                logger.error(f"KI-Fehler: {e}")
                # Fallback zu alter Logik
        
        # Fallback ohne KI (alte Logik)
        command_type = detect_command_type(message_text)
        
        if command_type == 'calendar' and self.calendar_provider:
            self._handle_calendar_message(update, message_text)
        else:
            update.message.reply_text(f"Echo: {message_text}")
    
    def _build_system_prompt(self, user_message: str, chat_history: list) -> str:
        """
        Erstellt System-Prompt für KI basierend auf verfügbaren Features und Chat-Historie
        
        Args:
            user_message: User-Nachricht
            chat_history: Liste von vorherigen Nachrichten
            
        Returns:
            System-Prompt String
        """
        calendar_status = "verfügbar" if self.calendar_provider else "nicht verfügbar"
        
        # Erstelle Kontext-Zusammenfassung aus Historie
        history_context = ""
        if len(chat_history) > 1:  # Mehr als nur aktuelle Nachricht
            history_context = "\n\n📝 VORHERIGE KONVERSATION (WICHTIG - LIES GENAU!):\n"
            for msg in chat_history[-8:-1]:  # Letzte 7 Nachrichten (ohne aktuelle)
                role = "👤 User" if msg['role'] == 'user' else "🤖 Du"
                history_context += f"{role}: {msg['content']}\n"
            history_context += "\n⚠️ WICHTIG: Berücksichtige ALLE Informationen aus dieser Historie für deine Antwort!\n"
        
        prompt = f"""Du bist AdonisAI, ein intelligenter persönlicher Assistent.

KALENDER-MANAGEMENT: {calendar_status}

KRITISCHE REGEL - KONTEXT VERSTEHEN:
Du MUSST die vorherige Konversation VOLLSTÄNDIG lesen und verstehen!
- Wenn User "Mittwoch" sagt und vorher "nächste Woche" erwähnte → MERKE: nächsten Mittwoch!
- Wenn User einen Namen erwähnt (z.B. "Kunde Max") → MERKE den Namen für später!
- Wenn User "die genannten Tage prüfen" sagt → Schau was vorher genannt wurde!
- Kombiniere ALLE Informationen aus der Historie zu einem vollständigen Bild!
{history_context}
TERMIN-ERSTELLUNG REGELN:
1. Erstelle NUR einen Termin bei EXPLIZITER Aufforderung mit komplettem Datum/Zeit
2. Bei unvollständigen Infos → Stelle GEZIELTE Fragen
3. Bei Termin-Erstellung → Nutze ALLE Infos aus der Konversation (Namen, Kontext, etc.)

WENN User einen Termin erstellen möchte (mit vollständigen Infos):
Kombiniere ALLE Informationen aus der Konversation:
- Datum/Zeit aus aktueller ODER früherer Nachricht
- Namen/Beschreibung aus früheren Nachrichten
- Erstelle vollständigen Text der ALLE Details enthält

Dann antworte:
{{"action": "create_event", "text": "Termin [vollständiges Datum] [Uhrzeit] mit [Name/Details aus Historie]"}}

BEISPIEL mit Historie:
User1: "Kunde Max möchte nächste Woche Montag oder Mittwoch"
Du: "Welcher Tag passt besser?"
User2: "Mittwoch"
Du: "Welche Uhrzeit?"
User3: "14 Uhr"
→ {{"action": "create_event", "text": "Termin nächsten Mittwoch 14 Uhr mit Kunde Max"}}
(NICHT nur "Termin Mittwoch 14 Uhr" - sondern MIT Name aus User1!)

WENN User Termine sehen will:
{{"action": "list_events", "timeframe": "today|tomorrow|week"}}

SONST: Antworte hilfreich, aber KURZ und PRÄZISE!

Aktuelle User-Nachricht: "{user_message}"

Analysiere JETZT die GESAMTE Konversation und antworte:"""
        
        return prompt
    
    def _process_ai_response(self, update: Update, original_message: str, ai_response: str) -> None:
        """
        Verarbeitet KI-Response und führt entsprechende Aktionen aus
        
        Args:
            update: Telegram Update
            original_message: Original User-Nachricht
            ai_response: KI-Antwort
        """
        import json
        import re
        
        # Versuche JSON-Action zu extrahieren
        json_match = re.search(r'\{[^}]+\}', ai_response)
        
        if json_match:
            try:
                action_data = json.loads(json_match.group(0))
                action = action_data.get('action')
                
                if action == 'create_event' and self.calendar_provider:
                    # Erstelle Termin
                    self._handle_calendar_message(update, original_message)
                    return
                
                elif action == 'list_events' and self.calendar_provider:
                    # Liste Termine
                    timeframe = action_data.get('timeframe', 'today')
                    
                    if timeframe == 'today':
                        self.today_command(update, None)
                    elif timeframe == 'tomorrow':
                        self.tomorrow_command(update, None)
                    elif timeframe == 'week':
                        self.week_command(update, None)
                    return
                
                elif action == 'next_event' and self.calendar_provider:
                    # Zeige nächsten Termin
                    self.next_command(update, None)
                    return
                    
            except json.JSONDecodeError:
                pass  # Kein valides JSON, fahre mit normaler Antwort fort
        
        # Normale Text-Antwort
        update.message.reply_text(ai_response)
    
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
    
    def _log_interaction(
        self,
        user,
        user_input: str,
        bot_output: str,
        bot_action: Optional[str] = None,
        chat_history: Optional[list] = None,
        is_sensitive: bool = False
    ) -> None:
        """
        Speichert eine Bot-Interaktion für Personal AI Training
        
        Args:
            user: Telegram User Objekt
            user_input: User-Nachricht
            bot_output: Bot-Antwort
            bot_action: Art der Aktion (create_event, answer_question, etc.)
            chat_history: Vorherige Konversation
            is_sensitive: Ob diese Nachricht sensibel ist (kein Training)
        """
        try:
            # Context-Daten sammeln
            context_data = {
                'timestamp': datetime.now().isoformat(),
                'weekday': datetime.now().strftime('%A'),
                'hour': datetime.now().hour,
                'has_calendar': self.calendar_provider is not None,
                'has_ai': self.ai_provider is not None
            }
            
            # Log to database
            self.interaction_logger.log_interaction(
                user_id=user.id,
                user_input=user_input,
                bot_output=bot_output,
                username=user.username,
                user_input_type='text',
                bot_action=bot_action,
                context_data=context_data,
                conversation_history=chat_history,
                is_sensitive=is_sensitive
            )
            
        except Exception as e:
            # Logging-Fehler sollen Bot nicht unterbrechen
            logger.warning(f"⚠️ Interaction logging failed: {e}")
    
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
        dispatcher.add_handler(CommandHandler("features", self.features_command))
        dispatcher.add_handler(CommandHandler("myid", self.myid_command))
        
        # Command Handler - Admin
        dispatcher.add_handler(CommandHandler("shutdown", self.shutdown_command))
        dispatcher.add_handler(CommandHandler("stats", self.stats_command))
        
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
        # Updater mit erweiterten Timeouts erstellen (für Corporate Networks)
        logger.info("🔌 Verbinde mit Telegram API...")
        self.updater = Updater(
            token=self.token, 
            use_context=True,
            request_kwargs={
                'read_timeout': 10,
                'connect_timeout': 10
            }
        )
        
        # Handler registrieren
        self.setup_handlers()
        
        # Bot starten
        logger.info("🤖 AdonisAI Bot wird gestartet...")
        try:
            self.updater.start_polling(timeout=10)
            logger.info("✅ Bot läuft und wartet auf Nachrichten!")
            logger.info("📱 Öffne Telegram und sende /start an deinen Bot")
            self.updater.idle()
        except Exception as e:
            logger.error(f"❌ Fehler beim Polling: {e}")
            raise


def create_bot(token: str) -> AdonisBot:
    """
    Factory-Funktion zum Erstellen einer Bot-Instanz
    
    Args:
        token: Telegram Bot API Token
        
    Returns:
        AdonisBot Instanz
    """
    return AdonisBot(token)

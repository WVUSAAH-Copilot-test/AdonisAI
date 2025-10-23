"""
Calendar Factory - Erstellt den richtigen Calendar Provider
"""

import os
import logging
from typing import Optional

from .calendar_client import CalendarClient
from .mock_provider import MockCalendarProvider

logger = logging.getLogger(__name__)


def create_calendar_provider(provider_type: Optional[str] = None) -> CalendarClient:
    """
    Factory-Funktion zum Erstellen des Calendar Providers
    
    Args:
        provider_type: 'google', 'icloud', 'mock' oder None (aus .env)
        
    Returns:
        CalendarClient-Instanz
    """
    
    # Provider-Typ aus .env wenn nicht angegeben
    if provider_type is None:
        provider_type = os.getenv('CALENDAR_PROVIDER', 'mock').lower()
    
    logger.info(f"📅 Erstelle Calendar Provider: {provider_type}")
    
    # Google Calendar
    if provider_type == 'google':
        try:
            from .google_provider import GoogleCalendarProvider
            
            credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', './credentials.json')
            token_file = os.getenv('GOOGLE_TOKEN_FILE', './token.pickle')
            
            if not os.path.exists(credentials_file):
                logger.warning(f"⚠️ credentials.json nicht gefunden - wechsle zu Mock")
                logger.info("💡 Siehe docs/GOOGLE_CALENDAR_SETUP.md für Setup")
                return MockCalendarProvider()
            
            provider = GoogleCalendarProvider(
                credentials_file=credentials_file,
                token_file=token_file
            )
            
            # Test-Verbindung
            if not provider.connect():
                logger.warning("⚠️ Google Calendar Verbindung fehlgeschlagen - wechsle zu Mock")
                return MockCalendarProvider()
            
            logger.info("✅ Google Calendar Provider aktiv")
            return provider
            
        except Exception as e:
            logger.error(f"❌ Google Calendar Fehler: {e}")
            logger.info("🔄 Fallback zu Mock Provider")
            return MockCalendarProvider()
    
    # iCloud Calendar
    elif provider_type == 'icloud':
        try:
            from .icloud_provider import iCloudCalendarProvider
            
            username = os.getenv('ICLOUD_USERNAME')
            password = os.getenv('ICLOUD_APP_PASSWORD')
            calendar_url = os.getenv('ICLOUD_CALENDAR_URL', 'https://caldav.icloud.com/')
            
            if not username or not password:
                logger.warning("⚠️ iCloud Credentials nicht gesetzt - wechsle zu Mock")
                logger.info("💡 Setze ICLOUD_USERNAME und ICLOUD_APP_PASSWORD in .env")
                return MockCalendarProvider()
            
            provider = iCloudCalendarProvider(
                username=username,
                password=password,
                calendar_url=calendar_url
            )
            
            # Test-Verbindung
            if not provider.connect():
                logger.warning("⚠️ iCloud Verbindung fehlgeschlagen - wechsle zu Mock")
                logger.info("💡 Siehe docs/ICLOUD_BLOCKED.md für bekannte Probleme")
                return MockCalendarProvider()
            
            logger.info("✅ iCloud Calendar Provider aktiv")
            return provider
            
        except Exception as e:
            logger.error(f"❌ iCloud Calendar Fehler: {e}")
            logger.info("🔄 Fallback zu Mock Provider")
            return MockCalendarProvider()
    
    # Mock Provider (Default)
    else:
        if provider_type != 'mock':
            logger.warning(f"⚠️ Unbekannter Provider '{provider_type}' - verwende Mock")
        
        logger.info("✅ Mock Calendar Provider aktiv (lokale Daten)")
        return MockCalendarProvider()


def get_available_providers() -> dict:
    """
    Gibt verfügbare Provider zurück
    
    Returns:
        Dict mit Provider-Namen und Status
    """
    providers = {
        'mock': {
            'available': True,
            'description': 'Lokaler Mock Provider (immer verfügbar)',
            'requires': []
        },
        'google': {
            'available': False,
            'description': 'Google Calendar via OAuth2',
            'requires': ['credentials.json', 'Google Cloud Projekt']
        },
        'icloud': {
            'available': False,
            'description': 'iCloud Calendar via CalDAV',
            'requires': ['ICLOUD_USERNAME', 'ICLOUD_APP_PASSWORD']
        }
    }
    
    # Google verfügbar?
    google_creds = os.getenv('GOOGLE_CREDENTIALS_FILE', './credentials.json')
    if os.path.exists(google_creds):
        providers['google']['available'] = True
    
    # iCloud verfügbar?
    icloud_user = os.getenv('ICLOUD_USERNAME')
    icloud_pass = os.getenv('ICLOUD_APP_PASSWORD')
    if icloud_user and icloud_pass:
        providers['icloud']['available'] = True
    
    return providers

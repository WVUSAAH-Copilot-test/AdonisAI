"""
NLP Utilities - Hilfsfunktionen für Natural Language Processing
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import dateparser

logger = logging.getLogger(__name__)


def parse_date(text: str, timezone: str = 'Europe/Berlin') -> Optional[datetime]:
    """
    Parst natürlichsprachliche Datums-/Zeitangaben
    
    Args:
        text: Text mit Datums-/Zeitangabe (z.B. "morgen um 15 Uhr")
        timezone: Zeitzone
        
    Returns:
        Datetime Objekt oder None
    """
    # TODO: Detaillierte Implementierung in Phase 3
    parsed_date = dateparser.parse(
        text,
        settings={'TIMEZONE': timezone, 'RETURN_AS_TIMEZONE_AWARE': True}
    )
    
    if parsed_date:
        logger.info(f"Datum geparst: {text} -> {parsed_date}")
    else:
        logger.warning(f"Konnte Datum nicht parsen: {text}")
    
    return parsed_date


def extract_keywords(text: str) -> list:
    """
    Extrahiert wichtige Keywords aus Text
    
    Args:
        text: Eingabetext
        
    Returns:
        Liste von Keywords
    """
    # TODO: Implementierung mit NLP-Bibliothek in Phase 2
    # Einfache Implementierung als Platzhalter
    words = text.lower().split()
    
    # Stopwörter filtern (vereinfacht)
    stopwords = {'der', 'die', 'das', 'ein', 'eine', 'und', 'oder', 'ist', 'sind'}
    keywords = [word for word in words if word not in stopwords and len(word) > 3]
    
    return keywords


def detect_command_type(text: str) -> str:
    """
    Erkennt den Typ eines Befehls
    
    Args:
        text: Benutzer-Eingabe
        
    Returns:
        Befehlstyp (z.B. 'calendar', 'reminder', 'question', 'general')
    """
    text_lower = text.lower()
    
    # Kalender-Keywords
    calendar_keywords = ['termin', 'kalendar', 'meeting', 'datum', 'morgen', 'heute']
    if any(keyword in text_lower for keyword in calendar_keywords):
        return 'calendar'
    
    # Erinnerungs-Keywords
    reminder_keywords = ['erinner', 'remind', 'vergiss nicht']
    if any(keyword in text_lower for keyword in reminder_keywords):
        return 'reminder'
    
    # Frage-Keywords
    question_keywords = ['wie', 'was', 'wann', 'wo', 'wer', 'warum']
    if any(text_lower.startswith(keyword) for keyword in question_keywords):
        return 'question'
    
    return 'general'


def clean_text(text: str) -> str:
    """
    Bereinigt Text von überflüssigen Zeichen
    
    Args:
        text: Eingabetext
        
    Returns:
        Bereinigter Text
    """
    # Mehrfache Leerzeichen entfernen
    cleaned = ' '.join(text.split())
    
    # Trim
    cleaned = cleaned.strip()
    
    return cleaned

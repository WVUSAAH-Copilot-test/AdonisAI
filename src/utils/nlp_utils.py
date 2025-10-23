"""
NLP Utilities - Hilfsfunktionen für Natural Language Processing
"""

import logging
import re
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
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
    
    Examples:
        >>> parse_date("morgen 15 Uhr")
        >>> parse_date("nächsten Montag um 10:00")
        >>> parse_date("in 2 Stunden")
    """
    parsed_date = dateparser.parse(
        text,
        settings={
            'TIMEZONE': timezone,
            'RETURN_AS_TIMEZONE_AWARE': False,
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': datetime.now()
        },
        languages=['de', 'en']
    )
    
    if parsed_date:
        logger.info(f"Datum geparst: '{text}' -> {parsed_date}")
    else:
        logger.warning(f"Konnte Datum nicht parsen: '{text}'")
    
    return parsed_date


def parse_event_from_text(text: str) -> Dict[str, Any]:
    """
    Extrahiert Event-Informationen aus natürlichsprachlichem Text
    
    Args:
        text: Benutzer-Eingabe (z.B. "Erstelle Termin morgen 15 Uhr Meeting mit Team")
        
    Returns:
        Dictionary mit Event-Daten: {
            'title': str,
            'start': datetime,
            'end': datetime,
            'duration_minutes': int,
            'location': str,
            'description': str,
            'raw_text': str
        }
    
    Examples:
        >>> parse_event_from_text("Meeting morgen 15 Uhr 1 Stunde")
        >>> parse_event_from_text("Arzttermin übermorgen 10:00 in der Klinik")
    """
    result = {
        'title': None,
        'start': None,
        'end': None,
        'duration_minutes': 60,  # Default: 1 Stunde
        'location': None,
        'description': None,
        'raw_text': text
    }
    
    # 1. Zeit/Datum extrahieren
    time_info = extract_datetime_from_text(text)
    if time_info:
        result['start'] = time_info['start']
        result['duration_minutes'] = time_info['duration_minutes']
        if time_info['end']:
            result['end'] = time_info['end']
        else:
            result['end'] = result['start'] + timedelta(minutes=result['duration_minutes'])
    
    # 2. Ort extrahieren
    location = extract_location_from_text(text)
    if location:
        result['location'] = location
    
    # 3. Titel extrahieren
    title = extract_event_title(text)
    if title:
        result['title'] = title
    else:
        # Fallback: Erste paar Wörter
        words = text.split()[:5]
        result['title'] = ' '.join(words)
    
    logger.info(f"Event geparst: {result['title']} @ {result['start']}")
    
    return result


def extract_datetime_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extrahiert Datum, Uhrzeit und Dauer aus Text
    
    Returns:
        {
            'start': datetime,
            'end': datetime or None,
            'duration_minutes': int
        }
    """
    # Relative Zeitangaben (heute, morgen, übermorgen)
    now = datetime.now()
    relative_dates = {
        'heute': now.replace(hour=0, minute=0, second=0, microsecond=0),
        'morgen': now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
        'übermorgen': now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=2),
    }
    
    base_date = None
    for key, value in relative_dates.items():
        if key in text.lower():
            base_date = value
            break
    
    # Wenn keine relative Angabe, versuche Wochentag
    if not base_date:
        weekdays = {
            'montag': 0, 'dienstag': 1, 'mittwoch': 2, 'donnerstag': 3,
            'freitag': 4, 'samstag': 5, 'sonntag': 6
        }
        for day_name, day_num in weekdays.items():
            if day_name in text.lower():
                days_ahead = (day_num - now.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7  # Nächste Woche
                base_date = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_ahead)
                break
    
    # Default: heute
    if not base_date:
        base_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Uhrzeit extrahieren (z.B. "15 Uhr", "15:30", "10.00")
    time_patterns = [
        r'(\d{1,2}):(\d{2})\s*(?:uhr)?',  # 15:30 Uhr
        r'(\d{1,2})\.(\d{2})\s*(?:uhr)?',  # 15.30 Uhr
        r'(\d{1,2})\s*uhr',                # 15 Uhr
        r'um\s*(\d{1,2}):?(\d{2})?',       # um 15:30
    ]
    
    hour = 9  # Default
    minute = 0
    
    for pattern in time_patterns:
        match = re.search(pattern, text.lower())
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.lastindex >= 2 and match.group(2) else 0
            break
    
    start_time = base_date.replace(hour=hour, minute=minute)
    
    # Dauer extrahieren (z.B. "1 Stunde", "30 Minuten", "2h")
    duration_minutes = 60  # Default
    
    duration_patterns = [
        (r'(\d+)\s*stunde[n]?', 60),      # 2 Stunden
        (r'(\d+)\s*h\b', 60),              # 2h
        (r'(\d+)\s*minute[n]?', 1),       # 30 Minuten
        (r'(\d+)\s*min\b', 1),             # 30min
    ]
    
    for pattern, multiplier in duration_patterns:
        match = re.search(pattern, text.lower())
        if match:
            duration_minutes = int(match.group(1)) * multiplier
            break
    
    end_time = start_time + timedelta(minutes=duration_minutes)
    
    return {
        'start': start_time,
        'end': end_time,
        'duration_minutes': duration_minutes
    }


def extract_location_from_text(text: str) -> Optional[str]:
    """
    Extrahiert Ort/Location aus Text
    
    Examples:
        "Meeting in Room 302"
        "Termin bei der Bank"
        "Arztbesuch in der Klinik"
    """
    location_patterns = [
        r'(?:in|im|bei)\s+(?:der\s+)?(.+?)(?:\s+um|\s+am|\s+morgen|$)',
        r'(?:@|bei)\s*([^\s]+)',
        r'location:\s*(.+?)(?:\s|$)',
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, text.lower())
        if match:
            location = match.group(1).strip()
            # Bereinige häufige Füllwörter
            location = re.sub(r'\s*(um|am|morgen|heute|termin|meeting).*$', '', location)
            if len(location) > 2:
                logger.info(f"Ort extrahiert: '{location}'")
                return location
    
    return None


def extract_event_title(text: str) -> Optional[str]:
    """
    Extrahiert Event-Titel aus Text
    
    Filtert Command-Keywords und Zeit/Ort-Angaben raus
    """
    # Entferne Command-Keywords
    command_keywords = [
        'erstelle', 'create', 'neuer', 'termin', 'meeting', 'event',
        'mach', 'plane', 'einplanen'
    ]
    
    words = text.split()
    filtered_words = []
    
    skip_next = False
    for i, word in enumerate(words):
        if skip_next:
            skip_next = False
            continue
        
        word_lower = word.lower()
        
        # Überspringe Command-Keywords
        if word_lower in command_keywords:
            continue
        
        # Überspringe Zeit-Keywords
        if word_lower in ['morgen', 'heute', 'übermorgen', 'um', 'uhr', 'in', 'bei', 'im']:
            continue
        
        # Überspringe Zahlen (wahrscheinlich Uhrzeit)
        if word_lower.replace(':', '').replace('.', '').isdigit():
            continue
        
        # Überspringe Zeiteinheiten
        if any(unit in word_lower for unit in ['stunde', 'minute', 'min', 'std']):
            continue
        
        filtered_words.append(word)
        
        # Stop bei max 6 Wörtern für Titel
        if len(filtered_words) >= 6:
            break
    
    if filtered_words:
        title = ' '.join(filtered_words)
        logger.info(f"Titel extrahiert: '{title}'")
        return title
    
    return None


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

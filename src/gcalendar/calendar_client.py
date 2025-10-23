"""
Calendar Client - Abstract Base Class für verschiedene Calendar Provider
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CalendarEvent:
    """
    Einheitliche Event-Repräsentation für alle Calendar Provider
    """
    
    def __init__(self, 
                 uid: str,
                 title: str,
                 start: datetime,
                 end: datetime,
                 location: Optional[str] = None,
                 description: Optional[str] = None,
                 attendees: Optional[List[str]] = None,
                 raw_event: Any = None):
        """
        Args:
            uid: Unique Event ID
            title: Event-Titel
            start: Startzeit
            end: Endzeit
            location: Ort (optional)
            description: Beschreibung (optional)
            attendees: Teilnehmer (optional)
            raw_event: Original Event-Objekt vom Provider
        """
        self.uid = uid
        self.title = title
        self.start = start
        self.end = end
        self.location = location
        self.description = description
        self.attendees = attendees or []
        self.raw_event = raw_event
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert Event zu Dictionary"""
        return {
            'uid': self.uid,
            'title': self.title,
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'location': self.location,
            'description': self.description,
            'attendees': self.attendees,
            'duration_minutes': int((self.end - self.start).total_seconds() / 60)
        }
    
    def __repr__(self):
        return f"CalendarEvent('{self.title}', {self.start.strftime('%Y-%m-%d %H:%M')})"


class CalendarClient(ABC):
    """
    Abstract Base Class für Calendar Provider
    Definiert die Interface für alle Calendar-Operationen
    """
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Verbindet zum Calendar Service
        
        Returns:
            True bei erfolgreicher Verbindung
        """
        pass
    
    @abstractmethod
    def list_events(self, 
                    start_date: datetime, 
                    end_date: datetime) -> List[CalendarEvent]:
        """
        Listet Events in einem Zeitraum
        
        Args:
            start_date: Start des Zeitraums
            end_date: Ende des Zeitraums
            
        Returns:
            Liste von CalendarEvent-Objekten
        """
        pass
    
    @abstractmethod
    def create_event(self,
                     title: str,
                     start: datetime,
                     end: datetime,
                     location: Optional[str] = None,
                     description: Optional[str] = None,
                     attendees: Optional[List[str]] = None) -> CalendarEvent:
        """
        Erstellt ein neues Event
        
        Args:
            title: Event-Titel
            start: Startzeit
            end: Endzeit
            location: Ort (optional)
            description: Beschreibung (optional)
            attendees: Teilnehmer (optional)
            
        Returns:
            Erstelltes CalendarEvent
        """
        pass
    
    @abstractmethod
    def update_event(self,
                     event_uid: str,
                     title: Optional[str] = None,
                     start: Optional[datetime] = None,
                     end: Optional[datetime] = None,
                     location: Optional[str] = None,
                     description: Optional[str] = None) -> CalendarEvent:
        """
        Aktualisiert ein existierendes Event
        
        Args:
            event_uid: Event ID
            title: Neuer Titel (optional)
            start: Neue Startzeit (optional)
            end: Neue Endzeit (optional)
            location: Neuer Ort (optional)
            description: Neue Beschreibung (optional)
            
        Returns:
            Aktualisiertes CalendarEvent
        """
        pass
    
    @abstractmethod
    def delete_event(self, event_uid: str) -> bool:
        """
        Löscht ein Event
        
        Args:
            event_uid: Event ID
            
        Returns:
            True bei Erfolg
        """
        pass
    
    def check_conflicts(self, 
                       start: datetime, 
                       end: datetime,
                       exclude_uid: Optional[str] = None) -> Dict[str, Any]:
        """
        Prüft ob ein Zeitraum mit existierenden Events kollidiert
        
        Args:
            start: Startzeit des neuen Events
            end: Endzeit des neuen Events
            exclude_uid: Event-ID die ignoriert werden soll (für Updates)
            
        Returns:
            Dictionary mit Konflikt-Informationen
        """
        try:
            # Hole Events im relevanten Zeitraum
            events = self.list_events(start, end)
            
            conflicts = []
            for event in events:
                # Überspringe das Event das wir updaten
                if exclude_uid and event.uid == exclude_uid:
                    continue
                
                # Prüfe Überlappung
                if (start < event.end and end > event.start):
                    conflicts.append(event)
            
            return {
                'has_conflict': len(conflicts) > 0,
                'conflicts': conflicts,
                'count': len(conflicts),
                'warning': f'⚠️ Überschneidet sich mit {len(conflicts)} Termin(en)' if conflicts else None
            }
            
        except Exception as e:
            logger.error(f"Fehler bei Konflikt-Prüfung: {e}")
            return {
                'has_conflict': False,
                'conflicts': [],
                'count': 0,
                'error': str(e)
            }


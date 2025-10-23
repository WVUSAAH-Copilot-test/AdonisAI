"""
Mock Calendar Provider - Für lokale Tests ohne Internet
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid

from .calendar_client import CalendarClient, CalendarEvent

logger = logging.getLogger(__name__)


class MockCalendarProvider(CalendarClient):
    """
    Mock Calendar Provider für Tests
    Speichert Events nur im Memory (nicht persistent)
    """
    
    def __init__(self):
        """
        Initialisiert Mock Calendar Provider
        """
        self.events = {}  # Dict[uid: CalendarEvent]
        self.connected = False
        
        # Beispiel-Events erstellen
        self._create_sample_events()
        
        logger.info("Mock Calendar Provider initialisiert")
    
    def _create_sample_events(self):
        """Erstellt einige Beispiel-Events für Tests"""
        base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        # Event 1: Heute 10:00 - 11:00
        event1 = CalendarEvent(
            uid=str(uuid.uuid4()),
            title="Daily Standup",
            start=base_date.replace(hour=10),
            end=base_date.replace(hour=11),
            location="Office",
            description="Tägliches Team-Meeting"
        )
        self.events[event1.uid] = event1
        
        # Event 2: Heute 14:00 - 15:30
        event2 = CalendarEvent(
            uid=str(uuid.uuid4()),
            title="Client Meeting",
            start=base_date.replace(hour=14),
            end=base_date.replace(hour=15, minute=30),
            location="Conference Room A",
            description="Projekt-Review mit Kunde"
        )
        self.events[event2.uid] = event2
        
        # Event 3: Morgen 15:00 - 16:00
        tomorrow = base_date + timedelta(days=1)
        event3 = CalendarEvent(
            uid=str(uuid.uuid4()),
            title="Code Review",
            start=tomorrow.replace(hour=15),
            end=tomorrow.replace(hour=16),
            description="AdonisAI Phase 3 Review"
        )
        self.events[event3.uid] = event3
        
        # Event 4: Nächste Woche Montag 9:00 - 10:00
        next_week = base_date + timedelta(days=7)
        event4 = CalendarEvent(
            uid=str(uuid.uuid4()),
            title="Sprint Planning",
            start=next_week.replace(hour=9),
            end=next_week.replace(hour=10),
            location="Virtual",
            description="Planung für nächsten Sprint"
        )
        self.events[event4.uid] = event4
        
        logger.info(f"📅 {len(self.events)} Beispiel-Events erstellt")
    
    def connect(self) -> bool:
        """
        Mock-Verbindung (immer erfolgreich)
        
        Returns:
            True
        """
        self.connected = True
        logger.info("✅ Mock Calendar verbunden")
        return True
    
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
        if not self.connected:
            self.connect()
        
        # Filtere Events im Zeitraum
        filtered_events = []
        
        for event in self.events.values():
            # Event liegt im Zeitraum wenn:
            # - Event-Start < Zeitraum-Ende UND
            # - Event-Ende > Zeitraum-Start
            if event.start < end_date and event.end > start_date:
                filtered_events.append(event)
        
        # Sortiere nach Startzeit
        filtered_events.sort(key=lambda e: e.start)
        
        logger.info(f"📅 {len(filtered_events)} Events gefunden ({start_date.date()} - {end_date.date()})")
        return filtered_events
    
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
        if not self.connected:
            self.connect()
        
        # Event erstellen
        uid = str(uuid.uuid4())
        
        event = CalendarEvent(
            uid=uid,
            title=title,
            start=start,
            end=end,
            location=location,
            description=description,
            attendees=attendees or []
        )
        
        # Speichern
        self.events[uid] = event
        
        logger.info(f"✅ Event erstellt: '{title}' ({start} - {end})")
        return event
    
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
        if not self.connected:
            self.connect()
        
        if event_uid not in self.events:
            raise ValueError(f"Event mit UID {event_uid} nicht gefunden")
        
        # Event aktualisieren
        event = self.events[event_uid]
        
        if title:
            event.title = title
        if start:
            event.start = start
        if end:
            event.end = end
        if location is not None:
            event.location = location
        if description is not None:
            event.description = description
        
        logger.info(f"✅ Event aktualisiert: {event_uid}")
        return event
    
    def delete_event(self, event_uid: str) -> bool:
        """
        Löscht ein Event
        
        Args:
            event_uid: Event ID
            
        Returns:
            True bei Erfolg
        """
        if not self.connected:
            self.connect()
        
        if event_uid not in self.events:
            logger.warning(f"Event {event_uid} nicht gefunden")
            return False
        
        # Event löschen
        del self.events[event_uid]
        
        logger.info(f"✅ Event gelöscht: {event_uid}")
        return True
    
    def reset(self):
        """Setzt alle Events zurück (für Tests)"""
        self.events.clear()
        self._create_sample_events()
        logger.info("🔄 Mock Calendar zurückgesetzt")
    
    def get_all_events(self) -> List[CalendarEvent]:
        """Gibt alle Events zurück (Debug-Funktion)"""
        return sorted(self.events.values(), key=lambda e: e.start)

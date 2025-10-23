"""
iCloud Calendar Provider - CalDAV Integration
"""

import os
import ssl
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import caldav
from icalendar import Calendar as iCalendar, Event as iEvent
from recurring_ical_events import of
from .calendar_client import CalendarClient, CalendarEvent

logger = logging.getLogger(__name__)


class iCloudCalendarProvider(CalendarClient):
    """
    iCloud Calendar Provider über CalDAV
    """
    
    def __init__(self, 
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 calendar_url: Optional[str] = None):
        """
        Initialisiert iCloud Calendar Provider
        
        Args:
            username: iCloud Email (oder aus .env)
            password: App-spezifisches Passwort (oder aus .env)
            calendar_url: CalDAV URL (oder aus .env)
        """
        self.username = username or os.getenv('ICLOUD_USERNAME')
        self.password = password or os.getenv('ICLOUD_APP_PASSWORD')
        self.calendar_url = calendar_url or os.getenv(
            'ICLOUD_CALENDAR_URL',
            'https://caldav.icloud.com/'
        )
        
        self.client = None
        self.principal = None
        self.calendar = None
        
        logger.info(f"iCloud Provider initialisiert für {self.username}")
    
    def connect(self) -> bool:
        """
        Verbindet zum iCloud CalDAV Server
        
        Returns:
            True bei erfolgreicher Verbindung
        """
        try:
            # SSL Context für Corporate Network
            ssl_context = ssl._create_unverified_context()
            
            # CalDAV Client erstellen
            self.client = caldav.DAVClient(
                url=self.calendar_url,
                username=self.username,
                password=self.password,
                ssl_verify_cert=False
            )
            
            # Principal abrufen (Benutzer-Account)
            self.principal = self.client.principal()
            
            # Standard-Kalender auswählen
            calendars = self.principal.calendars()
            
            if not calendars:
                logger.error("Keine Kalender gefunden!")
                return False
            
            # Ersten Kalender verwenden (meistens der Haupt-Kalender)
            self.calendar = calendars[0]
            
            logger.info(f"✅ Verbunden mit iCloud Calendar: {self.calendar.name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ iCloud Verbindung fehlgeschlagen: {e}")
            return False
    
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
        if not self.calendar:
            logger.warning("Nicht verbunden - rufe connect() auf")
            if not self.connect():
                return []
        
        try:
            # Events abrufen
            events = self.calendar.date_search(start=start_date, end=end_date)
            
            calendar_events = []
            
            for event in events:
                try:
                    # iCal parsen
                    ical = iCalendar.from_ical(event.data)
                    
                    # Alle VEVENT Komponenten durchgehen
                    for component in ical.walk():
                        if component.name == "VEVENT":
                            # Event-Daten extrahieren
                            uid = str(component.get('UID', ''))
                            title = str(component.get('SUMMARY', 'Unbenannt'))
                            start = component.get('DTSTART').dt
                            end = component.get('DTEND').dt
                            
                            # Datetime-Konvertierung falls nötig
                            if not isinstance(start, datetime):
                                start = datetime.combine(start, datetime.min.time())
                            if not isinstance(end, datetime):
                                end = datetime.combine(end, datetime.min.time())
                            
                            location = str(component.get('LOCATION', '')) or None
                            description = str(component.get('DESCRIPTION', '')) or None
                            
                            # Attendees extrahieren
                            attendees = []
                            if 'ATTENDEE' in component:
                                attendee_list = component.get('ATTENDEE')
                                if not isinstance(attendee_list, list):
                                    attendee_list = [attendee_list]
                                
                                for att in attendee_list:
                                    attendees.append(str(att))
                            
                            # CalendarEvent erstellen
                            calendar_event = CalendarEvent(
                                uid=uid,
                                title=title,
                                start=start,
                                end=end,
                                location=location,
                                description=description,
                                attendees=attendees,
                                raw_event=event
                            )
                            
                            calendar_events.append(calendar_event)
                
                except Exception as e:
                    logger.warning(f"Event konnte nicht geparst werden: {e}")
                    continue
            
            logger.info(f"📅 {len(calendar_events)} Events gefunden ({start_date.date()} - {end_date.date()})")
            return calendar_events
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen von Events: {e}")
            return []
    
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
        if not self.calendar:
            logger.warning("Nicht verbunden - rufe connect() auf")
            if not self.connect():
                raise ConnectionError("Verbindung zu iCloud fehlgeschlagen")
        
        try:
            # iCal Event erstellen
            ical = iCalendar()
            event = iEvent()
            
            # Event-Daten setzen
            event.add('SUMMARY', title)
            event.add('DTSTART', start)
            event.add('DTEND', end)
            
            if location:
                event.add('LOCATION', location)
            
            if description:
                event.add('DESCRIPTION', description)
            
            if attendees:
                for attendee in attendees:
                    event.add('ATTENDEE', attendee)
            
            # UID generieren
            import uuid
            uid = f"{uuid.uuid4()}@adonisai"
            event.add('UID', uid)
            
            # Timestamp
            event.add('DTSTAMP', datetime.now())
            
            # Event zum Calendar hinzufügen
            ical.add_component(event)
            
            # Event in iCloud speichern
            self.calendar.save_event(ical.to_ical().decode('utf-8'))
            
            logger.info(f"✅ Event erstellt: '{title}' ({start} - {end})")
            
            # CalendarEvent zurückgeben
            return CalendarEvent(
                uid=uid,
                title=title,
                start=start,
                end=end,
                location=location,
                description=description,
                attendees=attendees or []
            )
            
        except Exception as e:
            logger.error(f"❌ Event-Erstellung fehlgeschlagen: {e}")
            raise
    
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
        if not self.calendar:
            logger.warning("Nicht verbunden - rufe connect() auf")
            if not self.connect():
                raise ConnectionError("Verbindung zu iCloud fehlgeschlagen")
        
        try:
            # Event suchen
            events = self.calendar.events()
            target_event = None
            
            for event in events:
                ical = iCalendar.from_ical(event.data)
                for component in ical.walk():
                    if component.name == "VEVENT":
                        if str(component.get('UID', '')) == event_uid:
                            target_event = event
                            break
                if target_event:
                    break
            
            if not target_event:
                raise ValueError(f"Event mit UID {event_uid} nicht gefunden")
            
            # Event updaten
            ical = iCalendar.from_ical(target_event.data)
            
            for component in ical.walk():
                if component.name == "VEVENT":
                    if title:
                        component['SUMMARY'] = title
                    if start:
                        component['DTSTART'] = start
                    if end:
                        component['DTEND'] = end
                    if location is not None:
                        component['LOCATION'] = location
                    if description is not None:
                        component['DESCRIPTION'] = description
                    
                    # Timestamp aktualisieren
                    component['DTSTAMP'] = datetime.now()
            
            # Speichern
            target_event.data = ical.to_ical()
            target_event.save()
            
            logger.info(f"✅ Event aktualisiert: {event_uid}")
            
            # Aktualisiertes Event zurückgeben
            for component in ical.walk():
                if component.name == "VEVENT":
                    return CalendarEvent(
                        uid=event_uid,
                        title=str(component.get('SUMMARY', '')),
                        start=component.get('DTSTART').dt,
                        end=component.get('DTEND').dt,
                        location=str(component.get('LOCATION', '')) or None,
                        description=str(component.get('DESCRIPTION', '')) or None,
                        raw_event=target_event
                    )
            
        except Exception as e:
            logger.error(f"❌ Event-Update fehlgeschlagen: {e}")
            raise
    
    def delete_event(self, event_uid: str) -> bool:
        """
        Löscht ein Event
        
        Args:
            event_uid: Event ID
            
        Returns:
            True bei Erfolg
        """
        if not self.calendar:
            logger.warning("Nicht verbunden - rufe connect() auf")
            if not self.connect():
                return False
        
        try:
            # Event suchen
            events = self.calendar.events()
            
            for event in events:
                ical = iCalendar.from_ical(event.data)
                for component in ical.walk():
                    if component.name == "VEVENT":
                        if str(component.get('UID', '')) == event_uid:
                            # Event löschen
                            event.delete()
                            logger.info(f"✅ Event gelöscht: {event_uid}")
                            return True
            
            logger.warning(f"Event {event_uid} nicht gefunden")
            return False
            
        except Exception as e:
            logger.error(f"❌ Event-Löschung fehlgeschlagen: {e}")
            return False

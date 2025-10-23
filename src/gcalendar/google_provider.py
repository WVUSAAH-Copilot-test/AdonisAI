"""
Google Calendar Provider - OAuth2 Integration
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .calendar_client import CalendarClient, CalendarEvent

logger = logging.getLogger(__name__)

# Scopes für Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarProvider(CalendarClient):
    """
    Google Calendar Provider mit OAuth2
    """
    
    def __init__(self, 
                 credentials_file: Optional[str] = None,
                 token_file: Optional[str] = None):
        """
        Initialisiert Google Calendar Provider
        
        Args:
            credentials_file: Pfad zur credentials.json (OAuth Client)
            token_file: Pfad zur token.pickle (gespeicherte Credentials)
        """
        self.credentials_file = credentials_file or os.getenv(
            'GOOGLE_CREDENTIALS_FILE', 
            './credentials.json'
        )
        self.token_file = token_file or os.getenv(
            'GOOGLE_TOKEN_FILE',
            './token.pickle'
        )
        
        self.creds = None
        self.service = None
        
        logger.info("Google Calendar Provider initialisiert")
    
    def connect(self) -> bool:
        """
        Verbindet zu Google Calendar via OAuth2
        
        Returns:
            True bei erfolgreicher Verbindung
        """
        try:
            # Token laden falls vorhanden
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    self.creds = pickle.load(token)
            
            # Token erneuern oder neu authentifizieren
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    logger.info("🔄 Refresh Google Token...")
                    self.creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        logger.error(f"❌ credentials.json nicht gefunden: {self.credentials_file}")
                        logger.info("💡 Erstelle credentials.json über Google Cloud Console:")
                        logger.info("   https://console.cloud.google.com/apis/credentials")
                        return False
                    
                    logger.info("🔐 Starte OAuth2 Flow...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)
                
                # Token speichern
                with open(self.token_file, 'wb') as token:
                    pickle.dump(self.creds, token)
            
            # Service erstellen
            self.service = build('calendar', 'v3', credentials=self.creds)
            
            logger.info("✅ Mit Google Calendar verbunden")
            return True
            
        except Exception as e:
            logger.error(f"❌ Google Calendar Verbindung fehlgeschlagen: {e}")
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
        if not self.service:
            logger.warning("Nicht verbunden - rufe connect() auf")
            if not self.connect():
                return []
        
        try:
            # RFC3339 Format für Google API
            time_min = start_date.isoformat() + 'Z'
            time_max = end_date.isoformat() + 'Z'
            
            # Events abrufen
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            calendar_events = []
            
            for event in events:
                # Start/End Time parsen
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                # String zu datetime
                if isinstance(start, str):
                    start = datetime.fromisoformat(start.replace('Z', '+00:00'))
                if isinstance(end, str):
                    end = datetime.fromisoformat(end.replace('Z', '+00:00'))
                
                # Attendees extrahieren
                attendees = []
                if 'attendees' in event:
                    attendees = [att.get('email', '') for att in event['attendees']]
                
                # CalendarEvent erstellen
                calendar_event = CalendarEvent(
                    uid=event['id'],
                    title=event.get('summary', 'Unbenannt'),
                    start=start,
                    end=end,
                    location=event.get('location'),
                    description=event.get('description'),
                    attendees=attendees,
                    raw_event=event
                )
                
                calendar_events.append(calendar_event)
            
            logger.info(f"📅 {len(calendar_events)} Events gefunden ({start_date.date()} - {end_date.date()})")
            return calendar_events
            
        except HttpError as e:
            logger.error(f"Google Calendar API Fehler: {e}")
            return []
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
        if not self.service:
            logger.warning("Nicht verbunden - rufe connect() auf")
            if not self.connect():
                raise ConnectionError("Verbindung zu Google Calendar fehlgeschlagen")
        
        try:
            # Event-Objekt erstellen
            event = {
                'summary': title,
                'start': {
                    'dateTime': start.isoformat(),
                    'timeZone': 'Europe/Vienna',
                },
                'end': {
                    'dateTime': end.isoformat(),
                    'timeZone': 'Europe/Vienna',
                },
            }
            
            if location:
                event['location'] = location
            
            if description:
                event['description'] = description
            
            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]
            
            # Event erstellen
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            logger.info(f"✅ Event erstellt: '{title}' ({start} - {end})")
            
            # CalendarEvent zurückgeben
            return CalendarEvent(
                uid=created_event['id'],
                title=title,
                start=start,
                end=end,
                location=location,
                description=description,
                attendees=attendees or [],
                raw_event=created_event
            )
            
        except HttpError as e:
            logger.error(f"❌ Event-Erstellung fehlgeschlagen: {e}")
            raise
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
        if not self.service:
            logger.warning("Nicht verbunden - rufe connect() auf")
            if not self.connect():
                raise ConnectionError("Verbindung zu Google Calendar fehlgeschlagen")
        
        try:
            # Aktuelles Event abrufen
            event = self.service.events().get(
                calendarId='primary',
                eventId=event_uid
            ).execute()
            
            # Updates anwenden
            if title:
                event['summary'] = title
            
            if start:
                event['start'] = {
                    'dateTime': start.isoformat(),
                    'timeZone': 'Europe/Vienna',
                }
            
            if end:
                event['end'] = {
                    'dateTime': end.isoformat(),
                    'timeZone': 'Europe/Vienna',
                }
            
            if location is not None:
                event['location'] = location
            
            if description is not None:
                event['description'] = description
            
            # Event updaten
            updated_event = self.service.events().update(
                calendarId='primary',
                eventId=event_uid,
                body=event
            ).execute()
            
            logger.info(f"✅ Event aktualisiert: {event_uid}")
            
            # Parse Start/End
            start_dt = updated_event['start'].get('dateTime', updated_event['start'].get('date'))
            end_dt = updated_event['end'].get('dateTime', updated_event['end'].get('date'))
            
            if isinstance(start_dt, str):
                start_dt = datetime.fromisoformat(start_dt.replace('Z', '+00:00'))
            if isinstance(end_dt, str):
                end_dt = datetime.fromisoformat(end_dt.replace('Z', '+00:00'))
            
            return CalendarEvent(
                uid=event_uid,
                title=updated_event.get('summary', ''),
                start=start_dt,
                end=end_dt,
                location=updated_event.get('location'),
                description=updated_event.get('description'),
                raw_event=updated_event
            )
            
        except HttpError as e:
            logger.error(f"❌ Event-Update fehlgeschlagen: {e}")
            raise
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
        if not self.service:
            logger.warning("Nicht verbunden - rufe connect() auf")
            if not self.connect():
                return False
        
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_uid
            ).execute()
            
            logger.info(f"✅ Event gelöscht: {event_uid}")
            return True
            
        except HttpError as e:
            logger.error(f"❌ Event-Löschung fehlgeschlagen: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Event-Löschung fehlgeschlagen: {e}")
            return False

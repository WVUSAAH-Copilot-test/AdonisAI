"""
Interaction Logger
Speichert alle Bot-Interaktionen für Personal AI Training

Sammelt Daten für:
- Verhaltensmuster-Analyse
- Präferenzen-Learning
- Fine-tuning Dataset Export
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List, Any
from pathlib import Path
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class InteractionLogger:
    """
    Speichert und verwaltet alle Bot-Interaktionen
    für späteres Training eines Personal AI Models
    """
    
    def __init__(self, db_path: str = "data/interactions.db"):
        """
        Initialisiert den Interaction Logger
        
        Args:
            db_path: Pfad zur SQLite Datenbank
        """
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_database()
        logger.info(f"✅ InteractionLogger initialisiert: {db_path}")
    
    def _ensure_db_directory(self):
        """Stellt sicher, dass das data/ Verzeichnis existiert"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def _get_connection(self):
        """Context Manager für Datenbankverbindung"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """Erstellt die Datenbank-Tabellen falls nicht vorhanden"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Interactions Tabelle - Hauptdaten
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    
                    -- Input
                    user_input TEXT NOT NULL,
                    user_input_type TEXT DEFAULT 'text',  -- text, voice, command
                    
                    -- Bot Response
                    bot_output TEXT NOT NULL,
                    bot_action TEXT,  -- create_event, list_events, answer_question
                    
                    -- Context
                    context_data TEXT,  -- JSON mit Kontext (Uhrzeit, Kalender-State, etc.)
                    conversation_history TEXT,  -- Vorherige Nachrichten als JSON
                    
                    -- Feedback & Learning
                    user_feedback TEXT,  -- Korrektur, Bestätigung, etc.
                    feedback_timestamp TEXT,
                    
                    -- Metadata
                    session_id TEXT,
                    platform TEXT DEFAULT 'telegram',
                    
                    -- Privacy
                    is_sensitive BOOLEAN DEFAULT 0,  -- Opt-out für Training
                    
                    UNIQUE(timestamp, user_id, user_input)
                )
            """)
            
            # Patterns Tabelle - Erkannte Muster
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    pattern_type TEXT NOT NULL,  -- time_preference, communication_style, etc.
                    pattern_data TEXT NOT NULL,  -- JSON mit Muster-Details
                    confidence REAL,  -- 0.0 - 1.0
                    first_seen TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    occurrence_count INTEGER DEFAULT 1
                )
            """)
            
            # Training Exports Tabelle - Tracking von Exports
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS training_exports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    export_timestamp TEXT NOT NULL,
                    export_format TEXT,  -- jsonl, huggingface, csv
                    record_count INTEGER,
                    date_range_start TEXT,
                    date_range_end TEXT,
                    export_path TEXT,
                    notes TEXT
                )
            """)
            
            # Indices für Performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_timestamp 
                ON interactions(user_id, timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_bot_action 
                ON interactions(bot_action)
            """)
            
            logger.info("✅ Datenbank-Schema initialisiert")
    
    def log_interaction(
        self,
        user_id: int,
        user_input: str,
        bot_output: str,
        username: Optional[str] = None,
        user_input_type: str = "text",
        bot_action: Optional[str] = None,
        context_data: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict]] = None,
        session_id: Optional[str] = None,
        is_sensitive: bool = False
    ) -> int:
        """
        Speichert eine Bot-Interaktion
        
        Args:
            user_id: Telegram User ID
            user_input: User Nachricht
            bot_output: Bot Antwort
            username: Telegram Username
            user_input_type: text, voice, command
            bot_action: create_event, list_events, answer_question, etc.
            context_data: Dict mit Kontext-Informationen
            conversation_history: Liste der vorherigen Nachrichten
            session_id: Session Identifier
            is_sensitive: Ob diese Nachricht vom Training ausgeschlossen werden soll
            
        Returns:
            ID des erstellten Records
        """
        timestamp = datetime.now().isoformat()
        
        # Context als JSON speichern
        context_json = json.dumps(context_data) if context_data else None
        history_json = json.dumps(conversation_history) if conversation_history else None
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO interactions (
                        timestamp, user_id, username,
                        user_input, user_input_type,
                        bot_output, bot_action,
                        context_data, conversation_history,
                        session_id, is_sensitive
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    timestamp, user_id, username,
                    user_input, user_input_type,
                    bot_output, bot_action,
                    context_json, history_json,
                    session_id, is_sensitive
                ))
                
                interaction_id = cursor.lastrowid
                
                if not is_sensitive:
                    logger.debug(f"📝 Interaction logged: ID={interaction_id}, User={user_id}")
                else:
                    logger.debug(f"🔒 Sensitive interaction logged (no training): ID={interaction_id}")
                
                return interaction_id
                
            except sqlite3.IntegrityError:
                # Duplicate - ignorieren oder updaten
                logger.warning(f"⚠️ Duplicate interaction ignored: {user_id} @ {timestamp}")
                return -1
    
    def add_feedback(
        self,
        interaction_id: int,
        feedback: str
    ):
        """
        Fügt User-Feedback zu einer Interaktion hinzu
        
        Args:
            interaction_id: ID der Interaktion
            feedback: User Feedback Text
        """
        feedback_timestamp = datetime.now().isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE interactions
                SET user_feedback = ?, feedback_timestamp = ?
                WHERE id = ?
            """, (feedback, feedback_timestamp, interaction_id))
            
            logger.debug(f"💬 Feedback added to interaction {interaction_id}")
    
    def get_user_interactions(
        self,
        user_id: int,
        limit: int = 100,
        include_sensitive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Ruft Interaktionen eines Users ab
        
        Args:
            user_id: Telegram User ID
            limit: Maximale Anzahl
            include_sensitive: Ob sensible Nachrichten inkludiert werden sollen
            
        Returns:
            Liste von Interaktionen als Dicts
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM interactions
                WHERE user_id = ?
            """
            
            if not include_sensitive:
                query += " AND is_sensitive = 0"
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            
            cursor.execute(query, (user_id, limit))
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
    
    def get_statistics(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Berechnet Statistiken über gespeicherte Interaktionen
        
        Args:
            user_id: Optional - nur für bestimmten User
            
        Returns:
            Dict mit Statistiken
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Base query
            where_clause = "WHERE user_id = ?" if user_id else ""
            params = (user_id,) if user_id else ()
            
            # Total interactions
            cursor.execute(f"""
                SELECT COUNT(*) as total,
                       COUNT(CASE WHEN is_sensitive = 0 THEN 1 END) as trainable
                FROM interactions {where_clause}
            """, params)
            counts = dict(cursor.fetchone())
            
            # By action type
            cursor.execute(f"""
                SELECT bot_action, COUNT(*) as count
                FROM interactions {where_clause}
                GROUP BY bot_action
                ORDER BY count DESC
            """, params)
            actions = {row['bot_action'] or 'unknown': row['count'] 
                      for row in cursor.fetchall()}
            
            # By input type
            cursor.execute(f"""
                SELECT user_input_type, COUNT(*) as count
                FROM interactions {where_clause}
                GROUP BY user_input_type
            """, params)
            input_types = {row['user_input_type']: row['count'] 
                          for row in cursor.fetchall()}
            
            # Date range
            cursor.execute(f"""
                SELECT MIN(timestamp) as first, MAX(timestamp) as last
                FROM interactions {where_clause}
            """, params)
            date_range = dict(cursor.fetchone())
            
            return {
                'total_interactions': counts['total'],
                'trainable_interactions': counts['trainable'],
                'actions': actions,
                'input_types': input_types,
                'date_range': date_range
            }
    
    def export_for_training(
        self,
        output_path: str,
        format: str = "jsonl",
        user_id: Optional[int] = None,
        min_date: Optional[str] = None
    ) -> int:
        """
        Exportiert Daten für Model Training
        
        Args:
            output_path: Pfad für Export-Datei
            format: jsonl, csv, huggingface
            user_id: Optional - nur für bestimmten User
            min_date: Optional - nur ab diesem Datum
            
        Returns:
            Anzahl exportierter Records
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT user_input, bot_output, bot_action, 
                       context_data, conversation_history
                FROM interactions
                WHERE is_sensitive = 0
            """
            
            params = []
            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)
            if min_date:
                query += " AND timestamp >= ?"
                params.append(min_date)
            
            query += " ORDER BY timestamp"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Export je nach Format
            if format == "jsonl":
                self._export_jsonl(rows, output_path)
            elif format == "csv":
                self._export_csv(rows, output_path)
            elif format == "huggingface":
                self._export_huggingface(rows, output_path)
            
            # Export tracken
            cursor.execute("""
                INSERT INTO training_exports (
                    export_timestamp, export_format, record_count,
                    export_path
                ) VALUES (?, ?, ?, ?)
            """, (datetime.now().isoformat(), format, len(rows), output_path))
            
            logger.info(f"✅ Exported {len(rows)} records to {output_path}")
            return len(rows)
    
    def _export_jsonl(self, rows, output_path):
        """Exportiert als JSONL (JSON Lines) für Training"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for row in rows:
                record = {
                    'instruction': row['user_input'],
                    'output': row['bot_output'],
                    'action': row['bot_action'],
                }
                if row['context_data']:
                    record['context'] = json.loads(row['context_data'])
                
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def _export_csv(self, rows, output_path):
        """Exportiert als CSV"""
        import csv
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_input', 'bot_output', 'bot_action', 'context'])
            
            for row in rows:
                writer.writerow([
                    row['user_input'],
                    row['bot_output'],
                    row['bot_action'],
                    row['context_data'] or ''
                ])
    
    def _export_huggingface(self, rows, output_path):
        """Exportiert im HuggingFace Dataset Format"""
        # Wie JSONL, aber mit spezifischen Keys
        with open(output_path, 'w', encoding='utf-8') as f:
            for row in rows:
                record = {
                    'text': f"### Instruction:\n{row['user_input']}\n\n### Response:\n{row['bot_output']}"
                }
                f.write(json.dumps(record, ensure_ascii=False) + '\n')

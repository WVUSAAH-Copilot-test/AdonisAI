"""
Context Manager - Verwaltet Chat-Historie für KI-Kontext
"""

from typing import Dict, List
from datetime import datetime, timedelta


class ContextManager:
    """
    Verwaltet Chat-Kontext pro User
    Speichert die letzten N Nachrichten für Kontext-Awareness
    """
    
    def __init__(self, max_messages: int = 10, ttl_minutes: int = 30):
        """
        Args:
            max_messages: Max. Anzahl Nachrichten pro User
            ttl_minutes: Time-to-live in Minuten (alte Nachrichten werden gelöscht)
        """
        self.max_messages = max_messages
        self.ttl_minutes = ttl_minutes
        self.contexts: Dict[int, List[Dict]] = {}  # user_id -> messages
    
    def add_message(self, user_id: int, role: str, content: str):
        """
        Fügt eine Nachricht zum Kontext hinzu
        
        Args:
            user_id: Telegram User ID
            role: "user" oder "assistant"
            content: Nachrichteninhalt
        """
        if user_id not in self.contexts:
            self.contexts[user_id] = []
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        }
        
        self.contexts[user_id].append(message)
        
        # Cleanup: Entferne alte Nachrichten
        self._cleanup_old_messages(user_id)
        
        # Limitiere auf max_messages
        if len(self.contexts[user_id]) > self.max_messages:
            self.contexts[user_id] = self.contexts[user_id][-self.max_messages:]
    
    def get_context(self, user_id: int) -> List[Dict]:
        """
        Gibt den Kontext für einen User zurück
        
        Args:
            user_id: Telegram User ID
            
        Returns:
            Liste von Messages (role, content)
        """
        if user_id not in self.contexts:
            return []
        
        self._cleanup_old_messages(user_id)
        
        # Returniere nur role und content (ohne timestamp)
        return [
            {'role': msg['role'], 'content': msg['content']}
            for msg in self.contexts[user_id]
        ]
    
    def get_context_summary(self, user_id: int) -> str:
        """
        Erstellt eine textuelle Zusammenfassung des Kontexts
        
        Args:
            user_id: Telegram User ID
            
        Returns:
            Kontext als String
        """
        messages = self.get_context(user_id)
        
        if not messages:
            return "Keine vorherige Konversation."
        
        summary = "CHAT-VERLAUF:\n"
        for msg in messages[-5:]:  # Nur letzte 5 für Summary
            role_label = "User" if msg['role'] == 'user' else "AdonisAI"
            summary += f"{role_label}: {msg['content'][:100]}...\n"
        
        return summary
    
    def clear_context(self, user_id: int):
        """
        Löscht den Kontext für einen User
        
        Args:
            user_id: Telegram User ID
        """
        if user_id in self.contexts:
            del self.contexts[user_id]
    
    def _cleanup_old_messages(self, user_id: int):
        """
        Entfernt Nachrichten die älter als TTL sind
        
        Args:
            user_id: Telegram User ID
        """
        if user_id not in self.contexts:
            return
        
        cutoff_time = datetime.now() - timedelta(minutes=self.ttl_minutes)
        
        self.contexts[user_id] = [
            msg for msg in self.contexts[user_id]
            if msg['timestamp'] > cutoff_time
        ]

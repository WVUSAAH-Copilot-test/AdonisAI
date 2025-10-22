"""
AI Client - Interface für verschiedene AI Provider
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class AIProvider(ABC):
    """
    Abstrakte Basisklasse für AI Provider
    """
    
    @abstractmethod
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generiert eine Antwort basierend auf dem Prompt
        
        Args:
            prompt: User Input / Prompt
            context: Optionaler Kontext für die Generierung
            
        Returns:
            Generierte Antwort als String
        """
        pass
    
    @abstractmethod
    async def analyze_intent(self, text: str) -> Dict[str, Any]:
        """
        Analysiert die Absicht des Benutzers
        
        Args:
            text: Benutzer-Eingabe
            
        Returns:
            Dictionary mit erkannter Absicht und Parametern
        """
        pass


class AIClient:
    """
    Hauptklasse zur Verwaltung verschiedener AI Provider
    """
    
    def __init__(self, provider: AIProvider):
        """
        Initialisiert den AI Client mit einem Provider
        
        Args:
            provider: AI Provider Instanz
        """
        self.provider = provider
    
    async def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Chat-Funktion für Benutzer-Interaktionen
        
        Args:
            message: Benutzer-Nachricht
            context: Optionaler Kontext
            
        Returns:
            AI-generierte Antwort
        """
        # TODO: Implementierung folgt in Phase 2
        return await self.provider.generate_response(message, context)
    
    async def understand_command(self, text: str) -> Dict[str, Any]:
        """
        Versteht und klassifiziert Befehle
        
        Args:
            text: Benutzer-Eingabe
            
        Returns:
            Dictionary mit Befehlsinformationen
        """
        # TODO: Implementierung folgt in Phase 2
        return await self.provider.analyze_intent(text)

"""
OpenRouter Provider - Gateway zu verschiedenen Open-Source Modellen
"""

import os
import logging
from typing import Optional, Dict, Any, List
import requests
from src.ai.ai_client import AIProvider

logger = logging.getLogger(__name__)


class OpenRouterProvider(AIProvider):
    """
    OpenRouter AI Provider
    Nutzt OpenRouter als Gateway zu verschiedenen AI-Modellen
    
    Unterstützte Modelle:
    - openai/gpt-3.5-turbo (schnell, günstig)
    - anthropic/claude-instant-v1 (gut für Konversationen)
    - google/palm-2-codechat-bison (Code-fokussiert)
    """
    
    # Verfügbare Modelle
    MODELS = {
        'gpt-3.5': 'openai/gpt-3.5-turbo',
        'claude': 'anthropic/claude-instant-v1',
        'palm': 'google/palm-2-codechat-bison',
        'mistral': 'mistralai/mistral-7b-instruct'
    }
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialisiert den OpenRouter Provider
        
        Args:
            api_key: OpenRouter API Key (optional)
            model: Modell-Name (default: gpt-3.5-turbo)
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        model_key = model or os.getenv('OPENROUTER_MODEL', 'gpt-3.5')
        self.model = self.MODELS.get(model_key, self.MODELS['gpt-3.5'])
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            logger.warning("⚠️  OPENROUTER_API_KEY nicht gesetzt")
        
        logger.info(f"✅ OpenRouter Provider initialisiert mit Modell: {self.model}")
    
    def _make_request(self, messages: List[Dict[str, str]], 
                      temperature: float = 0.7, 
                      max_tokens: int = 150,
                      timeout: int = 30) -> Dict[str, Any]:
        """
        Macht einen API-Request zu OpenRouter
        
        Args:
            messages: Chat-Messages (OpenAI-Format)
            temperature: Kreativität (0-1)
            max_tokens: Max. Antwort-Länge
            timeout: Timeout in Sekunden
            
        Returns:
            API Response
            
        Raises:
            Exception bei API-Fehlern
        """
        if not self.api_key:
            raise Exception("OpenRouter API Key fehlt - setze OPENROUTER_API_KEY in .env")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/wvusaah/AdonisAI",
            "X-Title": "AdonisAI",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=timeout,
                verify=False  # SSL-Workaround
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error("⏱️  OpenRouter API Timeout")
            raise Exception("API Timeout")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ OpenRouter API Fehler: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise Exception(f"API Fehler: {str(e)}")
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generiert eine Antwort über OpenRouter (synchron)
        
        Args:
            prompt: User Input / Prompt
            context: Optionaler System-Prompt String
            
        Returns:
            Generierte Antwort
        """
        try:
            # System-Prompt
            system_prompt = context if context else \
                'Du bist AdonisAI, ein hilfreicher persönlicher Assistent auf Deutsch.'
            
            # Messages im OpenAI-Format
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            logger.info(f"🤖 Generiere Antwort mit {self.model}...")
            result = self._make_request(messages, temperature=0.8, max_tokens=500)
            
            # Parse Response
            if 'choices' in result and len(result['choices']) > 0:
                answer = result['choices'][0]['message']['content'].strip()
            else:
                answer = "Entschuldigung, ich konnte keine Antwort generieren."
            
            logger.info(f"✅ Antwort generiert ({len(answer)} Zeichen)")
            return answer
            
        except Exception as e:
            logger.error(f"❌ Fehler bei Antwort-Generierung: {e}")
            return f"⚠️ Fehler: {str(e)}"
    
    async def analyze_intent(self, text: str) -> Dict[str, Any]:
        """
        Analysiert die Absicht über OpenRouter
        
        Args:
            text: Benutzer-Eingabe
            
        Returns:
            Dictionary mit Intent-Informationen
        """
        try:
            # System-Prompt für Intent-Klassifikation
            system_prompt = """Du bist ein Intent-Klassifikator. 
Klassifiziere die Benutzer-Eingabe in eine der folgenden Kategorien:
- calendar: Termin-bezogene Anfragen
- reminder: Erinnerungs-bezogene Anfragen
- question: Informations-Fragen
- general: Allgemeine Konversation

Antworte nur mit dem Intent-Namen."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
            
            logger.info(f"🎯 Analysiere Intent für: {text[:50]}...")
            result = self._make_request(messages, temperature=0.3, max_tokens=20, timeout=10)
            
            # Parse Intent
            if 'choices' in result and len(result['choices']) > 0:
                intent_text = result['choices'][0]['message']['content'].strip().lower()
            else:
                intent_text = 'general'
            
            # Mapping zu Intent-Kategorien
            intent = 'general'
            confidence = 0.8
            
            if 'calendar' in intent_text:
                intent = 'calendar'
            elif 'reminder' in intent_text:
                intent = 'reminder'
            elif 'question' in intent_text:
                intent = 'question'
            
            result_dict = {
                'intent': intent,
                'confidence': confidence,
                'entities': [],
                'raw_text': text
            }
            
            logger.info(f"✅ Intent erkannt: {intent} (Confidence: {confidence})")
            return result_dict
            
        except Exception as e:
            logger.error(f"❌ Fehler bei Intent-Analyse: {e}")
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'entities': [],
                'error': str(e)
            }

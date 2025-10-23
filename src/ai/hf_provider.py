"""
Hugging Face Provider - Kostenfreie AI-Modelle über Hugging Face Inference API
"""

import os
import logging
from typing import Optional, Dict, Any, List
import requests
from src.ai.ai_client import AIProvider

logger = logging.getLogger(__name__)


class HuggingFaceProvider(AIProvider):
    """
    Hugging Face AI Provider
    Nutzt kostenfreie Inference API von Hugging Face
    
    Unterstützte Modelle:
    - google/flan-t5-base (schnell, leichtgewichtig)
    - mistralai/Mistral-7B-Instruct-v0.2 (besser, langsamer)
    - gpt2 (Fallback, immer verfügbar)
    """
    
    # Verfügbare Modelle mit Eigenschaften
    MODELS = {
        'flan-t5-base': {
            'name': 'google/flan-t5-base',
            'type': 'text2text-generation',
            'fast': True
        },
        'mistral': {
            'name': 'mistralai/Mistral-7B-Instruct-v0.2',
            'type': 'text-generation',
            'fast': False
        },
        'gpt2': {
            'name': 'gpt2',
            'type': 'text-generation',
            'fast': True
        }
    }
    
    def __init__(self, api_token: Optional[str] = None, model: Optional[str] = None):
        """
        Initialisiert den Hugging Face Provider
        
        Args:
            api_token: Hugging Face API Token (optional)
            model: Modell-Name (default: flan-t5-base)
        """
        self.api_token = api_token or os.getenv('HF_API_TOKEN')
        
        # Verwende flan-t5-base als Standard (schneller und zuverlässiger)
        model_key = model or os.getenv('AI_MODEL', 'flan-t5-base')
        self.model_config = self.MODELS.get(model_key, self.MODELS['flan-t5-base'])
        self.model = self.model_config['name']
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        
        if not self.api_token:
            logger.warning("⚠️  HF_API_TOKEN nicht gesetzt - limitierte API-Nutzung")
        
        logger.info(f"✅ HuggingFace Provider initialisiert mit Modell: {self.model}")
    
    def _make_request(self, payload: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
        """
        Macht einen API-Request zu Hugging Face
        
        Args:
            payload: Request Payload
            timeout: Timeout in Sekunden
            
        Returns:
            API Response als Dictionary
            
        Raises:
            Exception bei API-Fehlern
        """
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=timeout,
                verify=False  # SSL-Workaround für Firmennetzwerke
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error("⏱️  Hugging Face API Timeout")
            raise Exception("API Timeout - Modell lädt möglicherweise")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Hugging Face API Fehler: {e}")
            raise Exception(f"API Fehler: {str(e)}")
    
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generiert eine Antwort über Hugging Face Inference API
        
        Args:
            prompt: User Input / Prompt
            context: Optionaler Kontext (max_length, temperature, etc.)
            
        Returns:
            Generierte Antwort
        """
        try:
            # Kontext-Parameter
            max_length = context.get('max_length', 100) if context else 100
            temperature = context.get('temperature', 0.7) if context else 0.7
            
            # Für T5-Modelle: Prefix für bessere Antworten
            if 't5' in self.model.lower():
                prompt = f"Beantworte die folgende Frage: {prompt}"
            
            # Payload für API
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": max_length,
                    "temperature": temperature,
                    "return_full_text": False
                },
                "options": {
                    "wait_for_model": True,
                    "use_cache": True
                }
            }
            
            logger.info(f"🤖 Generiere Antwort mit {self.model}...")
            result = self._make_request(payload)
            
            # Response-Parsing abhängig vom Modell
            if isinstance(result, list) and len(result) > 0:
                # Text-Generation Modelle
                if 'generated_text' in result[0]:
                    answer = result[0]['generated_text'].strip()
                # Text2Text-Generation (T5)
                elif 'generated_text' in result[0] or isinstance(result[0], dict):
                    answer = str(result[0].get('generated_text', result[0])).strip()
                else:
                    answer = str(result[0]).strip()
            elif isinstance(result, dict):
                answer = result.get('generated_text', str(result)).strip()
            else:
                answer = str(result).strip()
            
            logger.info(f"✅ Antwort generiert ({len(answer)} Zeichen)")
            return answer if answer else "Entschuldigung, ich konnte keine Antwort generieren."
            
        except Exception as e:
            logger.error(f"❌ Fehler bei Antwort-Generierung: {e}")
            return f"⚠️ Fehler: {str(e)}"
    
    async def analyze_intent(self, text: str) -> Dict[str, Any]:
        """
        Analysiert die Absicht über Hugging Face
        
        Args:
            text: Benutzer-Eingabe
            
        Returns:
            Dictionary mit Intent-Informationen
        """
        try:
            # Einfache Intent-Klassifikation via Text-Generation
            prompt = f"Klassifiziere die Absicht: '{text}'. Antwort (calendar/reminder/question/general):"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 20,
                    "temperature": 0.3
                },
                "options": {
                    "wait_for_model": True
                }
            }
            
            logger.info(f"🎯 Analysiere Intent für: {text[:50]}...")
            result = self._make_request(payload, timeout=10)
            
            # Parse Intent aus Response
            if isinstance(result, list) and len(result) > 0:
                intent_text = result[0].get('generated_text', '').lower()
            else:
                intent_text = str(result).lower()
            
            # Mapping zu Intent-Kategorien
            intent = 'general'
            confidence = 0.5
            
            if 'calendar' in intent_text or 'termin' in text.lower():
                intent = 'calendar'
                confidence = 0.8
            elif 'reminder' in intent_text or 'erinner' in text.lower():
                intent = 'reminder'
                confidence = 0.8
            elif any(q in text.lower() for q in ['wie', 'was', 'wann', 'wo', 'warum']):
                intent = 'question'
                confidence = 0.7
            
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

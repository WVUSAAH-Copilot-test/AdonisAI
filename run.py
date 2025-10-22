#!/usr/bin/env python3
"""
Start-Skript für AdonisAI - Umgeht SSL-Verifizierungsprobleme
"""
import ssl
import urllib3

# SSL-Verifizierung deaktivieren
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Monkey-patch für requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_version'] = ssl.PROTOCOL_TLS
        kwargs['cert_reqs'] = ssl.CERT_NONE
        return super().init_poolmanager(*args, **kwargs)

# Patch requests Session
_old_request = requests.Session.request
def _new_request(self, *args, **kwargs):
    kwargs.setdefault('verify', False)
    return _old_request(self, *args, **kwargs)
requests.Session.request = _new_request

# Jetzt main.py ausführen
import src.main
src.main.main()

#!/usr/bin/env python3
"""
Start-Skript für AdonisAI - Umgeht SSL-Verifizierungsprobleme
"""

# CRITICAL: Import ssl_patch FIRST to patch SSL before telegram loads
import ssl_patch

# Patch telegram's vendored urllib3
import ssl
import telegram.vendor.ptb_urllib3.urllib3 as telegram_urllib3
from telegram.vendor.ptb_urllib3.urllib3.util import ssl_ as telegram_ssl_

# Disable warnings
telegram_urllib3.disable_warnings()

# Patch SSL context creation in vendored urllib3
_original_create_urllib3_context = telegram_ssl_.create_urllib3_context

def patched_create_urllib3_context(*args, **kwargs):
    """Create SSL context without certificate verification"""
    ctx = _original_create_urllib3_context(*args, **kwargs)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

telegram_ssl_.create_urllib3_context = patched_create_urllib3_context

# Jetzt main.py ausführen
import src.main
src.main.main()

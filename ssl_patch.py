"""
SSL Patch - Muss VOR allen anderen Imports geladen werden
Deaktiviert SSL Verifizierung für Corporate Network (Zscaler)
"""
import ssl

# 1. Globaler SSL Context Patch
_original_create_default_context = ssl.create_default_context

def _patched_create_default_context(purpose=ssl.Purpose.SERVER_AUTH, *args, **kwargs):
    ctx = _original_create_default_context(purpose, *args, **kwargs)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

ssl.create_default_context = _patched_create_default_context
ssl._create_default_https_context = ssl._create_unverified_context

# 2. Patch SSLContext.wrap_socket direkt
_original_wrap_socket = ssl.SSLContext.wrap_socket

def _patched_wrap_socket(self, sock, *args, **kwargs):
    # Erzwinge CERT_NONE für alle wrap_socket Aufrufe
    self.check_hostname = False
    self.verify_mode = ssl.CERT_NONE
    return _original_wrap_socket(self, sock, *args, **kwargs)

ssl.SSLContext.wrap_socket = _patched_wrap_socket

print("🔓 SSL Certificate Verification DISABLED (Corporate Network Workaround)")

from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication that skips the CSRF check.
    Used for development to allow cross-origin requests from different ports (e.g., 8081 to 8000).
    """
    def enforce_csrf(self, request):
        return  # Skip CSRF check

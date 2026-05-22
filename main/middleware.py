from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class TwoFactorEnforcementMiddleware:
    """Redirect sessions with pending email verification to the OTP page."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._should_redirect_to_otp(request):
            return redirect(f"{reverse('verify_otp')}?email={request.session['pending_verification_email']}")
        return self.get_response(request)

    def _should_redirect_to_otp(self, request):
        pending_email = request.session.get("pending_verification_email")
        if not pending_email:
            return False

        if not getattr(settings, "ENFORCE_2FA", False):
            return False

        verify_path = reverse("verify_otp")
        logout_path = reverse("logout")
        allowed_prefixes = (
            verify_path,
            logout_path,
            settings.STATIC_URL,
        )
        return not request.path.startswith(allowed_prefixes)

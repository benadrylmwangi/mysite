from django.conf import settings


def google_oauth(request):
    app_config = settings.SOCIALACCOUNT_PROVIDERS.get("google", {}).get("APP", {})
    return {
        "google_oauth_enabled": bool(app_config.get("client_id") and app_config.get("secret")),
    }

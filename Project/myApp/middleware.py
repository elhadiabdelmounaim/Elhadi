from django.conf import settings
from django.middleware.clickjacking import XFrameOptionsMiddleware


class PreviewFrameOptionsMiddleware(XFrameOptionsMiddleware):
    """Allow public pages in the trusted Replit development preview only."""

    def process_response(self, request, response):
        match = request.resolver_match
        if (
            settings.DEBUG
            and settings.REPLIT_PREVIEW_EMBEDDING
            and match is not None
            and match.url_name in {"root", "cv", "contact", "about"}
        ):
            response.headers.pop("X-Frame-Options", None)
            response["Content-Security-Policy"] = (
                "frame-ancestors 'self' https://replit.com "
                "https://*.replit.com https://*.replit.dev"
            )
            return response
        return super().process_response(request, response)

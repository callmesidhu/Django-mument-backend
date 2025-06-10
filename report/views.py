# report/views.py
import requests
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed
from .models import DailyUpdate
from .serializers import DailyUpdateSerializer

# Where we fetch the caller’s details.  Override in settings.py if you move it.
USER_DETAILS_URL = getattr(
    settings,
    "USER_DETAILS_URL",
    "http://127.0.0.1:8000/api/users/details/",
)


def _extract_uuid(request):
    """
    Helper: replay the caller’s Bearer token to /api/users/details
    and return the UUID.
    """
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if not auth_header.startswith("Bearer "):
        raise AuthenticationFailed("Missing or malformed Authorization header")

    try:
        r = requests.get(
            USER_DETAILS_URL,
            headers={"Authorization": auth_header},
            timeout=5,
        )
        r.raise_for_status()
    except requests.RequestException as exc:
        raise AuthenticationFailed(f"Could not fetch user details: {exc}") from exc

    uuid_value = r.json().get("uuid")
    if not uuid_value:
        raise AuthenticationFailed("UUID not present in user-details response")
    return uuid_value


class SubmitView(generics.CreateAPIView):
    """
    POST /api/report/submit/
    Body: { "title": "...", "content": "..." }
    """
    serializer_class = DailyUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        uuid_value = _extract_uuid(self.request)
        # The serializer has uuid as read-only, so we pass it directly to .save()
        serializer.save(uuid=uuid_value)


class DailyReportListView(generics.ListAPIView):
    """
    GET /api/report/daily-report/
    Returns only the caller’s rows.
    """
    serializer_class = DailyUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        uuid_value = _extract_uuid(self.request)
        return DailyUpdate.objects.filter(uuid=uuid_value)

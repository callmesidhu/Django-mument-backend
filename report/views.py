import requests
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed
from .models import DailyUpdate
from .serializers import DailyUpdateSerializer

USER_DETAILS_URL = getattr(
    settings,
    "USER_DETAILS_URL",
    "https://mument-apis.onrender.com/api/users/details/",
)

def _extract_user_details(request):
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

    data = r.json()
    uuid_value = data.get("uuid")
    email_value = data.get("email")

    if not uuid_value or not email_value:
        raise AuthenticationFailed("UUID or Email not present in user-details response")

    return uuid_value, email_value


class SubmitView(generics.CreateAPIView):
    serializer_class = DailyUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        uuid_value, email_value = _extract_user_details(self.request)
        serializer.save(uuid=uuid_value, email=email_value)


class DailyReportListView(generics.ListAPIView):
    serializer_class = DailyUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        uuid_value, _ = _extract_user_details(self.request)
        return DailyUpdate.objects.filter(uuid=uuid_value)

from rest_framework import serializers
from .models import DailyUpdate


class DailyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyUpdate
        fields = ("id", "uuid","email", "title", "content", "created_at")
        read_only_fields = ("id", "uuid","email" "created_at")
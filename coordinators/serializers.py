from rest_framework import serializers
from .models import Coordinator

class CoordinatorSerializer(serializers.ModelSerializer):
    coordinator_email = serializers.EmailField(required=True)
    players_email = serializers.ListField(
        child=serializers.EmailField(),
        required=True,
        allow_empty=False  # <- Disallow empty list
    )

    class Meta:
        model = Coordinator
        fields = ['id', 'coordinator_email', 'players_email']
        extra_kwargs = {
            'coordinator_email': {'required': True},
            'players_email': {'required': True},
        }

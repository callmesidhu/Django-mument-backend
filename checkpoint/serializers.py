from rest_framework import serializers
from .models import Checkpoint

class CheckpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkpoint
        fields = '__all__'

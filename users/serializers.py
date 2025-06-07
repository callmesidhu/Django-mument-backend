from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import MumentUser
from django.contrib.auth.hashers import make_password

class MumentUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = MumentUser
        fields = '__all__'

    def create(self, validated_data):
        return MumentUser.objects.create_user(**validated_data)
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MumentUser
        fields = ["name", "img_url", "mu_id", "phone", "domain", "idea_submission", "team"]
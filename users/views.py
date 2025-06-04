from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MumentUserSerializer
from .models import MumentUser
from django.contrib.auth.hashers import check_password


class SignupView(APIView):
    def post(self, request):
        serializer = MumentUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = MumentUser.objects.get(email=email)
        except MumentUser.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Login successful!", "user": MumentUserSerializer(user).data}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MumentUserSerializer,AllUserSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserUpdateSerializer
from .models import MumentUser

class AllView(APIView):
    def get(self, request):
        try:
            users = MumentUser.objects.all()
            serializer = AllUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Could not retrieve users: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SignupView(APIView):
    def post(self, request):
        serializer = MumentUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = MumentUserSerializer(user)
        return Response(serializer.data)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully!",
                "user": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        new_password = request.data.get('new_password')

        if not (email and phone and new_password):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = MumentUser.objects.get(email=email, phone=phone)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        except MumentUser.DoesNotExist:
            return Response({'error': 'User with this email and phone not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
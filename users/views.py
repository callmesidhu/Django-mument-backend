from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MumentUserSerializer

class SignupView(APIView):
    def post(self, request):
        serializer = MumentUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

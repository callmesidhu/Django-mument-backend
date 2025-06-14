from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Coordinator
from .serializers import CoordinatorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class AddCoordinatorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CoordinatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Coordinator added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCoordinatorsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        coordinators = Coordinator.objects.all()
        serializer = CoordinatorSerializer(coordinators, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

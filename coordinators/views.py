from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CoordinatorSerializer
from rest_framework.permissions import AllowAny

class AddCoordinatorView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CoordinatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Coordinator added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

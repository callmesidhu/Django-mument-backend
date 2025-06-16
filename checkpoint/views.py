from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Checkpoint
from .serializers import CheckpointSerializer

class AddCheckpointView(APIView):
    def post(self, request):
        serializer = CheckpointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowCheckpointView(APIView):
    def get(self, request):
        checkpoints = Checkpoint.objects.all()
        serializer = CheckpointSerializer(checkpoints, many=True)
        return Response(serializer.data)

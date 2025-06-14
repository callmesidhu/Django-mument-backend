from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Coordinator
from .serializers import CoordinatorSerializer
from .permissions import IsCoordinator
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class AddCoordinatorView(APIView):
    permission_classes = [IsCoordinator]

    def post(self, request):
        try:
            # Check for duplicate coordinator by email (if required)
            email = request.data.get("coordinator_email")
            if Coordinator.objects.filter(coordinator_email=email).exists():
                return Response(
                    {"error": "Coordinator with this email already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = CoordinatorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Coordinator added successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (IntegrityError, ValidationError) as e:
            return Response(
                {"error": f"Database error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CoordinatorListView(APIView):
    permission_classes = [IsCoordinator]

    def get(self, request):
        try:
            coordinators = Coordinator.objects.all()
            serializer = CoordinatorSerializer(coordinators, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Could not retrieve coordinators: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# class CoordinatorPlayerDetailsView(APIView):
    
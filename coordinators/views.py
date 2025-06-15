import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Coordinator
from .serializers import CoordinatorSerializer
from .permissions import IsCoordinator
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from report.models import DailyUpdate
from report.serializers import DailyUpdateSerializer
from rest_framework.permissions import IsAuthenticated

class AddCoordinatorView(APIView):
    permission_classes = [IsCoordinator]

    def post(self, request):
        try:
           
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


    
class CoordinatorPlayerDetailsView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            coordinators = Coordinator.objects.all()
            result = []

            for coord in coordinators:
                coord_data = {
                    "id": coord.id,
                    "coordinator_email": coord.coordinator_email,
                    "players_email": {}
                }

                for player_email in coord.players_email:
                    updates = DailyUpdate.objects.filter(email=player_email)
                    updates_serialized = DailyUpdateSerializer(updates, many=True).data

                    if updates_serialized:
                        coord_data["players_email"][player_email] = updates_serialized
                    else:
                        coord_data["players_email"][player_email] = "No reports submitted"

                result.append(coord_data)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Could not retrieve coordinator player details: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
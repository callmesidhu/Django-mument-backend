import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Coordinator
from .serializers import CoordinatorSerializer
from .permissions import IsCoordinator
from django.db import IntegrityError
from django.core.exceptions import ValidationError
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

            users_api = "https://mument-apis.onrender.com/api/users/all/"
            reports_api = "https://mument-apis.onrender.com/api/report/daily-report/"

            # Get user data
            users_response = requests.get(users_api)
            users_data = users_response.json()
            if not isinstance(users_data, list):
                raise ValueError("Invalid format for users data")

            email_to_uuid = {
                user["email"]: user["uuid"] for user in users_data if "email" in user and "uuid" in user
            }

            # Get reports
            reports_response = requests.get(reports_api)

            try:
                reports_data = reports_response.json()
            except Exception as e:
                return Response(
                    {"error": f"Failed to parse reports JSON: {str(e)}", "raw_response": reports_response.text},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Debug print actual format
            if not isinstance(reports_data, list):
                return Response(
                    {
                        "error": "Invalid format for reports data",
                        "received_type": str(type(reports_data)),
                        "example_data": reports_data
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


            result = []

            for coordinator in coordinators:
                players_info = []

                for email in coordinator.players_email:
                    uuid = email_to_uuid.get(email)
                    if uuid:
                        reports = [report for report in reports_data if report.get("uuid") == uuid]
                        players_info.append({
                            "email": email,
                            "uuid": uuid,
                            "reports": reports
                        })

                result.append({
                    "coordinator_email": coordinator.coordinator_email,
                    "players": players_info
                })

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to fetch data: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer

class RegisterUserView(APIView):

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save()
            return Response({
                "id": user_profile.id,
                "name": user_profile.name,
                "message": "Success"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

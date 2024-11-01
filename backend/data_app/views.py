from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserProfile
from .serializers import UserProfileSerializer

class RegisterView(APIView):

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user_id": user.id,
                "user_name": user.user_name,
                "message": "Success"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        contact = request.data.get("user_contact")
        password = request.data.get("user_password")

        try:
            user = UserProfile.objects.get(user_contact=contact)
            if check_password(password, user.user_password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "user_token": str(refresh.access_token),
                    "user_name": user.user_name,
                    "message": "Success"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except UserProfile.DoesNotExist:
            return Response({"message": "Failed"}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')

        try:
            user_profile = UserProfile.objects.get(id=user_id)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
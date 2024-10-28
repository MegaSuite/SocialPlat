from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserProfileSerializer

class RegisterView(APIView):

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "id": user.id,
                "name": user.name,
                "message": "Success"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        contact = request.data.get("contact")
        password = request.data.get("password")

        try:
            user = UserProfile.objects.get(contact=contact)
            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "token": str(refresh.access_token),
                    "name": user.name,
                    "message": "Success"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except UserProfile.DoesNotExist:
            return Response({"message": "Failed"}, status=status.HTTP_404_NOT_FOUND)
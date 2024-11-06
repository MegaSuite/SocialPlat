import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserProfile, Post, Comment
from .serializers import UserProfileSerializer, PostSerializer, CommentSerializer

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
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self, request):
        user_id = request.data.get('user_id')
        method = request.data.get('method')

        try:
            user_profile = UserProfile.objects.get(id=user_id)

            if method == 'request':
                serializer = UserProfileSerializer(user_profile)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif method == 'renew':
                serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
                if serializer.is_valid():
                    # 如果密码被更新，确保它被正确地哈希
                    if 'user_password' in serializer.validated_data:
                        serializer.validated_data['user_password'] = make_password(serializer.validated_data['user_password'])

                    serializer.save()
                    return Response({
                        "user_id": user_profile.id,
                        "user_name": serializer.validated_data.get('user_name', user_profile.user_name),
                        "message": "Success"
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"message": "Invalid method"}, status=status.HTTP_400_BAD_REQUEST)

        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class PostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user_id = request.data.get('user_id')
        method = request.data.get('method')

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if method == 'all':
            posts = Post.objects.all().order_by('-created_at')[:20]
            serializer = PostSerializer(posts, many=True)
            return Response({
                "message": "Success",
                "posts": serializer.data
            }, status=status.HTTP_200_OK)

        elif method == 'add':
            post_title = request.data.get('post_title')
            post_content = request.data.get('post_content')

            post = Post.objects.create(
                post_author=user,
                post_title=post_title,
                post_content=post_content
            )

            return Response({
                "post_id": post.post_id,
                "post_author": user.user_name,
                "message": "Success"
            }, status=status.HTTP_201_CREATED)

        elif method == 'comment':
            post_id = request.data.get('post_id')
            comment_content = request.data.get('comment_content')

            try:
                post = Post.objects.get(post_id=post_id)
            except Post.DoesNotExist:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

            comment = Comment.objects.create(
                post=post,
                comment_author=user,
                comment_content=comment_content
            )

            return Response({
                "post_id": post.post_id,
                "post_author": post.post_author.user_name,
                "comment_id": comment.comment_id,
                "comment_author": user.user_name,
                "message": "Success"
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_400_BAD_REQUEST)
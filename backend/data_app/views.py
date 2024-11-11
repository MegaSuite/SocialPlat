from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import check_password, make_password

from .alg.rcmFriends import rcm_friends
from .models import UserProfile, Post, Comment, FriendRequest, Friendship
from .serializers import UserProfileSerializer, PostSerializer, CommentSerializer, FriendSerializer, FriendRequestSerializer

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
                    "user_id": user.id,
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
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
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

        elif method == 'like':
            post_id = request.data.get('post_id')

            try:
                post = Post.objects.get(post_id=post_id)
            except Post.DoesNotExist:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

            # 检查帖子是否已经在用户的点赞列表中
            if post_id in user.user_like:
                # 如果已经点赞，则取消点赞
                user.user_like.remove(post_id)
            else:
                # 如果未点赞，则添加点赞
                user.user_like.append(post_id)

            user.save()

            return Response({
                "message": "Success"
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_400_BAD_REQUEST)


class AvatarView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        user_id = request.data.get('user_id')
        method = request.data.get('method')

        try:
            user_profile = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'message': 'Failed', 'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if method == 'add':
            avatar = request.FILES.get('avatar')
            if avatar:
                user_profile.avatar = avatar
                user_profile.save()
                return Response({
                    "avatar": request.build_absolute_uri(user_profile.avatar.url),
                    "message": "Success"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Failed", "error": "No avatar file provided"}, status=status.HTTP_400_BAD_REQUEST)

        elif method == 'request':
            if user_profile.avatar:
                return Response({
                    "avatar": request.build_absolute_uri(user_profile.avatar.url),
                    "message": "Success"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Failed", "error": "No avatar found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"message": "Failed", "error": "Invalid method"}, status=status.HTTP_400_BAD_REQUEST)


class RelationView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self, request):
        user_id = request.data.get('user_id')
        method = request.data.get('method')

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if method == 'add':
            friend_id = request.data.get('friend_add')
            try:
                friend = UserProfile.objects.get(id=friend_id)
            except UserProfile.DoesNotExist:
                return Response({'error': 'Friend not found'}, status=status.HTTP_404_NOT_FOUND)

            FriendRequest.objects.create(from_user=user, to_user=friend, status='pending')

            friendships = Friendship.objects.filter(user=user)
            serializer = FriendSerializer(friendships, many=True)
            return Response({
                'user_id': user.id,
                'friends': serializer.data,
                'message': 'Success'
            }, status=status.HTTP_200_OK)

        elif method == 'request':
            friendships = Friendship.objects.filter(user=user)
            friend_requests = FriendRequest.objects.filter(to_user=user)

            friend_serializer = FriendSerializer(friendships, many=True)
            request_serializer = FriendRequestSerializer(friend_requests, many=True)

            return Response({
                'friends': friend_serializer.data,
                'friendRequests': request_serializer.data,
                'avatar': request.build_absolute_uri(user.avatar.url) if user.avatar else None,
                'message': 'Success'
            }, status=status.HTTP_200_OK)

        elif method in ['accept', 'refuse']:
            request_id = request.data.get('friend_request_id')
            try:
                friend_request = FriendRequest.objects.get(id=request_id, to_user=user)
            except FriendRequest.DoesNotExist:
                return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

            if method == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
                Friendship.objects.create(user=user, friend=friend_request.from_user)
                Friendship.objects.create(user=friend_request.from_user, friend=user)
            else:
                friend_request.status = 'refused'
                friend_request.save()

            friendships = Friendship.objects.filter(user=user)
            serializer = FriendSerializer(friendships, many=True)
            return Response({
                'friends': serializer.data,
                'message': 'Success'
            }, status=status.HTTP_200_OK)

        elif method == 'remove':
            friend_id = request.data.get('friend_remove')
            try:
                friend = UserProfile.objects.get(id=friend_id)
            except UserProfile.DoesNotExist:
                return Response({'error': 'Friend not found'}, status=status.HTTP_404_NOT_FOUND)

            # 删除双向的好友关系
            Friendship.objects.filter(user=user, friend=friend).delete()
            Friendship.objects.filter(user=friend, friend=user).delete()

            # 获取更新后的好友列表
            friendships = Friendship.objects.filter(user=user)
            serializer = FriendSerializer(friendships, many=True)

            return Response({
                'friends': serializer.data,
                'message': 'Success'
            }, status=status.HTTP_200_OK)

        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_400_BAD_REQUEST)


class RecommendView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self, request):
        user_id = request.data.get('user_id')
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # 获取所有用户数据
        all_users = UserProfile.objects.exclude(id=user_id)
        user_data_list = []
        for u in all_users:
            user_data = {
                "id": u.id,
                "user_name": u.user_name,
                "user_job": u.user_job,
                "user_dob_year": u.user_dob_year,
                "user_gender": u.user_gender,
                "user_hobbies": u.user_hobbies,
                "user_friends": list(u.friendships.values_list('friend_id', flat=True)),
                "user_character": u.user_characters
            }
            user_data_list.append(user_data)

        # 获取用户的帖子内容
        user_posts = Post.objects.filter(post_author=user)
        user_post_content = [
            {
                "user_id": user_id,
                "post_content": post.post_content
            } for post in user_posts
        ]

        # 调用推荐函数
        recommendations = rcm_friends(user_data_list, user_post_content)

        # 获取推荐的用户详情
        recommended_users = []
        for rec_user_id in recommendations.get(str(user_id), []):
            try:
                rec_user = UserProfile.objects.get(id=rec_user_id)
                recommended_users.append({
                    "user_id": rec_user.id,
                    "user_name": rec_user.user_name,
                    "user_job": rec_user.user_job,
                    "user_hobbies": rec_user.user_hobbies,
                    "avatar_url": request.build_absolute_uri(rec_user.avatar.url) if rec_user.avatar else None
                })
            except UserProfile.DoesNotExist:
                continue

        return Response({
            "recommendations": recommended_users,
            "message": "Success"
        }, status=status.HTTP_200_OK)
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.models import Profile, User
from accounts.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'User Registration Successful',
                'success': True,
                'status': status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return Response(
                {
                    'message': 'Login Success.',
                    'token': token,
                    'success': True,
                    'status': status.HTTP_200_OK,
                },
                status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'message': 'Password Changed Successfully.',
                'success': True,
                'status': status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'message': 'Password Reset link send. Please check your Email.',
                'success': True,
                'status': status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'message': 'Password Reset Successfully',
                'success': True,
                'status': status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK)


# class UserProfileView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         serializer = UserSerializer(request.user)
#         return Response(
#             {
#                 'message': 'Successfully fetched User Profile',
#                 'success': True,
#                 'status': status.HTTP_200_OK,
#                 'data': serializer.data
#             },
#             status=status.HTTP_200_OK)


# class WishlistView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         id = request.data
#         print('to_watch id', id)
#         movie = get_object_or_404(Movie, id=request.data['to_watch'])
#         user_wishlist = Wishlist.objects.get_or_create(user=request.user)
#         wishlist = Wishlist.objects.filter(
#             user__email=user_wishlist[0], to_watch=movie).exists()
#         if wishlist:
#             Wishlist.objects.get(
#                 user__email=user_wishlist[0]).to_watch.remove(movie)
#             return Response(
#                 {
#                     'message': 'Successfully Removed from Wishlist',
#                     'success': True,
#                     'status': status.HTTP_200_OK,
#                 },
#                 status=status.HTTP_200_OK)
#         else:
#             Wishlist.objects.get(
#                 user__email=user_wishlist[0]).to_watch.add(movie)
#             return Response(
#                 {
#                     'message': 'Successfully Added to Wishlist',
#                     'success': True,
#                     'status': status.HTTP_201_CREATED,
#                 },
#                 status=status.HTTP_201_CREATED)

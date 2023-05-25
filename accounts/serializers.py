from rest_framework import serializers
from accounts.models import Profile, User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.utils import Util
from django.shortcuts import get_object_or_404, redirect, render


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # link = 'https://django-auth.vercel.app/api/user/reset/'+uid+'/'+token
            link = 'http://localhost:3000/reset-password/'+uid+'/'+token
            # Sending EMail
            print("Link: ", link)
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user
            }
            # Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_bio', 'gender', 'dob',
                  'country', 'avatar']


# class UserListSerializer(serializers.ModelSerializer):
#     movies_list = MovieSerializer(many=True, read_only=True)
#     celebrity_list = CelebritySerializer(many=True, read_only=True)

#     class Meta:
#         model = UserList
#         fields = ['id', 'list_title', 'list_description',
#                  'list_type', 'movies_list', 'celebrity_list']

# class WishlistSerializer(serializers.ModelSerializer):
#     to_watch = MovieSerializer(many=True, read_only=True)
#     watched = MovieSerializer(many=True, read_only=True)

#     class Meta:
#         model = Wishlist
#         fields = ['id', 'to_watch', 'watched']

    # def validate(self, attrs):
    #     user = self.context.get('user')
    #     wishlist_item = get_object_or_404(Movie, id=16)
    #     if wishlist_item.towatch.filter(id=14).exists():
    #         wishlist_item.towatch.remove(16)
    #     else:
    #         wishlist_item.towatch.add(16)
        # return HttpResponseRedirect(request.META["HTTP_REFERER"])

# class UserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer(read_only=True)
#     user_wishlist = WishlistSerializer(read_only=True)
#     user_list = UserListSerializer(read_only=True)
#     user_rating = RatingSerializer(read_only=True, many=True)
#     user_review = ReviewSerializer(read_only=True, many=True)
#     class Meta:
#         model = User
#     #   fields = ['id', 'name', 'email']
#         fields = ['id', 'email', 'name', 'profile', 'user_wishlist', 'user_list', 'user_rating', 'user_review']


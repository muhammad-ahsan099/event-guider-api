from django.urls import path
from accounts.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserRegistrationView, UserPasswordResetView, WishlistView, UserProfileView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('user-wishlist/', WishlistView.as_view(), name='user-wishlist'),

]
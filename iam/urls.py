from django.urls import path
from .views import LoginView, RefreshTokenView, SignUpView, UserListDetailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('user/', UserListDetailView.as_view(), name='user-list'),
]
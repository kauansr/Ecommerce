from django.urls import path
from accounts.views import UserAPI, UsersAPI, UserCreateAPI
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import CustomTokenObtainPairView

urlpatterns = [
    path('accounts/', UsersAPI.as_view(), name='usersapi'),
    path('accounts/<int:pk>/', UserAPI.as_view(), name='userapi'),
    path('accountscreateapi/', UserCreateAPI.as_view(), name='usercreateapi'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
    path('token/refresh', TokenRefreshView.as_view(), name='tokenrefresh'),
]

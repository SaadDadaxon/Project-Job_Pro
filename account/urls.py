from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from . import views


urlpatterns = [
    path('register/', views.AccountRegister.as_view()),
    path('login/', views.AccountLogin.as_view()),
    # Refresh Token olish uchun URL
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Black qilinadigan token
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('my-account/', views.MyAccount.as_view()),
    path('retrive-update/<int:pk>/', views.AccountRU.as_view()),
    path('working-history-list/', views.WorkingHistoryList.as_view()),
]

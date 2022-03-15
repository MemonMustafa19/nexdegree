from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserCRUD.as_view(), name='user'),
    path('user/<int:id>/', UserCRUD.as_view(), name='user_with_id'),

    path('login/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls',
                                    namespace='password_reset')),

]

from django.urls import path
from authen.views import (UserGroupsView,
                          UserRegisterView,
                          UserLoginView,
                          UserProfileView,
                          change_password,
                          RequestPasswordRestEmail,
                          SetNewPasswordView,
                          UserGetView,
                        )

urlpatterns = [
    path('user/groups/', UserGroupsView.as_view()),
    path('user/register/', UserRegisterView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('user/profile/', UserProfileView.as_view()),
    path('user/<int:pk>/', UserGetView.as_view()),
    # Passwordd
    path('password/change/', change_password),
    path('password/rest/', RequestPasswordRestEmail.as_view()),
    path('password/new/', SetNewPasswordView.as_view()),


]
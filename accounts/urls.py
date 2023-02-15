from django.urls import path
from .views import SignupView
from .views import ProfileView
from .views import EditProfileView
from .views import ChangePasswordView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/<str:username>", ProfileView.as_view(), name="profile"),
    path("editprofile/", EditProfileView.as_view(), name="edit_profile"),
    path("changepassword/", ChangePasswordView.as_view(), name="change_password"),
]

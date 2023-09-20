from django.urls import path
from accounts import views
urlpatterns = [
    path('login/', views.login_view, name='loginApi'),
    path('logout/', views.logout_view, name='logoutApi'),
    path('signup/', views.signup_view, name='signupApi'),
    path('userprofile/', views.user_profile_view, name='userprofileApi'),
    path('updateUserprofile/', views.update_user_profile_view, name='updateUserprofileApi'),
    path('changepassword/', views.change_password_view, name='changepasswordApi'),
    path('forgetPassword/', views.forgot_password_view, name='forgetPasswordApi'),
    path('setPassword/', views.set_password_view, name='setPasswordApi'),
]

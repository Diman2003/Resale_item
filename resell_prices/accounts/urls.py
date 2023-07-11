from django.urls import path
from .import views

app_name = "account"

urlpatterns = [
    path('',views.register,name='signup'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'), 
    path('profile/',views.user_profile,name='profile'),
    path('display_profile',views.profile,name='display_profile'),
]

"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DjangoApp.views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
    path('', home.as_view(), name='home'),
    path('CheckAuth', CheckAuth.as_view(), name='CheckAuth'),
    path('Register', Register.as_view(), name='Register'),
    path('GenerateOtp',GenerateOtp.as_view(), name='GenerateOtp'),
    path('Login', Login.as_view(), name='Login'),
    path('Logout', Logout.as_view(), name='Logout'),
    path('UploadData', UploadData.as_view(), name='UploadData'),
    path('Bot', Bot.as_view(), name='Bot'),
    path('Summary', Summary.as_view(), name='Summary'),
]

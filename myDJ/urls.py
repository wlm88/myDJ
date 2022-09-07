"""myDJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from myDJ import views

urlpatterns = [
    path('login1/', views.login1),
    path('login/', views.login),
    path('register1/', views.register1),
    path('register/', views.register),
    path('search_word/', views.search_by_word),
    path('show/',views.show),
    path('p_data/',views.p_data),
    path('dowload/',views.dowload),
    path('dowload1/',views.dowload1),
    path('dowload2/', views.dowload2)

]

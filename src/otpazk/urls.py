"""otp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

import main
from . import views

app_name = "portal"
urlpatterns = [
                  url(r'admin/', admin.site.urls),
                  url(r'otp/', include('main.urls')),
                  url(r'otp/', include('orders.urls')),
                  # url(r'^', include('django_telegrambot.urls')),
                  url(r'^$', views.index, name='index'),
              ]\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #\
              # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import url
from django.contrib import admin

from main import views

app_name = "main"
urlpatterns = [
    url(r'^naliv/', views.naliv, name='naliv'),
]

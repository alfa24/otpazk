from django.conf.urls import url
from django.contrib import admin

from orders import views

app_name = "orders"
urlpatterns = [
    url(r'^order/$', views.orderAllAzk, name='orderAllAzk'),
    # url(r'^order/(?P<azk>\w+)/', views.orderOneAzk, name='orderOneAzk'),
]

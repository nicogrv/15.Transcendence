from django.urls import path
from . import views

app_name = 'pong'

urlpatterns = [
    path('', views.say_hello, name='persons'),
    path('<slug:slug>/', views.person_detail, name='person')
]
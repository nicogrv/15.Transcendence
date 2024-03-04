from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.helloTitou   ),
    # path('', admin.site.urls),
]

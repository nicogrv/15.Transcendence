from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blogBd, name='blogBd'),
    path('id/<str:id>/', views.idF, name='blogBd'),
    # path('', admin.site.urls),
]

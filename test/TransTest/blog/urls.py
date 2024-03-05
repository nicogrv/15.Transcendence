from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/getUser', views.apiGetUser, name='apiGetUser'),
    path('api/UpdateUser/<str:uid>/<str:elem>/<str:value>', views.apiUpdateUser, name='blogBd'),
    path('id/<str:id>/', views.idF, name='blogBd'),
    path('', views.blogBd, name='blogBd'),
    # path('', admin.site.urls),
]

from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'Core'

router = routers.DefaultRouter()

router.register(r'piece', views.PieceViewSet, basename='Piece')

urlpatterns = [
    path('', include(router.urls)),
    path('hello-world/', views.hello_world, name='Hello World'),
]

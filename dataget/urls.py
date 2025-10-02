from django.urls import path
from .views import get_random_media

urlpatterns = [
    path("api/random-media/", get_random_media, name="get_random_media"),
]

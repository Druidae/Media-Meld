from django.urls import path

from .views import get_info, download_video

urlpatterns = [
    path('', get_info),
    path('download-video/', download_video)
]
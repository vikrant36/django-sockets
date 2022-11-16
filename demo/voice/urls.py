"""
Contains routes for the APIs
"""

from django.urls import path
from .views import AjaxSaveAudio, VoiceApiViewSet

urlpatterns = [
    path('voice/', VoiceApiViewSet.as_view(), name='voice'),
]

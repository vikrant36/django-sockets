"""
Contains routes for the APIs
"""

from django.urls import path
from .views import AnswerApiViewSet

urlpatterns = [
    path('answer/', AnswerApiViewSet.as_view(), name='answer'),
]

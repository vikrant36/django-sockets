"""
Contains routes for the APIs
"""

from django.urls import path
from .views import AnswerApiViewSet, QuestionApiViewSet

urlpatterns = [
    path('answer/', AnswerApiViewSet.as_view(), name='answer'),
    path('question/', QuestionApiViewSet.as_view(), name='question'),

]

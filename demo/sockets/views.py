from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Answer
from .serializers import AnswerSerializer
# Create your views here.


class AnswerApiViewSet(APIView):
    """"""

    model_class = Answer
    serializer_class = AnswerSerializer

    def get_object(self, pk):
        """helper to get specific object from Candidate Model"""

        return self.model_class.objects.get(pk=pk)

    def get(self, request, pk=None, format=None):
        """"""
        if pk is None:
            seed = self.model_class.objects.all()
            serializer = self.serializer_class(seed, many=True)
            return Response(serializer.data)
        else:
            seed = self.get_object(pk)
            serializer = self.serializer_class(seed)
            return Response(serializer.data)


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Answer
from .serializers import AnswerSerializer
from .consumers import DummyGoogleClient
# Create your views here.


def get_questions():
    """"""
    return [{"id": 1, "question": "Hi how are you"}]


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


class QuestionApiViewSet(APIView):
    """"""
    question_list = get_questions()
    localGoogleClient = DummyGoogleClient()

    def get(self, request, pk=None, format=None):
        """"""
        if len(self.question_list)==0:
            res = {
            "question": "HUME nahi puchna",
            "audio": None,
            "isEnded": True
            }
            return Response(res)

        cur_ques = self.question_list.pop()
        tts_res = self.localGoogleClient.dummy_tts(cur_ques)
        res = {
            "question": cur_ques,
            "audio": tts_res,
            "isEnded": False

        }
        return Response(res)

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView, View
from rest_framework.response import Response
from .models import Voice
from .serializer import VoiceSerializer
# Create your views here.


class AjaxSaveAudio(View):
    """Use ajax to save audio sent by user."""

    def post(self, request):
        """Save recorded audio blob sent by user."""
        audio_file = request.FILES.get('recorded_audio')
        my_obj = Voice() # Put aurguments to properly according to your model
        my_obj.audio = audio_file
        my_obj.save()
        return JsonResponse({
            'success': True,
        })


class VoiceApiViewSet(APIView):
    """"""

    model_class = Voice
    serializer_class = VoiceSerializer

    def post(self, request):
        """"""
        audio_file = request.FILES.get('audio')
        my_obj = Voice()  # Put aurguments to properly according to your model
        my_obj.audio = audio_file
        my_obj.save()
        return JsonResponse({
            'success': True,
        })

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



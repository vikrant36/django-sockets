from rest_framework import serializers
from .models import Voice


class VoiceSerializer(serializers.ModelSerializer):
    """Serializer for Candidate Model"""
    class Meta:
        model = Voice
        fields = "__all__"

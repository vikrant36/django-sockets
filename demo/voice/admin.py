from django.contrib import admin
from voice.models import Voice
# Register your models here.


@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Voice model
    """
    list_display = ["id", "audio"]

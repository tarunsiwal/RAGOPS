from rest_framework import serializers
from .models import ChatLog

class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = ['user_query', 'ai_response', 'prompt']
from django.contrib import admin
from .models import ChatHistory, ChatLog, UploadedFile

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_id', 'timestamp')

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_id','prompt', 'chat_name', 'pricing', 'timestamp')
    search_fields = ('user__username', 'chat_id')

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_id', 'user_query', 'ai_response', 'prompt', 'timestamp')
    search_fields = ('user__chat_id', 'user_query', 'ai_response', 'prompt')

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_history', 'file', 'upload_timestamp')
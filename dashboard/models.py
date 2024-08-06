from django.db import models
from django.contrib.auth.models import User


class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=100)
    chat_name = models.TextField(default='United chat')  # Store the messages in a serialized format
    prompt = models.TextField(blank=True)
    pricing = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.chat_id} - {self.timestamp} - {self.pricing}"
    
class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # chat_history = models.ForeignKey(ChatHistory, on_delete=models.CASCADE, null=True, blank=True)
    chat_id = models.CharField(max_length=100, db_index=True)
    user_query = models.TextField(blank=True)
    ai_response = models.TextField(blank=True)
    prompt = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)



class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_history = models.ForeignKey(ChatHistory, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploaded_files/')
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.chat_history.chat_id} - {self.file.name}"


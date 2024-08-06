from .models import UploadedFile
from django import forms

class UserQueryForm(forms.Form):
    user_query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your query...'}))


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
    
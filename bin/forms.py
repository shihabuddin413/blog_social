from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'attachment']
        labels = {
            'text':'',
            'attachment':'',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows':2, 'class':'form-control ', 'placeholder':'Write a message...'}),
            'attachment': forms.FileInput(attrs={'class':'form-control '})
        }

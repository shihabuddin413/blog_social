
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Conversation(models.Model):
    # Option: unique constraint to prevent duplicate pair conversations (unordered)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Conversation: " + ", ".join([u.username for u in self.participants.all()])

    def other_participant(self, user):
        return self.participants.exclude(pk=user.pk).first()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    attachment = models.FileField(upload_to='messages/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"Msg from {self.sender.username} at {self.created_at}"

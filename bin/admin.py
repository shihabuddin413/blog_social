from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'created_at', 'text_short')
    readonly_fields = ('created_at',)

    def text_short(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text
    text_short.short_description = 'Text'

from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('role','content','created_at')
    list_filter = ('role','created_at')


# Customize admin site texts
admin.site.site_header = "UCU BBUC Administration"
admin.site.site_title = "UCU BBUC Admin Portal"
admin.site.index_title = "Welcome to UCU BBUC Admin Dashboard"

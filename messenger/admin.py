from django.contrib import admin
from .models import Message, Chat, Chat_User

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(Chat_User)
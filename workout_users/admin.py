from django.contrib import admin
from .models import User, Post, Comment, Message, Conversation

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Conversation)

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    posts = models.ManyToManyField('Post')
    followers = models.ManyToManyField('self', related_name='follower', symmetrical=False, null=True)
    followings = models.ManyToManyField('self', related_name='following', symmetrical=False, null=True)
    profile_pic = models.ImageField(max_length=10000, default='default-pfp.jpg')
    conversations = models.ManyToManyField('Conversation')

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    img = models.ImageField(max_length=10000)
    caption = models.TextField(max_length=200)
    likes = models.IntegerField(default=0)
    comments = models.ManyToManyField('Comment')
    likers = models.ManyToManyField(User, related_name='liked_post')
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField(max_length=200)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    text = models.TextField(max_length=200)
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey('User', on_delete=models.CASCADE, related_name='recipient', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Conversation(models.Model):
    users = models.ManyToManyField(User, null=True)
    messages = models.ManyToManyField(Message, null=True)
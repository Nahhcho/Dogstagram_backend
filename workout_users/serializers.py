from rest_framework import serializers
from datetime import datetime
from .models import User, Post, Comment, Message, Conversation


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        # Convert the datetime object to a custom string format for output
        return value.strftime("%Y-%m-%dT%H:%M:%S")
    
    def to_internal_value(self, value):
        try:
            # Parse the input string to a datetime object using various formats
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            # Handle invalid date formats gracefully (you can raise a validation error or return a default value)
            raise serializers.ValidationError("Invalid date format. Please use YYYY-MM-DDTHH:MM:SS format.")
    

class CommentSerializer(serializers.ModelSerializer):
    commenter = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'commenter', 'likes', 'timestamp']

class PostSerializer(serializers.ModelSerializer):
    poster = serializers.StringRelatedField()
    comments = CommentSerializer(many=True)
    likers = serializers.StringRelatedField(many=True)
    timestamp = CustomDateTimeField()

    class Meta: 
        model = Post
        fields = ['id','poster', 'img', 'caption', 'likes', 'comments', 'likers', 'timestamp']

class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    followers = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'posts', 'followers', 'followings', 'follower_count', 'following_count', 'post_count', 'profile_pic', 'conversations']

    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.followings.count()
    
    def get_post_count(self, obj):
        return obj.posts.count()

class MessageSeralizer(serializers.ModelSerializer):
    timestamp = CustomDateTimeField()
    sender = UserSerializer()
    recipient = UserSerializer()

    class Meta:
        model = Message 
        fields = ['id', 'text', 'sender', 'recipient', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSeralizer(many=True)
    users = UserSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'messages', 'users']

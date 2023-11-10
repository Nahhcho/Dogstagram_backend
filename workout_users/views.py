from rest_framework.response import Response
from rest_framework.decorators import api_view
from io import BytesIO
import json
import tensorflow as tf
from PIL import Image
import numpy as np

from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import User, Post, Comment, Message, Conversation
from .serializers import UserSerializer, PostSerializer, MessageSeralizer, ConversationSerializer
from django.views.decorators.csrf import csrf_exempt
import os

@api_view(['GET'])
def all_posts(request):
     if request.method == 'GET':
        posts = Post.objects.all().order_by('-timestamp')
        serialized_posts = PostSerializer(posts, many=True)
        return JsonResponse(serialized_posts.data, safe=False)
     
@api_view(['GET'])
def user_posts(request, users):
     if request.method == 'GET':
        user_list = users.split(',')
        users_queryset = User.objects.filter(username__in=user_list)
        
        # Fetch posts related to the selected users
        posts = Post.objects.filter(user__in=users_queryset)
        serialized_posts = PostSerializer(posts, many=True)
        return JsonResponse(serialized_posts.data, safe=False)

@api_view(['GET', 'POST'])
def conversations(request, username):
    user = User.objects.get(username=username)
    if request.method == 'GET':
        conversations = user.conversations.all()
        serialized_conversations = ConversationSerializer(conversations, many=True)
        return JsonResponse(serialized_conversations.data, safe=False, status=201)
    elif request.method == 'POST':
        data = json.loads(request.body)
        sender = user
        recipient = User.objects.get(username=data.get('recipient'))
        text = data.get('text')
        message = Message(text=text, sender=sender, recipient=recipient)
        message.save()
        conversation = Conversation()
        conversation.save()
        conversation.users.add(sender)
        conversation.users.add(recipient)
        conversation.messages.add(message)
        sender.conversations.add(conversation)
        recipient.conversations.add(conversation)
        return JsonResponse(ConversationSerializer(conversation).data, status=201)
        


@api_view(['GET', 'POST'])
def conversation_detail(request, id):
    conversation = Conversation.objects.get(pk=id)
    if request.method == 'GET':
        serialized_conversation = ConversationSerializer(conversation)
        return JsonResponse(serialized_conversation.data, status=200)
    elif request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        sender = User.objects.get(username=data.get('sender'))
        recipient = User.objects.get(username=data.get('recipient'))
        message = Message(text=text, sender=sender, recipient=recipient)
        message.save()
        conversation.messages.add(message)
        conversation.save()
        return JsonResponse({'message': 'message sent!'}, status=200)
     
@api_view(['GET', 'POST', 'DELETE'])
def post_detail(request, id):
    post = Post.objects.get(pk=id)
    if request.method == 'GET':
        serialized_post = PostSerializer(post)
        return JsonResponse(serialized_post.data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        if data.get('type') == 'comment':
            post_comment(data, post)
            return Response({'message': 'comment posted successfully!'}, status=201)
        elif data.get('type') == 'like':
            post_like(data, post)
            return Response({'message': 'likes updated successfully!'}, status=200)
    elif request.method == 'DELETE':
        post.delete()
        return JsonResponse({'message': 'post deleted!'}, status=200)

         
def post_comment(data, post):
    user = User.objects.get(username=data.get('commenter'))
    comment = Comment(text=data.get('text'), commenter=user)
    comment.save()
    post.comments.add(comment)
    return JsonResponse({'message': 'post created!'}, status=201)

def post_like(data, post):
    user = User.objects.get(username=data.get('liker'))
    username = username=data.get('liker')
    serialized_post = PostSerializer(post)
    likers = serialized_post.data['likers']
    if username in likers:
        post.likes -= 1
        post.likers.remove(user)
        post.save()
    if username not in likers:
        post.likes += 1
        post.likers.add(user)
        post.save()
        

@api_view(['DELETE'])         
def comment(request, id):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        comment = Comment(pk=data.get('id'))
        comment.delete()
        return JsonResponse({'message': 'comment deleted'}, status=201)


import boto3
@api_view(['POST'])
def new_post(request):
    if request.method == 'POST':
        s3 = boto3.client('s3')
        caption = request.data.get('caption')
        img = request.FILES['img']
        

        # Open the image file
        image_stream = BytesIO(img.read())
        image = Image.open(image_stream)
        # Resize the image while streaming
        image = image.resize((256, 256))

        # Convert the image to a NumPy array and normalize
        image_array = np.array(image) / 255.0
        image_stream.close()
        # Expand dimensions to match the input shape expected by the model
        image_array = np.expand_dims(image_array, axis=0)

        bucket_name = 'dogstagram-images'
        model_file_name = 'model.h5'
        local_model_file_name = 'local-model-file-name'  # Specify the local file name to save the downloaded model

        # Download the model file from S3
        s3.download_file(bucket_name, model_file_name, local_model_file_name)

        # Load the model from the downloaded file
        model = tf.keras.models.load_model(local_model_file_name)


        prediction = model.predict(image_array)

        percentage = round(1 - prediction[0][0], 2)*100
        print(prediction)
        os.remove(local_model_file_name)

        if prediction < .5:
            poster = User.objects.get(username=request.data.get('poster'))
            poster = User.objects.get(username=request.data.get('poster'))
            post = Post(caption=caption, img=img, poster=poster)
            post.save()
            poster.posts.add(post)
            return JsonResponse({'message': 'post created!', 'prediction': f"{percentage})%"}, status=201)
        else:
            return JsonResponse({'message': "That's not a dog!", 'prediction': f"{percentage}%"}, status=201)
                  

@api_view(['GET', 'POST'])
def user(request, id):
    if request.method == 'GET':
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

@api_view(['GET', 'PUT'])
def profile(request, username):
    serialized_user = UserSerializer(User.objects.get(username=username)).data
    if request.method == 'GET':
        return JsonResponse(serialized_user, safe=False)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        user = User.objects.get(username=username)
        session_user = User.objects.get(username=data.get('follower'))
        if session_user.username in serialized_user['followers']:
            user.followers.remove(session_user)
            user.save()
            session_user.followings.remove(user)
            session_user.save()
            return JsonResponse({"message": 'unfollow'}, status=200)
        else:
            user.followers.add(session_user)
            user.save()
            session_user.followings.add(user)
            session_user.save()
            return JsonResponse({"message": 'follow'}, status=200)

@api_view(['POST'])
def login(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get("username")
    password = data.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, status=201)
    else:
         return JsonResponse({"message": 'invalid credentials'}, status=401)


@api_view(['POST'])
def register(request):

        # Ensure password matches confirmation
        data = json.loads(request.body.decode('utf-8'))
        username = data.get("username")
        password = data.get("password")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return JsonResponse({'message': 'user created!'}, status=201)
        except IntegrityError as e:
            print(e)
            return JsonResponse({'error': 'username already exists'})
        
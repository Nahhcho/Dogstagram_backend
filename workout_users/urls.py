"""
URL configuration for workout_users project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('all_posts', views.all_posts),
    path("posts/<str:users>", views.user_posts),
    path('post_detail/<int:id>', views.post_detail),
    path("user/<int:id>", views.user),
    path('comment/<int:id>', views.comment),
    path("login", views.login),
    path('register', views.register),
    path('new_post', views.new_post),
    path('profile/<str:username>', views.profile),
    path('messages/<str:username>', views.conversations),
    path('conversation/<int:id>', views.conversation_detail),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

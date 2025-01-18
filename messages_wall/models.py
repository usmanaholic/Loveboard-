
from django.db import models
from django.contrib.auth.models import User

class Theme(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    background_music = models.FileField(upload_to='themes/music/', null=True, blank=True)
    background_image = models.ImageField(upload_to='themes/images/', null=True, blank=True)

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    background_color = models.CharField(max_length=7, default='#ffffff')
    font_style = models.CharField(max_length=50, default='Arial')
    
class MediaAttachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    type = models.CharField(max_length=20)  # 'image', 'gif', 'audio'
    
class Timeline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='timeline/')
    
class SpecialDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    reminder = models.BooleanField(default=False)
    
class MessageWall(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    custom_url = models.SlugField(unique=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

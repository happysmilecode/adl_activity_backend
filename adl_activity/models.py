from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser, Group, Permission, User
import os

def user_directory_path(instance, filename):
    return 'user_{0}\{1}'.format(instance.user.id, filename)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    birthday = models.DateField(null=True)
    
    groups = models.ManyToManyField(Group, related_name='adlactivity_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='adlactivity_user_permissions')

    def __str__(self):
        return self.email

class SwipeModality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True)
    json_data = JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.json_data}"

class PhysicalModality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True)
    json_data = JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.json_data}"
    
class DeviceDropModality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True)
    json_data = JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.json_data}"
    
class TypingMonitorModality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True)
    json_data = JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.json_data}"
    
class VoiceModality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True)
    json_data = JSONField(null=True, blank=True)
    audio = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.json_data}"
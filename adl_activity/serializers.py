from rest_framework import serializers
from .models import User, SwipeModality, PhysicalModality, DeviceDropModality, TypingMonitorModality, VoiceModality
from django.conf import settings
import os
from .utils import analyze_audio
from .models import user_directory_path

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        email = validated_data.get('email')
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists")
        
        user = User.objects.create(**validated_data)
        
        user.groups.set(groups)
        user.user_permissions.set(user_permissions)
        
        return user
    
class SwipeModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SwipeModality
        fields = '__all__'
        
class PhysicalModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalModality
        fields = '__all__'
        
class DeviceDropModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDropModality
        fields = '__all__'
        
class TypingMonitorModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypingMonitorModality
        fields = '__all__'
        
class VoiceModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceModality
        fields = '__all__'
        
    # def create(self, validated_data):
    #     # Extract the audio file from validated_data
    #     audio_file = validated_data.pop('audio', None)
        
    #     # Create the instance without saving it yet
    #     instance = super().create(validated_data)
    #     instance.save()
        
    #     # Perform analysis if audio file exists
    #     if audio_file:
    #         file_path = os.path.join(settings.MEDIA_ROOT, user_directory_path(instance, str(audio_file)))
            
    #         # Perform your analysis on file_path
    #         # Example analysis:
    #         print(f"Analyzing file at path: {file_path}")

    #         if os.path.exists(file_path):
    #             # Perform your analysis on file_path
    #             print(f"Analyzing file at path: {file_path}")
    #             user_friendly_result = analyze_audio(file_path)
                
    #             # Update the instance with analysis result
    #             instance.json_data = {
    #                 'data': user_friendly_result
    #             }
    #             instance.save()  # Save the instance after updating json_data
    #         else:
    #             print(f"File does not exist at path: {file_path}")
        
    #     return instance
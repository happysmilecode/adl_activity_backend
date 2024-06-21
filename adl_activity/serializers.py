from rest_framework import serializers
from .models import User, SwipeModality, PhysicalModality, DeviceDropModality, TypingMonitorModality, VoiceModality

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
from django.shortcuts import render
from rest_framework import viewsets, parsers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import UserSerializer, SwipeModalitySerializer, PhysicalModalitySerializer, DeviceDropModalitySerializer, TypingMonitorModalitySerializer, VoiceModalitySerializer
from .models import User, SwipeModality, PhysicalModality, DeviceDropModality, TypingMonitorModality, VoiceModality

from .utils import analyze_audio, describe_results, assess_interaction_ability
import os
from .models import user_directory_path
from django.conf import settings

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email is None or password is None:
            return None
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid email or password')
        
        if not check_password(password, user.password):
            raise AuthenticationFailed('Invalid email or password')

        return (user, None)
    
# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.JSONParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def create(self, request):
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_instance = serializer.save()
            serializer_user = UserSerializer(user_instance)
            response_data = {'data': serializer_user.data}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        user = CustomAuthentication().authenticate(request)
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user_id': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], authentication_classes=[JWTAuthentication])
    def profile(self, request):
        print("User Profile: ", request)
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated], authentication_classes=[JWTAuthentication])
    def update_profile(self, request):
        user = request.user
        data = request.data
        
        if 'username' in data:
            user.username = data['username']
        
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SwipeModalityViewSet(viewsets.ModelViewSet):
    queryset = SwipeModality.objects.all()
    serializer_class = SwipeModalitySerializer

class PhysicalModalityViewSet(viewsets.ModelViewSet):
    queryset = PhysicalModality.objects.all()
    serializer_class = PhysicalModalitySerializer

class DeviceDropModalityViewSet(viewsets.ModelViewSet):
    queryset = DeviceDropModality.objects.all()
    serializer_class = DeviceDropModalitySerializer

class TypingMonitorModalityViewSet(viewsets.ModelViewSet):
    queryset = TypingMonitorModality.objects.all()
    serializer_class = TypingMonitorModalitySerializer

class VoiceModalityViewSet(viewsets.ModelViewSet):
    queryset = VoiceModality.objects.all()
    serializer_class = VoiceModalitySerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    @action(detail=False, methods=['post'])
    def analyze_data(self, request):
        pk = request.data.get('pk')
        print('Pk:', pk)
        try:
            instance = VoiceModality.objects.get(pk=pk)
        except VoiceModality.DoesNotExist:
            return Response({'error': 'VoiceModality instance not found.'}, status=status.HTTP_200_OK)
        
        if not instance.audio:
            return Response({'error': 'No audio file associated with this instance.'}, status=status.HTTP_200_OK)
        
        file_path = os.path.join(settings.MEDIA_ROOT, str(instance.audio))
        print(f"Viewset Analyzing file at path: {file_path}")
        
        user_friendly_result = analyze_audio(file_path)
        instance.json_data = {
            'data': user_friendly_result
        }
        instance.save()

        return Response({
            'data': instance.json_data,
        }, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
        
    #     response = super().create(request, *args, **kwargs)
    #     instance = self.get_object()
        
    #     if instance.audio:
    #         file_path = instance.audio.path
            
    #         user_friendly_result = analyze_audio(file_path)
    #         instance.json_data = {
    #             'data': user_friendly_result
    #         }
    #         instance.save()
        
    #     return Response(VoiceModalitySerializer(instance).data, status=status.HTTP_201_CREATED)
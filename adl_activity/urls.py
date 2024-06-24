from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

router = SimpleRouter()

router.register('api/v1/users', views.UserViewset)
router.register('api/v1/modalities/physical-modality', views.PhysicalModalityViewSet)
router.register('api/v1/modalities/device-drop-modality', views.DeviceDropModalityViewSet)
router.register('api/v1/modalities/swipe-modality', views.SwipeModalityViewSet)
router.register('api/v1/modalities/voice-modality', views.VoiceModalityViewSet)
router.register('api/v1/modalities/typing-monitor-modality', views.TypingMonitorModalityViewSet)

urlpatterns = router.urls + [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from .views import LoginView,RegistrationAPIView,NearHospitalsList,DistanceAPICall


urlpatterns = [
    path('login_view/', LoginView.as_view()),
    path(r'register_user/', RegistrationAPIView.as_view(), name='Register'), 
    path(r'near_hospitals_list/', NearHospitalsList.as_view(), name='Register'),
    path(r'distance/', DistanceAPICall.as_view(), name='Register')
    
    ]

from django.conf import settings

from django.conf.urls.static import static

# if settings.DEBUG:

urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)
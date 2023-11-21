from django.urls import path
from .views import RaiseRequest,hospital_Dash_bord,hospital_request_Accept, LoginView,RegistrationAPIView,NearHospitalsList,get_hospital_details_single,Userprofileview,HospitalsLiveLocation,Userprofileview_update


urlpatterns = [
    path(r'login_view/', LoginView.as_view()),
    path(r'register_user/', RegistrationAPIView.as_view(), name='Register'), 
    path(r'near_hospitals_list/', NearHospitalsList.as_view(), name='Register'),
    path(r'distance/<str:hospital_name>', get_hospital_details_single.as_view(), name='Register'),
    path(r'user_profile/<str:user_type>', Userprofileview.as_view(), name='Register'),
    path(r'hospital_address/', HospitalsLiveLocation.as_view(), name='Register'),
    path(r'user_profile_update/<str:user_type>', Userprofileview_update.as_view(), name='Register'),
    path(r'user_request/', RaiseRequest.as_view(), name='Register'),
    path(r'accepted_user_request/', hospital_request_Accept.as_view(), name='Register'),
    path(r'get_all_user_requests/', hospital_Dash_bord.as_view(), name='Register'),
    
    ]

from django.conf import settings

from django.conf.urls.static import static

# if settings.DEBUG:

urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)
from django.urls import path
from .views import ride_complete_button,driver_start_button,user_status,RaiseRequest,driver_dashboard,hospital_Dash_bord,hospital_request_Accept, Login_View,RegistrationAPIView,NearHospitalsList,get_hospital_details,Userprofileview,get_address_from_long_lat,Userprofileview_update


urlpatterns = [
    path(r'login_view/', Login_View.as_view()),
    path(r'register_user/', RegistrationAPIView.as_view(), name='Register'), 
    path(r'near_hospitals_list/', NearHospitalsList.as_view(), name='Register'),
    path(r'get_hospital_details/<str:hospital_name>', get_hospital_details.as_view(), name='Register'),
    path(r'user_profile/<str:user_type>', Userprofileview.as_view(), name='Register'),
    path(r'get_address_from_long_lat/', get_address_from_long_lat.as_view(), name='Register'),
    path(r'user_profile_update/<str:user_type>', Userprofileview_update.as_view(), name='Register'),
    path(r'user_request/', RaiseRequest.as_view(), name='Register'),
    path(r'accepted_user_request/', hospital_request_Accept.as_view(), name='Register'),
    path(r'get_all_user_requests/', hospital_Dash_bord.as_view(), name='Register'),
    path(r'driver_dashbord/', driver_dashboard.as_view(), name='Register'),
    path(r'user_status/', user_status.as_view(), name='Register'),
    path(r'driver_start_button/', driver_start_button.as_view(), name='Register'),
    path(r'ride_complete_button/', ride_complete_button.as_view(), name='Register'),
    
    ]

from django.conf import settings

from django.conf.urls.static import static

# if settings.DEBUG:

urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)
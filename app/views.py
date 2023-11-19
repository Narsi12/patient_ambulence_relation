import pymongo
import jwt
import requests
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from .models import USER_Entry, Driver_Entry, Hospital
from .serializers import USER_EntrySerializer, Driver_EntrySerializer, HospitalSerializer
from rest_framework import status
from django.http import JsonResponse
from mail_notification.connection import MailConfig
from datetime import datetime, timedelta
from django.conf import settings
from .helper import EmailBackend,calculate_distance
from googlemaps import Client as GoogleMaps
from django.utils.decorators import method_decorator
from .permissions import CustomIsauthenticated,DriverCustomIsauthenticated,HospitalCustomIsauthenticated
from .utils import token_required


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ambluence_db"]
mycol1 = mydb['app_driver_entry']
mycol2 = mydb['app_hospital']
mycol3 = mydb['app_user_entry']
tokens = mydb['tokens']




#registration api
class RegistrationAPIView(APIView):
    def post(self, request):
        user_type = request.data.get('user_type')
        password = request.data.get('password')
        email = request.data.get('email')

       
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
         # Hash the password
        hashed_password = make_password(password) 
        request.data['password'] = hashed_password
        # mutable_data = request.data.copy()
        # mutable_data['password'] = hashed_password

        
        existing_user = USER_Entry.objects.filter(email=email).first() or Driver_Entry.objects.filter(email=email).first() or Hospital.objects.filter(email=email).first()
        if existing_user is not None:
            return JsonResponse({'Message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if user_type == 'user':
            serializer = USER_EntrySerializer(data=request.data)


        elif user_type == 'driver':
            serializer = Driver_EntrySerializer(data=request.data)
            demo=MailConfig(mail_user="harikishansuri1998@gmail.com",password="mita ypfc xjel khyy")
            demo.send_mail(to_mail=email,subject="text",body=f"Dear user, your account details are being processed.\n Email: {email}")
            demo.close_conn()
            
        elif user_type == 'hospital':
            serializer = HospitalSerializer(data=request.data)
            demo=MailConfig(mail_user="harikishansuri1998@gmail.com",password="mita ypfc xjel khyy")
            demo.send_mail(to_mail=email,subject="text",body=f"Dear user, your account details are being processed.\n Email: {email}")
            demo.close_conn()
        else:
            return Response({"error": "Invalid user_type"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class LoginView(APIView):
    def post(self,request):
        data = request.data
        email = data.get('email',None)
        password = data.get('password',None)

        user=EmailBackend.authenticate(self, request, username=email, password=password)
        if user is not None:
            token_payload = {
                'user_id': str(user._id),
                'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_SETTINGS['JWT_ACCESS_TOKEN_EXPIRATION']),
                'iat': datetime.utcnow()
                }
            access_token = jwt.encode(token_payload, settings.JWT_SETTINGS["JWT_SECRET_KEY"], settings.JWT_SETTINGS["JWT_ALGORITHM"])

            refresh_token_payload = {
                'user_id': str(user._id),
                'exp': datetime.utcnow() + timedelta(days=settings.JWT_SETTINGS['JWT_REFRESH_TOKEN_EXPIRATION']),
                'iat': datetime.utcnow()
                }
            refresh_token = jwt.encode(refresh_token_payload, settings.JWT_SETTINGS["JWT_REFRESH_SECRET_KEY"], settings.JWT_SETTINGS["JWT_ALGORITHM"])

            tokens.insert_one({
                "user_id":str(user._id),
                "access_token":access_token,
                "refresh_token":refresh_token,
                "active":True,
                "created_date":datetime.utcnow()
            })

            collections = [mycol1, mycol2, mycol3]

            for collection in collections:
                details = collection.find_one({"email": email})
                if details:
                    usertype = details.get('user_type')
            
            # logedin = details['logged_in']

            return JsonResponse({
                    "status": "success",
                    "msg": "user successfully authenticated",
                    "token": access_token,
                    "refresh_token": refresh_token,
                    "email":email,
                    "usertype":usertype
                    # "loggedin":logedin
                })
        else:
            return JsonResponse({"message":"invalid data"})
        



class NearHospitalsList(APIView):
    def get(self, request):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
 
        api_key = 'AIzaSyBO0HZnIuHmIB7qalDQ-jTsT4bXbkcFLZM'
        gmaps = GoogleMaps(api_key)
 
        radius = 5000
        location = (latitude, longitude)
 
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type=hospital&key={api_key}"
 
        response = requests.get(url)
 
        if response.status_code == 200:
            hospitals_data = response.json()
       
            if 'results' in hospitals_data:
                nearby_hospitals = hospitals_data['results']
                print("\nNearby Hospitals:")
                hospitals_json = []
                for hospital in nearby_hospitals:
                    hospital_name = hospital['name']
                    hospital_opening_hours = hospital.get('opening_hours', {}).get('open_now', None)
                    hospital_location = hospital['geometry']['location']
                    hospital_lat = hospital_location['lat']
                    hospital_lng = hospital_location['lng']
 
                    ambulance_avb = mycol2.find_one({"hospital_name":hospital_name})
                    if ambulance_avb is not None:
                        ambulance = "False" if ambulance_avb['no_of_ambulances'] =="0" else "True"
                    else:
                        ambulance = "hospital not rejected"
 
                    hospital_info = {
                        "name": hospital_name,
                        "latitude": hospital_lat,
                        "longitude": hospital_lng,
                        "open_now": str(hospital_opening_hours) if hospital_opening_hours else 'Not available',
                        "ambulance_available": ambulance
                    }
                    hospitals_json.append(hospital_info)
 
                return Response(hospitals_json, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No hospital data found in the specified radius."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Failed to fetch data from Google Places API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

class DistanceAPICall(APIView): # it's used to show the distance in kilometers
    def get(self, request):
        data = request.data
        lat1 = data.get('lat1')
        lon1 = data.get('lon1')
        lat2 = data.get('lat2')
        lon2 = data.get('lon2')

        if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
            return Response({"message": "Latitude or longitude values are missing."}, status=400)

        distance,maps_link = calculate_distance(lat1, lon1, lat2, lon2)
        if distance is not None:
            return Response({
                "distance": distance,
                "location": maps_link
            })
        
        else:
            return Response({"message": "Failed to calculate distance."}, status=500)
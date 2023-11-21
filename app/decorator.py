from geopy.geocoders import GoogleV3
import requests


def address_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        api_key = 'AIzaSyBO0HZnIuHmIB7qalDQ-jTsT4bXbkcFLZM'  # Replace with your actual Google Maps API key
        geolocator = GoogleV3(api_key=api_key)
        
        latitude = request.GET.get('latitude', None)
        longitude = request.GET.get('longitude', None)
        
        if latitude is not None and longitude is not None:
            location = f"{latitude}, {longitude}"
            
            try:
                address = geolocator.reverse(location)
                result = address.address if address else "Address not found"
                return func(self, request, *args, latitude=latitude, longitude=longitude, result=result, **kwargs)
            except Exception as e:
                return func(self, request, *args, latitude=latitude, longitude=longitude, result=f"Error: {str(e)}", **kwargs)
        else:
            return func(self, request, *args, latitude=None, longitude=None, result="Latitude or longitude not provided", **kwargs)

    return wrapper
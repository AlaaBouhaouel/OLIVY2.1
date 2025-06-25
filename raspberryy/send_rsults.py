#fl raspberry :
import requests

def send_incident_data(latitude, longitude):
    data = {
        'latitude': latitude,
        'longitude': longitude
    }
    url = 'http://127.0.0.1:8000/from_drone/'
    response = requests.post(url, data=data)
    return response.json()


latitude = 123.456  
longitude = 78.910  
response = send_incident_data(latitude, longitude)
print(response)

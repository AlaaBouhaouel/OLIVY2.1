
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os
from django.conf import settings
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import numpy as np
import cv2
import tensorflow as tf
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image
from django.http import JsonResponse
from django.http import HttpResponse
import matplotlib.pyplot as plt
import statistics
from io import BytesIO
import base64
from geopy.geocoders import Nominatim  
from django.core.mail import send_mail
from .models import users_data

from django.contrib import messages
from .models import DiseaseIncident

from datetime import datetime, date
from meteostat import Point, Daily
import matplotlib
from django.shortcuts import render
from .models import DiseaseIncident
from django.core.mail import EmailMessage
import random
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from django.views.decorators.csrf import csrf_exempt
#run once 
#nltk.download('punkt')
#nltk.download('wordnet')


model_path = r"disease_detection\Aimodels\,2"

def index (request):
    return render(request , 'index.html')   



def prediction_model(image_file):
    image_data = image_file.read()

    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), 1)
    imge = cv2.resize(img, (256, 256))
    

    
    input_image = np.array(imge)
    if input_image is not None and input_image.all():

        model = tf.keras.models.load_model(model_path)

        class_names = ['Aculos', 'Healthy', 'olive peacock']

        img_array = tf.keras.preprocessing.image.img_to_array(input_image)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array)
        print ('prediction ...')
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * (np.max(predictions[0])), 2)

        print(predicted_class)
        print('confidence:', confidence)
    return predicted_class , confidence








# ***********************************************still testing********************************************************
#UPDATES: the prediction works well but it is using StreamingHttpResponse which is used to desplay streamed vdos with no html attachements 
#we need to continously send the frames to the html to get a life time vdo GOOD LUCK 



def detect_leaf(frame, model,disease_model):
    frame_vierge= frame 

    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    img = cv2.resize(frame, ( 224, 224))
    #//////////////expected shape=(None, 224, 224, 3),
    yhat = model.predict(np.expand_dims(img / 255, 0))
    print(yhat)
    if yhat[0][0] < 0.7:
        print(f'Predicted class is not leaf')
    else:
        print(f'Predicted class is leaf')
        h, w, _ = frame.shape
        leaf_x = int(w * 0.25)  # Example values, adjust as needed
        leaf_y = int(h * 0.25)  # Example values, adjust as needed
        leaf_w = int(w * 0.5)   # Example values, adjust as needed
        leaf_h = int(h * 0.5)   # Example values, adjust as needed
        cv2.rectangle(frame, (leaf_x, leaf_y), (leaf_x + leaf_w, leaf_y + leaf_h), (0, 255, 0), 2)

        #expected shape=(None, 256, 256, 3),
        #img is the resised one 
        #frame with the rectangles of the leafs 
        if yhat[0][0] > 0.9:
            frame = process_disease(frame, frame_vierge, disease_model)

    return frame 

def process_disease(frame, frame_vierge, model):
    class_names = ['Aculos', 'Healthy', 'olive peacock']
    img = cv2.resize(frame_vierge, ( 256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    print('Prediction...')
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * np.max(predictions[0]), 2)
    print (predictions)
    print(predicted_class)
    print('Confidence:', confidence)

    # Draw predicted disease and confidence on the frame
    cv2.putText(
        frame,
        f'Predicted disease: {predicted_class}',
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )
    cv2.putText(
        frame,
        f'Confidence: {confidence}',
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    return frame








def video_feed_page(request):
    # Render the HTML template
    return render(request, 'disease_detection/cam.html')

#video_feed is just a streaming vdo that i wanna include in th emali webcame page 
#called video_feed_page ,so the question can i call the streaming  vdo in my html coding ? (cam.html)  








def video_feed(request):
    leaf_model_path = "disease_detection\Aimodels\leafModel.h5"
    disease_model_path = "disease_detection\Aimodels\,2"

    leaf_model = tf.keras.models.load_model(os.path.abspath(leaf_model_path))
    disease_model = tf.keras.models.load_model(os.path.abspath(disease_model_path))

    # Function to stream video frames
    return StreamingHttpResponse(generate_frames(leaf_model, disease_model), content_type='multipart/x-mixed-replace; boundary=frame')


import time

def generate_frames(leaf_model, disease_model):
    # Access the webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Call object detection function//////////////expected shape=(None, 224, 224, 3),expected shape=(None, 256, 256, 3),
        processed_frame = detect_leaf(frame, leaf_model, disease_model)

        # Convert processed frame to JPEG
        _, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

# ********************************blo*blo*blo*blo*blo*****************************************************************************



def detection_image(request):
    print ('in the view ')
    if request.method == 'POST':
        #get the user address from the drone 
        longitude=35.666
        latitude=112.546
        user_email = request.POST.get('email')
        print('good', user_email) if user_email is not None else print ('no email')
        #********************************************still testing ************************************************
        # i wanna save the email the moment it comes to the view function and then remember it as the last element in the model , 
        # because whene the user load this page and enter his email the page will instantly refrech which will means that this view function 
        # will ever get the email data or the image data , while i need bothof them . 
        #save the email in a model 

        if user_email is not None :
            user_email_instance = users_data(user_name = 'User' , user_email =user_email)
            user_email_instance.save() 
            print('Email saved:', user_email)



        uploaded_image = request.FILES['image']
        
        # Process the uploaded image here, and if it's successful, respond with a JSON success message
        if uploaded_image:
            print ('GOT THE IMAGE !!')
            predicted_class , confidence = prediction_model(uploaded_image)
            print ('predicted_class  ======> ' , predicted_class)
            print ('confidence       ======> ' , confidence)

            try:
                user_datas = users_data.objects.all()

                # Get the last elementt
                last_record = user_datas.last()

                # Access the last email of the last registered user
                user_email = last_record.user_email
                print(f"Username        : {user_email}")
                #'Aculos', 'Healthy', 'olive peacock'
                if predicted_class == 'Aculos' or predicted_class == 'olive peacock': #save the user's coordinates     
                    print ('User Crop Adress is saving.........')

                    if latitude and  longitude :    
                        print('location is in the database ++++++' )
                        print(longitude ,latitude  )
                        incident = DiseaseIncident(
                            name="User Submission",
                            description=latitude +longitude,
                            longitude=longitude,
                            latitude=latitude,
                        )
                        incident.save()
                        messages.success(request, 'Coordinates saved successfully.')
                    else:
                        print ('got nothing as user adress!!!!!!!')


            except users_data.DoesNotExist:
                print("*******************smth went wrong when accessing the last user's email !************")
            return JsonResponse({'success': True,'predicted_class':predicted_class ,'confidence':confidence })
        else:
            print ( 'uploaded_image is none **********************************')
            return JsonResponse({'success': False})
    return render(request, 'disease_detection/import_image.html') 


matplotlib.use('Agg') 
from meteostat import Point, Daily
from datetime import datetime, date
def weather_view(request, lat=None, lng=None, email=None):
    if lat is None or lng is None:
        print("Coordinates are not provided.")
        lat,lng =49.2827 , -123.1207              #For Now , When we wiill make the sign in page we will get these informations from the user 
        if email is None:
            print("User email                 = ellabouhawel@gmail.com ")
            email='ellabouhawel@gmail.com'      #For Now , When we wiill make the sign in page we will get these informations from the user 
    else :
        print("Coordinates are send successfully :).")

        lat = round(float(lat), 5) 
        lng = round(float(lng), 5)
    print ('weather view function ; .............lat =',lat ,'type =',type(lat), '..........lng =', lng ,'type =',type(lng), '...............email = ', email,'type =',type(email))
    messages = {}
    context = {    'email_sent': False,  }

    

    today = date.today().strftime("%Y, %m, %d")
    td = date.today()
    y=int(td.strftime("%Y"))
    m=int(td.strftime("%m"))
    d=int(td.strftime("%d"))
    start = datetime(2024, 1, 1)
    end = datetime(y ,m ,d)

    print ("*************start:",start, "  /end:", end)
    vancouver = Point(lat, lng, 50)
    try:
        data = Daily(vancouver, start, end)
        data = data.fetch()
        
        # Check if data is not empty
        if not data.empty:
            print("                               Data Retrieved")
            print(data.head())  # Display the first few rows
            print(data.dtypes)  # Display data types of the DataFrame
        else:
            print("No data available for the specified location and date range.")
    except Exception as e:
        print("An error occurred:", str(e))




    if not data.empty:
        print('                               data     ......         ')
        print(data.head())
        print(data.dtypes)

        fig, ax = plt.subplots()
        data.plot(y=['tavg', 'tmin', 'tmax'], ax=ax)
        plt.title("Average temperature data") 

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        plot_data = buffer.getvalue()
        plot_data_uri_temp = "data:image/png;base64,"  + base64.b64encode(plot_data).decode('utf-8')

        data.plot(y=['snow'])
        plt.title("Snow Data") 
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        plot_data = buffer.getvalue()
        plot_data_uri_snow = "data:image/png;base64," + base64.b64encode(plot_data).decode('utf-8')



        data.plot(y=['prcp'])
        plt.title("precipitation data for 2023") 
        buffer = BytesIO()
        plt.savefig(buffer, format='png')

        plt.close(fig)
        buffer.seek(0)
        plot_data = buffer.getvalue()
        plot_data_uri_prcp = "data:image/png;base64,"  + base64.b64encode(plot_data).decode('utf-8')
    
        plt.title("Precipitation data")
        moin = td.strftime("%B")
        print ("the moin is :",moin)



        start1 = datetime(2013, 1, 1)

        end1 = datetime(y ,m ,d)

        data = Daily(vancouver, start1,end1)
        data = data.fetch()

        data.plot(y=['prcp'])
        plt.title("precipitation data since 2013")
        plt.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        plot_data = buffer.getvalue()
        plot_data_2012_prcp = "data:image/png;base64,"  + base64.b64encode(plot_data).decode('utf-8')
    


        if moin =="March" or moin=="February":
            messages['harvesting'] = 'It is the harvesting season!' 

        temp_data= data['tavg'][-15:-1]
        prcp_data= data['prcp'][-15:-1]

        print('precipitation data:\n',prcp_data)
        print('temperature data:\n',temp_data)
        avrg_prcp_data = statistics.mean(prcp_data)
        avrg_temp_data = statistics.mean(temp_data)
    
        avrg_prcp_data=round (avrg_prcp_data,2)
        avrg_temp_data=round (avrg_temp_data,2)

        avrg_prcp_datastr=str(avrg_prcp_data)+"cm"
        avrg_temp_datastr=str(avrg_temp_data)+"°C"

        print (f'the average of the precipitation the last 15 days ={avrg_prcp_data}')
        print (f'the average of the temperature the last 15 days ={avrg_temp_data}')
    

        if avrg_prcp_data <1.5 and avrg_temp_data> 23 :
            print ('you should water your crop.')
            messages['irrigate']='you should water your crop.'
            watering_rapport='watering_rapport'

    
            #NOT WORKING :   send_mail('Olivy wanted to inform you ', messages['irrigate'], settings.EMAIL_HOST_USER, email)

        else :
            context['email_sent'] = True
            print ( 'send via email ..')
            messages['irrigate']="Hey , the weather is not dry ,your trees are OKEY !"

        print ('cooooordinations ', lat , lng)
        # Dummy data for context (replace with actual data processing results)
        context = {
            'today': today,
            'avg_precipitation': avrg_prcp_datastr,
            'avg_temperature': avrg_temp_datastr,
            'temp_plot': plot_data_uri_temp,
            'precp_plot': plot_data_uri_prcp,
            'precp_plot2012':plot_data_2012_prcp,
            'snow_plot': plot_data_uri_snow,
            'messages': messages,
            'email_sent': False,
        }
        
    else:
        print('...............No data available for the specified date range..........')  
        context = {
            'today': None,
            'avg_precipitation': None,
            'avg_temperature': None,
            'temp_plot': None,
            'precp_plot': None,
            'precp_plot2012':None,

            'snow_plot': None,
            'messages': None,
            'email_sent': False,
        }

    return render(request, 'disease_detection/weather.html', context)














def geocode_address(address):
    geolocator = Nominatim(user_agent="disease_detection")
    if address:
        print(f"Address received: {address}")

        location = geolocator.geocode(address)
        
        if location:
            longitude = location.longitude
            latitude = location.latitude
            return latitude, longitude
        else:
            print("Error: Unable to geocode address")
            return None  # or you could return a default location
    else :
        print('                    the adress is not passing properly   ')
        return None

from django.shortcuts import redirect

def map_view(request):
    incidents_query = DiseaseIncident.objects.all().values('name', 'description', 'latitude', 'longitude')
    incidents_list = list(incidents_query)
    print(incidents_list)
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [incident['longitude'], incident['latitude']]
                },
                "properties": incident
            }
            for incident in incidents_list
        ]
    }

    
    if request.method == 'POST':
        address = request.POST.get('user_address')
        email = request.POST.get('user_email')
        adress = geocode_address(address)
        if adress :    
            latitude, longitude = adress 
            print('location is in the model' )
            print(longitude ,latitude  )
            incident = DiseaseIncident(
                name="User Submission",
                description=address,
                longitude=longitude,
                latitude=latitude,
            )
            incident.save()

            messages.success(request, 'Coordinates saved successfully.')
            return redirect('weather_with_coords', lat=latitude, lng=longitude,email=email)

        else:
            print ('got nothing as user adress')
            return redirect('weather_with_coords', lat=None, lng=None,email=email)

    return render(request, 'disease_detection/map.html',  {'incidents': json.dumps(geojson_data)})






lemmatizer =WordNetLemmatizer()
intents = json.loads(open('disease_detection/olivy_chat/intents_olivy.json').read())

words= pickle.load(open('disease_detection/olivy_chat/words.pkl', 'rb'))
classes = pickle.load(open('disease_detection/olivy_chat/classes.pkl', 'rb'))
model= load_model('disease_detection/olivy_chat/chatbot_model_olivy.h5')
def clean_up_sentence (sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag =[0] *len(words)
    for w in sentence_words:
        for i, word in enumerate (words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow= bag_of_words(sentence)
    res = model.predict(np.array ([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i , r in enumerate (res) if r > ERROR_THRESHOLD]

    results.sort(key = lambda x: x[1], reverse = True)
    return_list = []
    for r in results :
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list , intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def Olivy_chat (request):
    if request.method == 'POST':
        user_message = request.POST.get('message' , '')
        intents = json.loads(open('disease_detection/olivy_chat/intents_olivy.json').read())
        ints = predict_class(user_message)
        chatbot_response = get_response(ints ,intents)
        
        time.sleep(1)

        return JsonResponse({'message': user_message, 'response': chatbot_response})
    return render(request, 'disease_detection/Olivy_chat.html')






#**********************************************NOT WORKING *********************************
#the connection in the 587 port is appearently denied : Port 587 is closed on 185.53.178.51.Port 587 is closed on 185.53.178.51.
# try other methods , check youtube for any idea how to send emails in django 

def send_email(recipient_email, pdf_file_path):

        print (recipient_email,'email sent successfully ' , pdf_file_path)








def test (request):
    return render(request, 'disease_detection/test.html')






@csrf_exempt
def from_drone(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        DiseaseIncident.objects.create(
            name='UserName',
            description='No description',
            latitude=latitude,
            longitude=longitude
        )

        return JsonResponse({'message': 'Context received and saved successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})




#ignore it , it didnot change anything 

#sometimes the firewall blocks the port and the email sending fails 

#To ensure that your firewall allows outgoing connections on port 587, you need to create a rule to allow this. The steps may vary depending on the firewall software you are using.


#Here are some examples:

#Windows Defender Firewall:
#Press Windows + R, type "wf.msc", and press Enter.
#Click on "Outbound Rules" on the left pane.
#Click on "New Rule..." on the right pane.
#In the "New Outbound Rule Wizard", select "Custom" and click "Next".
#In the "Program" section, click "Next".
#In the "Protocol and Ports" section, select "TCP" and enter "587" in the "Local port" field. Click "Next".
#In the "Scope" section, specify the remote IP addresses to which you want to allow the outbound connections, if needed. Click "Next".
#In the "Action" section, select "Allow the connection". Click "Next".
#In the "Profile" section, make sure all the applicable profiles (Domain, Private, Public) are selected. Click "Next".
#In the "Name" section, enter a name for the rule (e.g., "SMTP Port 587") and click "Finish".
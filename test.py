import cv2
from datetime import datetime
from gtts import gTTS
import os
import requests

resource_url = "https://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SR/SR-AQ/SR-AQ-KH95-00/Data/la"
headers = {"X-M2M-Origin":"iiith_guest:iiith_guest", "Content-Type": "application/json"}
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

current_datetime = datetime.now()
formated_datetime=current_datetime.strftime("%H:%M %A")

def onem2m_get_request(url, headers=None):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("GET request successful!")
        return response.json()  # Assuming the response is JSON data
    else:
        print(f"GET request failed with status code: {response.status_code}")
        return None
    

def text_to_speech(text, language='en', filename='output.mp3', play=True):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)
    if play:
        os.system("mpg321 output.mp3")
    os.remove(filename)    

KNOWN_DISTANCE = 60.0  # Assume the distance in centimeters (e.g., 60 cm)
KNOWN_FACE_WIDTH = 16.5  # Assume the average face width in centimeters (e.g., 16.5 cm)
FOCAL_LENGTH = 500.0  # Assume the focal length of the camera (e.g., 500 pixels)

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 1:
        (x, y, w, h) = faces[0]
        face_width_pixels = w
        distance = (KNOWN_FACE_WIDTH * FOCAL_LENGTH) / face_width_pixels
        print(int(distance))        # Display distance
        if(distance <40):
            try:
                response_data = onem2m_get_request(resource_url, headers)
                con_value =response_data['m2m:cin']['con'].split(',')
                print(formated_datetime)
                data = f"Welcone to Smart city living lab , time is {formated_datetime} current value of C O 2 is {str(con_value[1])} and temperature is {str(con_value[2])} and humidity is{str(con_value[3])}"
                text_to_speech(data) 
                print(data)     
            except:
                print("connecting.....")
        else:
            print("connection lost")
            
    else:
        print("face  not detect")

 
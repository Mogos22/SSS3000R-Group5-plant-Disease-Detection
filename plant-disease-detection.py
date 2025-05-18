import cv2 
import mysql.connector
from datetime import datetime
from picamera2 import Picamera2
from time import sleep
from tomato import tomato
from apple import apple
from send_email import Send_email
from gtts import gTTS
import os
from playsound import playsound  



#initialiser tomat and epleklasser
tomato_detector = tomato()
apple_detector = apple()

#mysql databasekonfigurasjon

db_config = {
    "host" : "localhost",
    "user" : "mogosmael",
    "password" : "sss3001",
    "database" : "plant_disease_detection"
}

#last haar cascade for gjenstandsdetekjon +
cascade = cv2.cascadeclassifier("haarcascade_frontalface_default.xml")

def detect_disease(image_path, plant_type):

    #oppdag sykdom basert på plantetypen
    if plant_type == "tomato":
        result = tomato_detector.detect_disease(image_path)
    elif plant_type == "apple":
        result = apple_detector.detect_disease(image_path)
    else:
        result = "ukjent plantetype"
    return result

def text_to_speech(text):
    #konverter tekst til tale og lagre permanent
    if not os.path.exists('sounds'):
        os.makedirs('sounds') 
    
    # opprettt inikt filnavn med tidsstempel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename =f"sounds/detection_{timestamp}.mp3"

    tts = gTTS(text=text, lang='en') 
    tts.save(filename)
    playsound.playsound(filename)
    

def save_to_database(plant_type, name, image_path,disease):
    #lagre bilde og metadata til riktig tabll i mysql databasen
    try:
        #koblle til database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        #les bildefile
        with open(image_path, "rb") as file:
            image_data = file.read()

            #sett inn data i den aktuell tabellen
        if plant_type == "tomato":
            query ="""
            insert into tomato(name, point_in_time, dato, detected_disease, image) 
            value(%s, %s, %s, %s, %s)
            """
        else:
            query ="""
            insert into apple(name, point_in_time, dato, detected_disease, image) 
            value(%s, %s, %s, %s, %s)
            """
        current_time = datetime.now()
        cursor.execute(query, (name, current_time, current_time.strftime("%Y-%m-%d"), disease, image_data))

        #forplikte transaksjonen
        connection.commit()
        print("data lagret i databasen vellykket!")
    except Exception as e:
        print(f"kunne ikke lagre data i databasen:{e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def capture_and_detect():
    #ta bilde fra picamera og oppdage sykedommer
    while True:
        #initiliserer picamera
        camera = Picamera2()
        camera.resolution(640, 480)

        print("åpne kamera... ")
        camera.start_preview()
        sleep(1)

        #ta bilde med kamera
        image_path = "temp_capture.jpg"
        camera.capture(image_path)
        print("bilde tatt.")

        #stopp og lukke kamera
        camera.stop_preview()
        camera.close()
        print("kamera lukket")

        #last inn det fangede bildet gjenkjenning av objekter
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2gray)
        plant_leaves = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors = 5)
        #sjekk om noen gjenstander ble oppdaget
        if len(plant_leaves) == 0:
            print("ingen planteblad påvist. vennligst prøv igjen.")
            
            #os.remove(image_path)
            continue

        #spør brukerne for plant_type
        plant_type = input("oppgi plant type (tomato/apple): ").lower()
        if plant_type  not in ["tomato", "apple"]:
            print("ugyldig plant type. vennligst, skriv 'tomato' eller 'apple' ")
            continue

        #forutsi sykdom
        disease = detect_disease(image_path, plant_type)
        disease_output = f"{plant_type}_{disease.replace('','_').lower()}"
        print(f"detected disease: {disease_output}")

        #lagre bilde i riktig mappe
        if plant_type == "tomato": 
            save_path = f"images/tomato/{len(os.listdir('images/tomato')) +1}.jpg"
        else:
            save_path = f"images/apple/{len(os.listdir('images/apple')) +1}.jpg"
        os.rename(image_path, save_path)

        #lagre bilde og metadata i det riktig tabell i mysql databasen

        save_to_database(plant_type, plant_type, save_path, disease)
        
        #spill tekst_til_tale_utgang 
        text_to_speech(f"detected disease: {disease}")
        #send epost med oppdaget sykdom og bilde
        Send_email(save_path, disease_output)


        #spør brukeren om vil fortsette
        choice = input("vil du ta et nytt bilde? (ja/nei): ").lower()
        if choice != "ja":
            break


if __name__ == "__main__":
    capture_and_detect()











        



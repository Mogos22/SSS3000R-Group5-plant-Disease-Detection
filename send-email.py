import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
#from email.mime.base import MIMEBase
#from email import encoders


def send_email(image_path, disease):
    #send et epost ved den oppdaget sykdommen og bildet
    #epost konfigration

    sender_email = ""            #eposten du konfigurerte til sende e-posten med apppassordet
    sender_password = ""         #Apppassordet du genererte  
    receiver_email = ""          #eposten til mottaker

    #skappe den eposten
    msg = MIMEMultipart()
    msg["from"] = sender_email
    msg["to"] = receiver_email
    msg["subject"] = f"Plantesykdom Oppdaget: {disease}"

    #Eposttekst
    body = f"Følgende Plantesykdom er påvist: {disease}"
    msg.attach(MIMEText(body, "plain"))

    #Legg ved bildet
    with open(image_path, "+rb") as image_file:
        image = MIMEImage(image_file.read(), name = os.path.basename(image_path)) 
        msg.attach(image)
    

    #send eposten

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) 
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string)() 
        print("E-post sendt sukssefully!")
    except Exception as e:
        print(f"Kunne ikke sende e-post{e}")
        #Lukke serveren
        server.close()
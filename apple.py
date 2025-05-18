import cv2
import numpy as np
import matplotlib. pyplot as plt 
import tensorflow as tf
import pyttsx3

#definerer tomat klass
class apple:
    def __init__(self, image_path, text_to_speech_func):
        self.image_path = image_path
        #last inn den ferdigtrente tensorflow-modellen
        self.model = tf.keras.models.load_model('/home/mogos/SSS3000R-Group5-plant-Disease-Detection/models/AppleModel.h5' , compile=False)

        #definere ekiketter for tomatskdom
        #input_img = preprocess_image(images_path) Two-spotted_spider_mite
        #if input_img is not None:
        self.class_labels = ["AppleBlackrot", "AppleHealthy", "Tomato_healthy",
                                "AppleScab","Cedarapplerust"] 
        # lagre tekst til tale-funksjonen
        self.text_to_speech = text_to_speech_func

    def preprocess_image(self, image_path, target_size=(256,256)):

        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("bilde finnes ikke i tomat mappa eller ute av stand til å lese")
            print(f"Original image shap: {image.shape}")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, target_size)
            print(f"Resize shape: {image.shape}")

            #normaliser pikselverdier
            image = image / 255.0
            #legg til batchdimentjon 
            image = np.expand_dims(image, axis=0)

            print(f"Normalized shape: {image.shape}")
            return image
        except Exception as e:
            print(f"feil under behandling av bildet:, {e}")
            return None
        
        
            
    def detect_disease(self): #predict_disease
        #forbehandlet bildet
        input_img = self.preprocess_image(self.image_path)
        if input_img is None:
            return "feil: bildebehandling mislykkes"
        
        detection = self.model.predict(input_img)
        result_index = np.argmax(detection)
        detected_class = self.class_labels[result_index]
        confidence = round(100 * np.max(detection[0]), 2)



         #vis bilde vis predikjon
        plt.imshow(input_img[0])
        plt.title("detected disease: " + detected_class + "\nConfidence: " + str(confidence) + "%")
        plt.xticks([])
        plt.yticks([])
        plt.show()
        

        #bruk tekst-til-tale-funksjon
        self.text_to_speech(f"detected disease: {detected_class.replace('_', ' ')}")
        return detected_class


#test bildebane
if __name__ == "__main__":
    engine = pyttsx3.init()
    text_to_speech_func = lambda x: (engine.say(x), engine.runAndWait())


    image_path = "/home/mogos/SSS3000R-Group5-plant-Disease-Detection/image/apple/AppleBlackrot/AppleBlackRot(1).JPG"

    #initialser tomato-klassen med bildbanen og tekst-til-tale funsjonen. 
    detector = apple(image_path, text_to_speech_func)

    #forutsi sykdommem 
    result = detector.detect_disease()
    print("Result:", result)
        









        
 



import cv2
import numpy as np
import tensorflow as tf
import keras
model_path = r"C:\olivy\disease_detection\Aimodels\,2"
file_path = r"C:\olivy\leaf_tests\670.jpg"

def process_image(image_path):
    img = cv2.imread(image_path)
    if img is not None:
        print('GOT THE IMAGE !!')
        predicted_class, confidence = prediction_model(img)
        print('predicted_class  ======> ', predicted_class)
        print('confidence       ======> ', confidence)
        return predicted_class, confidence
    else:
        print('Failed to load the image from the provided path.')
        return None, None

def prediction_model(input_image):
    # Resize the image if needed
    resized_image = cv2.resize(input_image, (256, 256))
    input_image = np.array(input_image)

    # Assuming the model_path variable is defined somewhere
    model = tf.keras.models.load_model(model_path)
    class_names = ['Aculos', 'Healthy', 'olive peacock']
    img_array = tf.keras.preprocessing.image.img_to_array(input_image)

    # Convert image to array and expand dimensions to match model input
    img_array = np.expand_dims(img_array, 0)
    
    # Make predictions
    predictions = model.predict(img_array)
    print ('prediction ...')

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * np.max(predictions[0]), 2)
    
    print('predicted_class:', predicted_class)
    print('confidence:', confidence)
    
    return predicted_class, confidence

# Test the code with the provided file path
print(process_image(file_path))

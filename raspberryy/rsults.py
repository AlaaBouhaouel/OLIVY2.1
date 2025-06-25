import cv2
import numpy as np
import tensorflow as tf

model_path = r"disease_detection\Aimodels\,2"  # Update with the path to your TensorFlow model file


def prediction_model(image):
    predicted_class = "Unknown"
    confidence = 0.0

    img = cv2.resize(image, (256, 256))

    input_image = np.array(img)
    if input_image is not None and input_image.all():
        model = tf.keras.models.load_model(model_path)

        class_names = ['Aculos', 'Healthy', 'olive peacock']

        img_array = tf.keras.preprocessing.image.img_to_array(input_image)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array)
        print('Prediction:')
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * (np.max(predictions[0])), 2)

        print(predicted_class)
        print('Confidence:', confidence)
    return predicted_class, confidence

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # Open the default camera (0)

    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        if not ret:
            break

        # Display the frame
        cv2.imshow('Webcam Feed', frame)

        # Perform prediction on the frame
        predicted_class, confidence = prediction_model(frame)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import keras
input_image= plt.imread(r'C:\olivy\leaf_tests\2.jpg')
model = keras.layers.TFSMLayer(r'C:\olivy\disease_detection\Aimodels\,2')
class_names=['Aculos','Healthy','olive peacock']


img_array = tf.keras.preprocessing.image.img_to_array(input_image)
img_array = tf.expand_dims(img_array, 0)

predictions = model.predict(img_array)

predicted_class = class_names[np.argmax(predictions[0])]
confidence = round(100 * (np.max(predictions[0])), 2)

print (predicted_class)
print ('confidence:',confidence)
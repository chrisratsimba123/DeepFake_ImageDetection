#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 11:17:46 2023

@author: ratsimbazafy
"""

import streamlit as st
from PIL import Image
import requests
import os
os.system('pip3 install pyngrok')
os.system('pip3 install tensorflow')

from pyngrok import ngrok
import tensorflow as tf
# from process import predict_img


execution_path = os.getcwd()
print(execution_path)

# prediction output
def predict_img(filename):
    # print('Filename is ' + filename)
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
    # target = filename  # location of image present in temp directory
    image_height = 256
    image_width = 256
    model_path = os.path.join(os.getcwd(), "/W210/Models/Baseline Model")
    print('model path' + model_path)

    loaded_model = tf.saved_model.load(export_dir=os.path.join(execution_path, "/W210/Models/Baseline Model"),
                                       tags=['serve'])
    class_names = ['fake', 'real']

    img = tf.keras.utils.load_img(
        filename, target_size=(image_height, image_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    predictions = loaded_model(img_array)
    score = tf.nn.softmax(predictions[0])
    d = [class_names[np.argmax(score)], round(100 * np.max(score), 2)]
    # os.remove(target)  # delete temporary file

    return d

# Function to resize the image
def resize_image(image, size):
    resized_image = image.resize(size)
    return resized_image

def main():
    st.title('Luminare')
    
    st.header("Unveil the Authentic You")
    st.markdown("At Luminare, we believe in the power of truth and authenticity. In a world filled with filters and "
                "digital enhancements, it's becoming increasingly challenging to distinguish between real and fake. "
                "That's where we come in.")
    
    st.header("Verify the Authenticity of Your Image")

    uploaded_file = st.file_uploader("Upload an image of a human face to check if it's real or AI-generated", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image

        response = predict_img(uploaded_file)
        
        if response is not none:
            st.success(f'Verification Complete: The image is {response[0]} with a {response[1]} % confidence')
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True, width=10)
        
        else:
            st.error('Failed to verify the image')

if __name__ == "__main__":
    main()

    

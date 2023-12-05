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
os.system('pip3 install -r requirements.txt')
import tensorflow as tf
import random
import matplotlib.pyplot as plt
import plotly.express as px

# prediction output
def predict_img(filename):
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
    image_height = 256
    image_width = 256
    # model_path = os.path.dirname("/Users/ratsimbazafy/Desktop/Data Science/MIDS/Fall23/W210/Models")
    # model_path = os.path.dirname("/Users/ratsimbazafy/Desktop/Data Science/MIDS/Fall23/W210/Models/Baseline/")
    model_path = os.getcwd()

    loaded_model = tf.saved_model.load(export_dir=os.path.join(model_path, "Models/"), tags=['serve'])
    # loaded_model = tf.keras.models.load_model(model_path+'/CNN/CNN_base.h5')
    class_names = ['fake', 'real']

    img = tf.keras.utils.load_img(filename, target_size=(image_height, image_width))
    
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

# Custom CSS
def load_css():
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        h1, h2, h3 {
            color: #32CD32; /* Slightly darker green */
        }
        /* Styling for the active tab */
        .st-bb .st-at, .st-bb .st-ae {
            border-color: #32CD32 !important;
        }
        .st-bb .st-at {
            background-color: #32CD32 !important;
            color: white !important;
        }
        /* Styling for the inactive tab */
        .st-bb .st-ae {
            background-color: transparent !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
def image_guessing_game():
    
    # Paths to the directories containing real and fake images
    real_images_dir = os.path.join(model_path, "Data/RealImages")
    fake_images_dir = os.path.join(model_path, "Data/FakeImages")

    # Check if directories exist
    if not os.path.exists(real_images_dir) or not os.path.exists(fake_images_dir):
        st.error("Image directories not found. Please check the paths.")
        return

    real_images = [img for img in os.listdir(real_images_dir) if os.path.isfile(os.path.join(real_images_dir, img))]
    fake_images = [img for img in os.listdir(fake_images_dir) if os.path.isfile(os.path.join(fake_images_dir, img))]

    # Ensure there are enough images
    if len(real_images) < 5 or len(fake_images) < 5:
        st.error("Insufficient images in directories")
        return

    selected_real_images = random.sample(real_images, 5)
    selected_fake_images = random.sample(fake_images, 5)

    all_images = selected_real_images + selected_fake_images
    random.shuffle(all_images)

    if 'current_image' not in st.session_state:
        st.session_state.current_image = 0
        st.session_state.score = 0
        st.session_state.correct_answers = {}
        for img in all_images:
            img_path = os.path.join(real_images_dir if img in selected_real_images else fake_images_dir, img)
            if os.path.exists(img_path):
                st.session_state.correct_answers[img] = 'Real' if img in selected_real_images else 'Fake'
            else:
                st.error(f"Missing image file: {img_path}")

    if st.session_state.current_image < len(all_images):
        image_name = all_images[st.session_state.current_image]
        image_path = os.path.join(real_images_dir if image_name in selected_real_images else fake_images_dir, image_name)

        if not os.path.exists(image_path):
            st.error(f"Image not found: {image_path}")
            return

        st.image(image_path, caption=f'Image {st.session_state.current_image + 1}')
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Real', key=f'real_{st.session_state.current_image}'):
                if st.session_state.correct_answers.get(image_name) == 'Real':
                    st.session_state.score += 1
                st.session_state.current_image += 1

        with col2:
            if st.button('AI-Generated', key=f'fake_{st.session_state.current_image}'):
                if st.session_state.correct_answers.get(image_name) == 'Fake':
                    st.session_state.score += 1
                st.session_state.current_image += 1

    else:
        st.write(f'Game Over! Your score: {st.session_state.score} out of {len(all_images)}')
        if st.button('Restart Game'):
            st.session_state.current_image = 0
            st.session_state.score = 0
            st.session_state.correct_answers.clear()
            random.shuffle(all_images)
            st.session_state.correct_answers = {img: 'Real' if img in selected_real_images else 'Fake' for img in all_images}

def main():
    load_css()
    st.title('Luminare')
    
    tab1, tab2 = st.tabs(['DeepFake Detection', 'Spot the Fake!'])
    
    with tab1:
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

            # For demonstration, let's assume the API response is a dummy dictionary
            # response = {'status': 'Success', 'result': 'Real'}
    
            # if response['status'] == 'Success':
                # result = response['result']
                # st.image(uploaded_file, caption='Uploaded Image', use_column_width=True, width=10)
                # st.success(f'Verification Complete: The image has a 82.3% likelihood of being {result}')
            # else:
                # st.error('Failed to verify the image')
                
    with tab2:
        st.header('Spot the Fake!')
        image_guessing_game()

if __name__ == "__main__":
    main()

    

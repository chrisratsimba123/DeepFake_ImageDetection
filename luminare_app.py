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
import numpy as np

# prediction output
def predict_img(filename):
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
    image_height, image_width = 256, 256
    model_path = os.path.join(os.getcwd(), "Models", "CNN_base.h5")

    # Check if the model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f'Model file not found at {model_path}')

    # Load the model
    loaded_model = tf.keras.models.load_model(model_path)
    # loaded_model = tf.saved_model.load(export_dir=os.path.join(os.getcwd(), "Models", "CNN_base.h5"), tags=['serve'])
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
    path = os.getcwd()
    real_images_dir = os.path.join(path, "Data/RealImages")
    fake_images_dir = os.path.join(path, "Data/FakeImages")

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

    def reset_game():
        st.session_state.current_image = 0
        st.session_state.score = 0
        random.shuffle(all_images)
        st.session_state.correct_answers = {img: 'Real' if img in selected_real_images else 'Fake' for img in all_images}

    if 'current_image' not in st.session_state:
        reset_game()
        # st.session_state.current_image = 0
        # st.session_state.score = 0
        # st.session_state.correct_answers = {img: 'Real' if img in selected_real_images else 'Fake' for img in
        #                                    all_images}

    # Center the header and images
    st.write("<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;}</style>", unsafe_allow_html=True)
    st.write("<style>div.stButton > button:first-child {margin: 0 auto;}</style>", unsafe_allow_html=True)

    def display_current_image():
        image_name = all_images[st.session_state.current_image]
        image_path = os.path.join(real_images_dir if image_name in selected_real_images else fake_images_dir, image_name)
        if not os.path.exists(image_path):
            st.error(f"Image not found: {image_path}")
            return
        st.image(image_path, caption=f'Image {st.session_state.current_image + 1}', use_column_width=True)

    def evaluate_choice(user_choice):
        correct_answer = st.session_state.correct_answers.get(all_images[st.session_state.current_image])
        if user_choice == correct_answer:
            st.success("Correct!")
            st.session_state.score += 1
        else:
            st.error(f"Incorrect! Image is {correct_answer}")
    
    if st.session_state.current_image < 10:  # Ensure only 10 images in total
        display_current_image()
        # image_name = all_images[st.session_state.current_image]
        # image_path = os.path.join(real_images_dir if image_name in selected_real_images else fake_images_dir, image_name)

        # if not os.path.exists(image_path):
            # st.error(f"Image not found: {image_path}")
            # return

        # st.image(image_path, caption=f'Image {st.session_state.current_image + 1}', use_column_width=True)

        # correct_answer = st.session_state.correct_answers.get(image_name)
        col1, col2 = st.columns([1, 1], gap='medium')
        # made_choice = False  # Flag to track if a choice was made
        
        with col1:
            if st.button('Real', key=f'real_{st.session_state.current_image}'):
                evaluate_choice('Real')
                # made_choice = True
                # if st.session_state.correct_answers.get(image_name) == 'Real':
                    # st.success("Correct!")
                    # st.session_state.score += 1
                # else:
                    # st.error("Incorrect! Image is Fake")

        # if col1.button('Real', key=f'real_{st.session_state.current_image}'):
            # if correct_answer == 'Real':
                # st.success("Correct!")
                # st.session_state.score += 1
            # else:
                # st.error("Incorrect! Image is Fake")
            # st.session_state.current_image += 1

        # if col2.button('Fake', key=f'fake_{st.session_state.current_image}'):
            # if correct_answer == 'Fake':
                # st.success("Correct!")
                 #st.session_state.score += 1
            # else:
                # st.error("Incorrect! Image is Fake")
            # st.session_state.current_image += 1

        with col2:
            if st.button('Fake', key=f'fake_{st.session_state.current_image}'):
                evaluate_choice('Fake')
                # made_choice = True
                # if st.session_state.correct_answers.get(image_name) == 'Fake':
                    # st.success("Correct!")
                    # st.session_state.score += 1
                # else:
                    # st.error("Incorrect! Image is Real")

        # Increment the current image index after a choice is made
        # if made_choice:
            # st.session_state.current_image += 1

    else:
        st.write(f'Game Over! Your score: {st.session_state.score} out of {len(all_images)}')
        if st.button('Restart Game'):
            reset_game()
            # st.session_state.current_image = 0
            # st.session_state.score = 0
            # st.session_state.correct_answers.clear()
            # random.shuffle(all_images)
            # st.session_state.correct_answers = {img: 'Real' if img in selected_real_images else 'Fake' for img in
            #                                     all_images}

def about_us():
    st.title("About Us - Deepfake Detection Service")

    st.write(
        "Welcome to our Deepfake Detection Service! We are a team of dedicated individuals "
        "committed to leveraging our expertise in Data Science to address the challenges posed "
        "by deepfake technology. Our team is comprised of three highly skilled graduate students "
        "from the renowned UC Berkeley, all graduating with master's degrees in Data Science."
    )
    st.header("Our Mission")

    st.write(
        "At our core, we are driven by the mission to combat the rise of deepfake technology. "
        "Our focus is on developing cutting-edge solutions that empower individuals and organizations "
        "to detect and mitigate the impact of manipulated media. We believe in the responsible use of technology "
        "and strive to create a safer digital environment for everyone."
    )

    st.header("Meet the Team")

    # Information about each team member
    team_members = [
        {"name": "Saket Suman", "role": "Co-Founder & Data Scientist", "image": "Team/saket.jpg"},
        {"name": "Chris Ratsimbazafy", "role": "Co-Founder & Machine Learning Engineer", "image": "Team/cards.jpeg"},
        {"name": "Cheick Sissoko", "role": "Co-Founder & Software Engineer", "image": "Team/cheick.jpeg"}
    ]

    for member in team_members:
        st.subheader(member["name"])
        st.image(member["image"], caption=f"{member['role']}")
        st.write(
            f"{member['name']} is our {member['role']} with a strong background in Data Science. "
            "They have demonstrated exceptional skills and dedication throughout their academic journey at UC Berkeley."
        )

    st.header("Contact Us")

    st.write(
        "If you have any questions or would like to learn more about our deepfake detection service, please feel free "
        "to reach out to us at [contact@example.com](mailto:contact@example.com). We appreciate your interest and look "
        "forward to collaborating with you in the fight against deepfake threats."
    )

def main():
    load_css()
    st.title('Luminare')

    tab1, tab2, tab3 = st.tabs(['DeepFake Detection', 'Spot the Fake!', 'About Us'])

    with tab1:
        st.header("Unveil the Authentic You")
        st.markdown(
            "At Luminare, we believe in the power of truth and authenticity. In a world filled with filters and "
            "digital enhancements, it's becoming increasingly challenging to distinguish between real and fake. "
            "That's where we come in.")

        st.header("Verify the Authenticity of Your Image")

        uploaded_file = st.file_uploader("Upload an image of a human face to check if it's real or AI-generated",
                                         type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Display the uploaded image

            response = predict_img(uploaded_file)

            if response is not None:
                st.success(f'Verification Complete: The image is {response[0]} with a {response[1]} % confidence')
                st.image(uploaded_file, caption='Uploaded Image', use_column_width=True, width=10)

            else:
                st.error('Failed to verify the image')

    with tab2:
        st.header('Spot the Fake!')
        image_guessing_game()

    with tab3:
        st.header('About Us')
        about_us()

if __name__ == "__main__":
    main()

    

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 11:17:46 2023

@author: ratsimbazafy
"""
import streamlit as st
import requests
import os

os.system('pip3 install pyngrok')

def main():
    st.title('Luminare - DeepFake Image Detection')

    uploaded_file = st.file_uploader("Upload an image of a human face to check if it's real or AI-generated", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Replace 'API_ENDPOINT' and 'API_KEY' with API details
        # response = requests.post('API_ENDPOINT', files={'image': uploaded_file}, headers={'Authorization': 'Bearer API_KEY'})

        # Sample API Response
        response = {'status': 'Success', 'result': 'Real'}

        if response['status'] == 'Success':
            result = response['result']
            st.success(f'Verification Complete: The image is {result}')
        else:
            st.error('Failed to verify the image')

if __name__ == "__main__":
    main()

# from pyngrok import ngrok

# Terminate open tunnels if exist
# ngrok.kill()

# Setup a new ngrok tunnel for the Streamlit app
# public_url = ngrok.connect(8501)
# print(f"Streamlit app is running at: {public_url}")
    

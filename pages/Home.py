import streamlit as st
import base64
from pathlib import Path
import sys
import os
import tempfile
import surabhi
import PIL.Image

import agents

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

file_path = ''
img = get_img_as_base64("Home.png")

custom_css = """
    <style>
        /* Add your custom font URL here */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap');

        /* Apply the font to the body or specific elements */
        body {
            font-family: 'Roboto', sans-serif;
            background-color: rgba(255, 255, 255, 0.6); /* Set the background color opacity here */
        }

        /* You can also apply the font to specific elements using their class or ID */
        .custom-text {
            font-family: 'Roboto', sans-serif;
            margin: auto;
        }

        /* Increase font size for all widgets */
        .css-1l02z2a {
            font-size: 20px; /* Adjust the font size as needed */
        }

        .css-1hb7zxy {
            font-size: 20px; /* Adjust the font size as needed */
        }

        .css-1pahdxg {
            font-size: 20px; /* Adjust the font size as needed */
        }

        .css-j08mfv {
            font-size: 20px; /* Adjust the font size as needed */
        }

        .css-dzdy9s {
            font-size: 20px; /* Adjust the font size as needed */
        }
    </style>
"""

page_bg_img = f'''
    <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{img}");
            background-repeat: no-repeat;
            background-size: 100%;
            background-color: rgba(255, 255, 255, 0.9);
        }}
         [data-testid="stSidebarContent"]{{
            background-image: linear-gradient(to right, #3533cd,black );
        }}
        [data-testid="stHeader"]{{
            background-color: rgba(0, 0, 0, 0);
        }}
          [data-testid="baseButton-secondary"]{{
            border-sizing:box-border;
            background-color: blue;
            margin-left: 250px;
            height:50px;
            width:250px;
            border-radius:50px;    
        }}
        p {{
            font-size:15px;
        }}
        #choose-platform{{
            margin-bottom:0px;
        }}
    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("## Select input method")
input_method = st.selectbox("", ["Text", "Photo", "Video"])

if input_method == "Text":
    text_input = st.text_area("Enter description for the post")

elif input_method == "Photo":
    image_input = st.file_uploader("Generate hashtags for this image")
    if image_input is not None:
    # Save the uploaded file to a temporary location
        file_path = os.path.join('upload', image_input.name)
        with open(file_path, "wb") as f:
            f.write(image_input.getvalue())
        

elif input_method == "Video":
        video_input = st.file_uploader("Generate hashtags for this image", type=['jpg', 'jpeg', 'png', 'webp'])
        if video_input is not None:
    # Save the uploaded file to a temporary location
            file_path = os.path.join('upload', video_input.name)
            with open(file_path, "wb") as f:
                f.write(video_input.getvalue())

st.markdown("### Choose Platform")

platform =st.radio("", ["Instagram", "Youtube", "Facebook"])

st.multiselect("Target Audience", ["Kids", "Teenagers", "Adults", "Senior Citizens"])

submit = st.button("Generate hashtags and captions")
final_text = ''
hashtags=''
if submit:
    if input_method == 'Text':
        final_text = text_input
        hashtags = agents.hashtag_agent.run(f"{final_text}")
        st.session_state['text'] = hashtags  
    elif input_method == 'Photo':
        conv_img = PIL.Image.open(file_path)
        final_text = surabhi.image_to_text(conv_img) 
        hashtags=agents.hashtag_agent.run(final_text)
        st.session_state['text'] = hashtags  
    elif input_method == 'Video':
         final_video = surabhi.video_to_text()
         hashtags=agents.hashtag_agent.run(final_video)
         hashtags=agents.hashtag_agent.run(final_video)
        #  st.write(hashtags)
    if 'text' not in st.session_state:
        st.session_state['text'] = ''
        st.session_state['text'] = ''
    st.session_state['text'] = st.text_area("Relevant hashtags are :", st.session_state['text'])
        
    st.session_state['text'] = st.text_area("Relevant caption is :", st.session_state['text'],key="23")
     
        
    
    
# if 'text' not in st.session_state:
#     st.session_state['text'] = ''

# # Create a text area and get the entered text
# st.session_state['text'] = st.text_area("Relevant hashtags are :", st.session_state['text'])




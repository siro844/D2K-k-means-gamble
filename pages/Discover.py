
import streamlit as st
import base64
from pathlib import Path
import sys
import os
import tempfile
import text_conversion
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

st.markdown("### Enter Theme")
st.text_input('')

st.markdown("### Enter Location")
loc =  st.text_input('',key="23")

st.markdown("### Choose Platform")

platform =st.radio("", ["Instagram", "Youtube", "Facebook"])

submit = st.button("Inspire me")
# final_text = ''
# hashtags=''

generated_script
if submit:
    if loc:
        script_generated = agents.Script_Agent.run(loc)
        




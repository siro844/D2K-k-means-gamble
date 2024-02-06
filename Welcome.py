import base64
import streamlit as st


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("Landing.png")

custom_css = """
    <style>
        /* Add your custom font URL here */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap');

        /* Apply the font to the body or specific elements */
        body {
            font-family: 'Roboto', sans-serif;
        }

        /* You can also apply the font to specific elements using their class or ID */
        .custom-text {
            font-family: 'Roboto', sans-serif;
            margin: auto;
        }
    </style>
"""

page_bg_img = f'''
    <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{img}");
            background-repeat: no-repeat;
            background-size: 100%;
        }}
         [data-testid="stHeader"]{{
            background-color: rgba(0, 0, 0, 0);
        }}
        [data-testid="stSidebarContent"]{{
            background-image: linear-gradient(to right, #3533cd,black );
        }}
        [data-testid="baseButton-secondary"]{{
            border-sizing:box-border;
            background-color: blue;
            margin-bottom:20%;
            margin-left: 0px;
            height:70px;
            width:450px;
            border-radius:50px;    
        }}
        //[data-testid="stSidebarContent"]{{visibility: hidden;}}
    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)
#st.button("Get Started")
#st.markdown('<style>[data-testid="stSidebarContent"]{{visibility: hidden;}}</style>', unsafe_allow_html=True)
st.markdown('<button style =" border-sizing:box-border;background-color: blue;margin-top:55%;margin-left: 0px;height:70px;width:450px;border-radius:50px;    "><a href="/Home" target="_self" style="font-size:25px;color:white;text-decoration:none;">Get Started</a></button>', unsafe_allow_html=True)
#st.markdown(custom_css, unsafe_allow_html=True)

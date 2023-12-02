import streamlit as st
from PIL import Image

st.write("""
# My first app
Hello *world!\\
InST Interface
""")

content_img = st.sidebar.file_uploader(label='Upload a content Image', type=['png', 'jpg'])

style_img = st.sidebar.file_uploader(label='Upload a style Image', type=['png', 'jpg'])

if content_img:
    img = Image.open(content_img)
    st.image(img, width=500)

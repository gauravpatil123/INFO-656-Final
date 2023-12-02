import streamlit as st
from PIL import Image

intro_str = """
# My first app 
Hello *world!*  
InST Interface
"""

st.write(intro_str)

content_img = st.sidebar.file_uploader(label='Upload a content Image', type=['png', 'jpg'])

# style_img = st.sidebar.file_uploader(label='Upload a style Image', type=['png', 'jpg'])

def load_img_from_path(path):
    img = Image.open(path)
    return img

sp1 = "./assets/style_images/modern.jpg"
sp2 = "./assets/style_images/andre-derain.jpg"
si1 = load_img_from_path(sp1)
si2 = load_img_from_path(sp2)

style_str = "## Choose a Style Image"
st.write(style_str)

col1, col2 = st.columns(2)

with col1:
    dsi1 = st.image(si1, width=300)
    st.write("### Modern")
    modern = st.checkbox("Modern")

with col2:
    dsi2 = st.image(si2, width=460)
    st.write("### Andre Derain")
    andre = st.checkbox("Andre Derain")

if modern:
    st.write("Modern Style Selected")

if andre:
    st.write("Andre Derian Style Selected")

style_choice = st.radio(
                "#### Choose a Style Image",
                ["Modern", "Andre Derain"],)

def style_embedding_path(style_choice):
    path = ""
    if style_choice == "Modern":
        path = ""
    elif style_choice == "Andre Derain":
        path = ""
    else:
        path = ""

if content_img:
    img = Image.open(content_img)
    st.image(img, width=500)

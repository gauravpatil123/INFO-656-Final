import streamlit as st
from PIL import Image

MODERN_EMBEDDING_PATH = "./embeddings/modern_embeddings.pt"
ANDRE_EMBEDDING_PATH = "./embeddings/andre-derain_embeddings.pt"
style_path_1 = "./assets/style_images/modern.jpg"
style_path_2 = "./assets/style_images/andre-derain.jpg"

intro_str = """
# My InST Feedback App 
"""

def load_img_from_path(path):
    img = Image.open(path)
    return img

def style_prompt(style):
    out = f"###### {style} style selected"
    st.write(out)
    return out

def style_embedding_path(style_choice):
    path = ""
    if style_choice == "Modern":
        path = MODERN_EMBEDDING_PATH
    elif style_choice == "Andre Derain":
        path = ANDRE_EMBEDDING_PATH
    else:
        path = MODERN_EMBEDDING_PATH
    return path

if __name__=="__main__":
    
    st.write(intro_str)

    content_img = st.sidebar.file_uploader(label='Upload a content Image', type=['png', 'jpg'])
    #style_img = st.sidebar.file_uploader(label='Upload a style Image', type=['png', 'jpg'])

    style_image_1 = load_img_from_path(style_path_1)
    style_image_2 = load_img_from_path(style_path_2)

    style_str = "## Choose a Style Image"
    st.write(style_str)

    col1, col2 = st.columns(2)

    with col1:
        dsi1 = st.image(style_image_1, width=300)
        st.write("### Modern")

    with col2:
        dsi2 = st.image(style_image_2, width=460)
        st.write("### Andre Derain")

    style_choice = st.radio(
                "#### Choose a Style Image",
                ["Modern", "Andre Derain"],)
    
    style_selected = style_prompt(style_choice)

    embedding_path = style_embedding_path(style_choice)

    if content_img:
        img = Image.open(content_img)
        st.image(img, width=500)


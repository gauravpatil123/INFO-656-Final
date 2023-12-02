import streamlit as st
from PIL import Image
import os
# from InSt import generate_images as gen

MODERN_EMBEDDING_PATH = "./embeddings/modern_embeddings.pt"
ANDRE_EMBEDDING_PATH = "./embeddings/andre-derain_embeddings.pt"
style_modern = "./assets/style_images/modern.jpg"
style_andre = "./assets/style_images/andre-derain.jpg"
CONTENT_IMG_DIR = "./assets/content_images/"
current_content_img_path = ""

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

def style_image_path(style_choice):
    path = ""
    if style_choice == "Modern":
        path = style_modern
    elif style_choice == "Andre Derain":
        path = style_andre
    else:
        path = style_modern
    return path

def save_uploaded_image(dir, uploaded_image):
    global current_content_img_path
    img = Image.open(uploaded_image)
    st.image(img, width=500)
    file_name = uploaded_image.name
    file_type = uploaded_image.type
    # st.write(file_name)
    # st.write(file_type)
    with open(os.path.join(dir, uploaded_image.name), "wb") as f:
        current_content_img_path = os.path.join(dir, uploaded_image.name)
        # st.write(current_content_img_path)
        f.write(uploaded_image.getbuffer())
    return st.success(f"File Uploaded to ./assets/content_images/")

if __name__=="__main__":
    intro_str = """
    # My InST Feedback App 
    """

    st.write(intro_str)

    style_image_1 = load_img_from_path(style_modern)
    style_image_2 = load_img_from_path(style_andre)

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
    style_image_p = style_image_path(style_choice)

    content_img = st.file_uploader(label='#### Upload a content Image', type=['png', 'jpg'])

    if content_img:
        save_uploaded_image(CONTENT_IMG_DIR, content_img)
        content_image_p = current_content_img_path





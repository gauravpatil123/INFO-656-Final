import streamlit as st
from PIL import Image
import os
from InSt import model
from InSt import generate_images as gen

MODERN_EMBEDDING_PATH = "./embeddings/modern_embeddings.pt"
ANDRE_EMBEDDING_PATH = "./embeddings/andre-derain_embeddings.pt"
style_modern = "./assets/style_images/modern.jpg"
style_andre = "./assets/style_images/andre-derain.jpg"
CONTENT_IMG_DIR = "./assets/content_images/"
current_content_img_path = None
CONTENT_IMG_BOOL = False
output = None
GENERATED_IMG_DIR = "./assets/generated_images/"
save = None
current_output_image_dir = ""

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
    global current_content_img_path, CONTENT_IMG_BOOL
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
        CONTENT_IMG_BOOL = True
    return st.success(f"File Uploaded to ./assets/content_images/")

def convert_image(model, embeddings, content_img_path, style_image_path):
    global CONTENT_IMG_BOOL, current_content_img_path
    if CONTENT_IMG_BOOL and current_content_img_path:
        out = gen(model, embeddings, content_img_path, style_image_path)
        pass
    else:
        st.write(f"No content Image Uploaded, try to upload a content image.")
        out = None
    return out

def run_convert(convert, model, embeddings, content_img_path, style_image_path, style_name, gen_name):
    global output, GENERATED_IMG_DIR
    if convert:
        out = convert_image(model, embeddings, content_img_path, style_image_path)
        name = f"{style_name}_{gen_name}.jpg"
        out.save(os.path.join(GENERATED_IMG_DIR, name))
        output = out

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
    content_image_p = current_content_img_path

    if content_img:
        save_uploaded_image(CONTENT_IMG_DIR, content_img)
        content_image_p = current_content_img_path
        
    gen_name = st.text_input('Please name the generated image')
    convert = st.button("Generate Image")

    run_convert(convert, model, embedding_path, content_image_p, style_image_p, style_choice, gen_name)

    current_output_image_dir = GENERATED_IMG_DIR + f"{style_choice}_{gen_name}.jpg"

    if output is not None:
        st.image(output, width=500)
        image_download = Image.open(output)
        with open(current_output_image_dir, "rb") as f:
            download = st.download_button(label="Download Image", data=f, file_name="download.jpg", mime="image/jpeg")






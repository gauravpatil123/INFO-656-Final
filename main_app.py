import streamlit as st
from PIL import Image
import os
from InSt import model
from InSt import generate_images as gen

MODERN_EMBEDDING_PATH = "./embeddings/modern_embeddings.pt"
ANDRE_EMBEDDING_PATH = "./embeddings/andre-derain_embeddings.pt"
LONGHAIR_EMBEDDING_PATH = "./embeddings/longhair_embeddings.pt"
WOMEN_EMBEDDING_PATH = "./embeddings/woman_embeddings.pt"
style_modern = "./assets/style_images/modern.jpg"
style_andre = "./assets/style_images/andre-derain.jpg"
style_longhair = "./assets/style_images/longhair.jpg"
style_women = "./assets/style_images/woman.png"
CONTENT_IMG_DIR = "./assets/content_images/"
current_content_img_path = None
CONTENT_IMG_BOOL = False
GENERATED_IMG_DIR = "./assets/generated_images/"
save = None
current_output_image_dir = None
feedback = None
MODEL_TYPE = "cpu"
FEEDBACK_LOG = "./assets/logs/feedback/feedback_log.txt"

def load_img_from_path(path:str):
    img = Image.open(path)
    return img

def style_prompt(style:str) -> str:
    out = f"###### {style} style selected"
    st.write(out)
    return out

def style_embedding_path(style_choice:str) -> str:
    path = ""
    if style_choice == "Modern":
        path = MODERN_EMBEDDING_PATH
    elif style_choice == "Andre Derain":
        path = ANDRE_EMBEDDING_PATH
    elif style_choice == "Long Hair":
        path = LONGHAIR_EMBEDDING_PATH
    elif style_choice == "Women":
        path = WOMEN_EMBEDDING_PATH
    else:
        path = MODERN_EMBEDDING_PATH
    return path

def style_image_path(style_choice:str) -> str:
    path = ""
    if style_choice == "Modern":
        path = style_modern
    elif style_choice == "Andre Derain":
        path = style_andre
    elif style_choice == "Long Hair":
        path = style_longhair
    elif style_choice == "Women":
        path = style_women
    else:
        path = style_modern
    return path

def save_uploaded_image(dir:str, uploaded_image):
    global current_content_img_path, CONTENT_IMG_BOOL
    img = Image.open(uploaded_image)
    st.image(img, width=500)
    # file_name = uploaded_image.name
    # file_type = uploaded_image.type
    # st.write(file_name)
    # st.write(file_type)
    with open(os.path.join(dir, uploaded_image.name), "wb") as f:
        f.write(uploaded_image.getbuffer())
        current_content_img_path = os.path.join(dir, uploaded_image.name)
        # st.write(current_content_img_path)
        CONTENT_IMG_BOOL = True
    return st.success(f"File Uploaded to ./assets/content_images/")

def convert_image(model, embeddings, content_img_path, style_image_path):
    global CONTENT_IMG_BOOL, current_content_img_path
    if CONTENT_IMG_BOOL and current_content_img_path:
        with st.status("Converting image..."):
            st.write("Image conversion in progress...")
            out = gen(model, embeddings, content_img_path, style_image_path)
            st.write("Image conversion complete!")
    else:
        st.write(f"No content image uploaded, try to upload a content image.")
        out = None
    return out

def run_convert(convert, model, embeddings, content_img_path, style_image_path, style_name, gen_name):
    global GENERATED_IMG_DIR
    if convert:
        out = convert_image(model, embeddings, content_img_path, style_image_path)
        name = f"{style_name}_{gen_name}.jpg"
        path = os.path.join(GENERATED_IMG_DIR, name)
        out.save(path)
        return path

def generate_feedback(feedback_list):
    global feedback
    p, n = feedback_list
    if p:
        feedback = "positive"
    elif n:
        feedback = "negative"

def record_feedback(embedding, style_img, content_img, feedback, model_type=MODEL_TYPE, feedback_file=FEEDBACK_LOG):
    global current_output_image_dir

    feedback_str = "{\nEmbedding: " + f"{embedding}" + ",\n"
    feedback_str += "Style Image: " + f"{style_img}" + ",\n"
    feedback_str += "Content Image: " + f"{content_img}" + ",\n"
    feedback_str += "Feedback: " + f"{feedback}" + ",\n"
    feedback_str += "Model Type: " + f"{model_type}" + "\n}\n"

    with open(feedback_file, "a") as fb_log:
        fb_log.write(feedback_str)

if __name__=="__main__":

    intro_str = """
    # My InST Feedback App 
    """

    st.write(intro_str)

    style_image_1 = load_img_from_path(style_modern)
    style_image_2 = load_img_from_path(style_andre)
    style_image_3 = load_img_from_path(style_longhair)
    style_image_4 = load_img_from_path(style_women)

    style_str = "## Choose a Style Image"
    st.write(style_str)

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Modern")
        dsi1 = st.image(style_image_1, width=300)

    with col2:
        st.write("### Andre Derain")
        dsi2 = st.image(style_image_2, width=460)

    col3, col4 = st.columns(2)

    with col3:
        st.write("### Long Hair")
        dsi3 = st.image(style_image_3, width=300)

    with col4:
        st.write("### Women")
        dsi4 = st.image(style_image_4, width=350)

    style_choice = st.radio(
                "#### Choose a Style Image",
                ["Modern", "Andre Derain", "Long Hair", "Women"],)
    
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

    output_path = run_convert(convert, model, embedding_path, content_image_p, style_image_p, style_choice, gen_name)

    current_output_image_dir = output_path

    if current_output_image_dir is not None:

        current_output_image = load_img_from_path(current_output_image_dir)

        st.image(current_output_image, width=500)

        # with open(current_output_image_dir, "rb") as f:
        #     download = st.download_button(label="Download Image", data=f, file_name="download.jpg", mime="image/jpeg")

    st.write("##### Is the converted image acceptable?")

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        positive = st.button("Acceptable 👍")
    
    with col6:
        negative = st.button("Unacceptable 👎")

    feedback_list = [positive, negative]

    generate_feedback(feedback_list)

    if feedback is not None:
        record_feedback(embedding_path, style_image_p, content_image_p, feedback)
            







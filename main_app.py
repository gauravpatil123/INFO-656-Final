import streamlit as st
from PIL import Image
import os
from InSt import model
from InSt import generate_images as gen
from time import gmtime, strftime

# Global Variables
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
GEN_SEED = 42

# Utility Functions
def load_img_from_path(path:str):
    """
    Function to load images from path
    """
    img = Image.open(path)
    return img

def style_prompt(style:str) -> str:
    """
    Input:
        style: selected style as a string
    Action & Output:
        Writes the markdown str in st app &
        Return markdown str of selected style
    """
    out = f"###### {style} style selected"
    st.write(out)
    return out

def style_embedding_path(style_choice:str) -> str:
    """
    Input:
        style_choice: selected style from the app
    Output:
        Returns the embedding path of the selected style
    """
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
    """
    Input:
        style_choice: selected style from the app
    Output:
        Returns the image path of the selected style image
    """
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
    """
    Input:
        dir: directory path for content images
        uploaded_image: content image uploaded from st file uploader
    Output & Action:
        saves the uploaded images to dir
        sets global current_content_img_path to current uploaded image path
        sets global content_img_bool to true
        writes successfull file upload message the streamlit app
    """
    global current_content_img_path, CONTENT_IMG_BOOL
    img = Image.open(uploaded_image)
    st.image(img, width=500)

    with open(os.path.join(dir, uploaded_image.name), "wb") as f:
        f.write(uploaded_image.getbuffer())
        current_content_img_path = os.path.join(dir, uploaded_image.name)
        CONTENT_IMG_BOOL = True
    return st.success(f"File Uploaded to ./assets/content_images/")

def convert_image(model, embeddings:str, content_img_path:str, style_image_path:str):
    """
    Input:
        model: imported model from InSt
        embeddings: path for selected embeddings
        content_img_path: path for uploaded content image
        style_image_path: path for selected style image
    Output:
        out: output image after converting content image using the imported model
                or None if no content image is uploaded
    """
    global CONTENT_IMG_BOOL, current_content_img_path, GEN_SEED
    if CONTENT_IMG_BOOL and current_content_img_path:
        with st.status("Converting image..."):
            st.write("Image conversion in progress...")
            out = gen(model, embeddings, content_img_path, style_image_path, GEN_SEED)
            st.write("Image conversion complete!")
    else:
        st.write(f"No content image uploaded, try to upload a content image.")
        out = None
    return out

def run_convert(convert:bool, model, embeddings:str, content_img_path:str, style_image_path:str, style_name:str, gen_name:str) -> str:
    """
    Input:
        convert: Bool to check if generate button is clicked on the main app
        model: imported model from InSt
        embeddings: path for selected embeddings
        content_img_path: path for uploaded content image
        style_image_path: path for selected style image
        style_name: name of the selected style
        gen_name: inout name for the generated image from st input
    Output & Action:
        runs convert_image function and saves the output image using the styel and gen name from input
        saves the output image in the global generated image directory
        returns the path of output image directory
    """
    global GENERATED_IMG_DIR
    if convert:
        out = convert_image(model, embeddings, content_img_path, style_image_path)
        name = f"{style_name}_{gen_name}.jpg"
        path = os.path.join(GENERATED_IMG_DIR, name)
        out.save(path)
        return path

def generate_feedback(feedback_list:list):
    """
    Input:
        feedback_list: list containing bool list of [positive, negative] feedback
    Action:
        unpacks the feedback_list 
        sets the global feedback to positive or negative depending on input list
    """
    global feedback
    p, n = feedback_list
    if p:
        feedback = "positive"
    elif n:
        feedback = "negative"

def record_feedback(embedding:str, style_img:str, content_img:str, feedback:str, model_type:str=MODEL_TYPE, feedback_file:str=FEEDBACK_LOG):
    """
    Input:
        embedding: selected embedding path
        style_img: selected style image path
        content_img: uploaded content image path
        feedback: global feedback set from users imput
        model_type: global model type used for conversion
        feedback_file: path to feedback log file
    Action:
        gets current time using time library
        generates feedback_str
        logs the feedback_str in the feedback_log file
    """
    curr_time_gmt = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    feedback_str = "{\nEmbedding: " + f"{embedding}" + ",\n"
    feedback_str += "Style Image: " + f"{style_img}" + ",\n"
    feedback_str += "Content Image: " + f"{content_img}" + ",\n"
    feedback_str += "Feedback Record Time (GMT): " + f"{curr_time_gmt}" + ",\n"
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

        # Download Button (will have to set states to make it work)
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
            







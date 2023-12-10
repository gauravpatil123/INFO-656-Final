# INFO-656-Final
A Feedback Logger App of InST Project.

**App Contents**
- About
- Requirements
- Scripts & Executables
- assets

**About**</br>
This app is built over InST, as a feedback logger app for outputs from InST models.

**Requirements**</br>
The requirements for dependencies & libraries for this app are mentioned in "requirements.txt"<br>
Please create an environment with these mentioned requirements before running the app.

**Scripts**</br>
- "InSt.py"<br>
This script initialised and creates an instance of the model which is used to convert images.<br>
This script also defines the "generate_images" function to be used for converting images.

- "main_app.py"<br>
This script creates a local stremlit app to be used to upload a contnent image and then convert it to the selected style.<br>
Further this app aloows the user to give a positive or negative feedback for the output result.<b>
To run this app use: ```streamlit run main_app.py```

**assets**</br>
- content_images</br>
Contains all the uploaded content images by the user.

- generated_images</br>
Contains all the generated outputs after converting the uploaded images.

- style_images</br>
Contains all the style images on which are used by the model.

- logs</br>
Contains the feedback_log txt file with all the feedbacks along with other metadata.
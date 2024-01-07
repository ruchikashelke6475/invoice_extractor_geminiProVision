from dotenv import load_dotenv
import pathlib
import textwrap
import google.generativeai as genai
#from google.colab import userdata

from IPython.display import display
from IPython.display import Markdown
from PIL import Image
import os
import streamlit as st

os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']

genai.configure(api_key=os.environ['GOOGLE_API_KEY'] )

model = genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input,image,prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Intialize streamlit app 
st.set_page_config(page_title = " Multi Language Invoice Extractor")

input = st.text_input("Input Prompt : ", key = "input")
uploaded_file = st.file_uploader("Choose an image for invoice",type = ["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None: 
    image = Image.open(uploaded_file)
    st.image(image, caption= "Uploaded image.", use_column_width = True)


submit = st.button("Ask Gemini")


input_prompt = """

yu are an expert in understanding invoices. We will upload an image as invoices and you will have to anwer any images based on the invoices.
"""

if submit: 
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("Response is:")
    st.write(response)

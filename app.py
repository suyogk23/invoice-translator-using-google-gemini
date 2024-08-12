from dotenv import load_dotenv #load env elements
import streamlit as st  # easy app creation-like web apps
import os   #pick assigned env vars
from PIL import Image
import google.generativeai as genai 


load_dotenv() #load all environment vars from .env

#configure api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load GeminiProVision
model=genai.GenerativeModel("gemini-pro-vision")

# function to get gemini api response
def get_gemini_response(input,image,prompt):    #input=specifies what the model should do by the user, prompt=the use case behaviour of the gemini-model; 
    response=model.generate_content([input,image[0],prompt])
    return response.text

#processing the image
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type": uploaded_file.type, #Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not uploaded")

#init STEAMLIT APP
st.set_page_config(page_title="MULTI-LANGUAGE INVOICE EXTRACTOR")   
input=st.text_input("Input Prompt: ",key="input") #The key parameter is used to uniquely identify this input widget in Streamlit
uploaded_file=st.file_uploader("Choose invoice image to upload....",type=["jpg","jpeg","png"]) #file uploader for image
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image", use_column_width=True) #display uploaded image


submit =st.button("Get Invoice Details")

input_prompt="""
You are an expert in understanding invoices. We will upload an image as an invoice and
you will have to answer any questions based on the uploaded invoice image
"""


#if submit button is clicked:
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is:")
    st.write(response)
 








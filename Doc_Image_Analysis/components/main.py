import os,sys
from Doc_Image_Analysis.logger import logging
from Doc_Image_Analysis.exception import ImageAnalysisException
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import google.ai.generativelanguage as glm
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


logging.info(f" Load the Gemini Pro Vision model ")
model = genai.GenerativeModel("gemini-pro-vision")

def get_image(file):
    try:
        logging.info(f"Open Image File")
        image = Image.open(file)
        return image
    except Exception as e:
        raise ImageAnalysisException(e,sys)



def get_response(image,input):
    try:
        logging.info(f"extract the information from given document")
        response = model.generate_content([image,input])
        result = response.text
        return {f"{input}":result,}
    except Exception as e:
        raise ImageAnalysisException(e,sys)
    





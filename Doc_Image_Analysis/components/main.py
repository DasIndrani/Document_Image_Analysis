import os,sys
from Doc_Image_Analysis.logger import logging
from Doc_Image_Analysis.exception import ImageAnalysisException
import google.generativeai as genai
#from dotenv import load_dotenv
from PIL import Image
import google.ai.generativelanguage as glm
#load_dotenv()

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))


logging.info(f"Load the Gemini Pro Vision model ")
model = genai.GenerativeModel("gemini-pro-vision")

class MainFunction:
    def __init__(self):
        try:
            self.file_path = None
            self.image = None
            self.input = None
        except Exception as e:
            raise ImageAnalysisException
        
    def get_image(self,file_path):
        try:
            logging.info(f"open Image File")
            self.image = Image.open(file_path)
            return self.image
        except Exception as e:
            raise ImageAnalysisException(e,sys)



    def get_response(self,image,input):
        try:
            logging.info(f"extract the information from given document")
            self.response = model.generate_content([image,input])
            self.result = self.response.text
            return {f"{input}":self.result}
        except Exception as e:
            raise ImageAnalysisException(e,sys)
    





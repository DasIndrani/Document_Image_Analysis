import os,sys
import streamlit as st
from Doc_Image_Analysis.logger import logging
from Doc_Image_Analysis.exception import ImageAnalysisException
from Doc_Image_Analysis.components.main import MainFunction
from Doc_Image_Analysis.utils import save_responses,logged_in,sign_up,page_1, output_folder,upload_to_s3


class App:
    def __init__(self,main_function:MainFunction):
        try:
            self.main_function= main_function
        except Exception as e:
            raise ImageAnalysisException(e,sys) 
    def main_app(self):
        try:
            logging.info(f" Configure the App Page ")
            st.subheader(":key: Extract key information from Document")


            if 'input_list' not in st.session_state:
                st.session_state.input_list = []

            logging.info(f"Create Simple Text input  and image input Box for the app")
            input_text= st.text_area("write Input Text :pencil2::", key="input", height= 20)
            if st.button("Add to List :memo:"):
                st.session_state.input_list.append(input_text)


            st.sidebar.title("Upload image file of Document")
            uploaded_file = st.sidebar.file_uploader(label= ":file_folder: choose a file...",type=["jpeg","png","jpg"])


            if uploaded_file is not None:
                image = self.main_function.get_image(file_path = uploaded_file)
                logging.info(f"load and display the image")
                st.image(image, caption='Image', use_column_width=True)

            logging.info(f"Create the sumbit button" )
            sumbit_button = st.button(label="Click here to see about the Document :point_left:")


            if 'responses' not in st.session_state:
                st.session_state.responses = []

            if 'executed' not in st.session_state:
                st.session_state.executed =[]

            if sumbit_button:
                new_inputs = [input for input in st.session_state.input_list if input not in st.session_state.executed]
                for input in new_inputs:
                    response = self.main_function.get_response(image=image, input=input)
                    st.session_state.executed.append(input)
                    st.session_state.responses.append(response)
                    st.write(response)
                st.subheader("key Information: ")
                st.write(st.session_state.responses)


            reset = st.button("Reset :arrows_counterclockwise:")

            if st.session_state.responses:
                save_responses(response=st.session_state.responses, reset=reset)
                output_folder = output_folder()
                upload_to_s3(local_folder_path=output_folder,bucket_name=os.getenv("BUCKET_NAME"),s3_folder_prefix="Outbox")

                st.success(f"Information saved to  s3 outbox folder")

            logging.info(f" After Extract all information from a doc reset all list as empty list ")
            if reset:
                st.session_state.input_list = []
                st.session_state.responses = []
                st.session_state.executed =[]

        except Exception as e:
            raise ImageAnalysisException(e,sys)

    def initiate_app(self):
        try:
            page_1()
            st.header(" :ice_cube: Welcome To DIA (Document Image Analysis)",divider='rainbow')
            page_options = ['Login', 'Sign Up']
            selected_page = st.sidebar.selectbox('Login/Signup :point_down:',placeholder="choose an option",index=None, options=page_options)

            if selected_page == 'Login':
                if 'logged_in'  not in st.session_state or not st.session_state.logged_in:
                    logged_in()
                
                elif 'logged_in' in st.session_state and st.session_state.logged_in:
                    self.main_app()

            if selected_page == "Sign Up":
                if 'sign_up' not in st.session_state or not st.session_state.sign_up:
                    sign_up()
                elif 'sign_up' in st.session_state and st.session_state.sign_up:
                    if 'logged_in'  not in st.session_state or not st.session_state.logged_in:
                        logged_in()
                    elif 'logged_in' in st.session_state and st.session_state.logged_in:
                        self.main_app()
        except Exception as e:
            raise ImageAnalysisException(e,sys)
        
    def start(self):
        app = self.initiate_app()
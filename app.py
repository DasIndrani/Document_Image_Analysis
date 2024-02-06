import streamlit as st
from Doc_Image_Analysis.logger import logging
from Doc_Image_Analysis.components.main import get_image, get_response
from Doc_Image_Analysis.utils import save_object


logging.info(f" Configure the App Page ")
st.set_page_config(page_title= "Document Image Analysis App",layout="centered",page_icon=":droplet:")
st.header(":key: Extract key information from Document")


if 'input_list' not in st.session_state:
    st.session_state.input_list = []

logging.info(f"Create Simple Text input  and image input Box for the app")
input_text= st.text_area("write Input Text :pencil2::", key="input", height= 20)
if st.button("Add to List :memo:"):
    st.session_state.input_list.append(input_text)


st.sidebar.title("Upload Image file of Document")
uploaded_file = st.sidebar.file_uploader(label= ":file_folder: choose a file...",type=["jpeg","png","jpg"])


if uploaded_file is not None:
    image = get_image(uploaded_file)
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
        response = get_response(image=image, input=input)
        st.session_state.executed.append(input)
        st.session_state.responses.append(response)
        st.write(response)
    st.subheader("key Information: ")
    st.write(st.session_state.responses)


reset = st.button("Reset :arrows_counterclockwise:")

if st.session_state.responses:
    save_object(response=st.session_state.responses, reset=reset)
        
    st.success(f"Information saved to output folder")

logging.info(f" After Extract all information from a doc reset all list as empty list ")
if reset:
    st.session_state.input_list = []
    st.session_state.responses = []
    st.session_state.executed =[]
    



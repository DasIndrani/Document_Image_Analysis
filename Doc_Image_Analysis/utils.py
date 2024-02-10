import os,sys
import json, dump
import streamlit as st
from Doc_Image_Analysis.exception import ImageAnalysisException


Output_folder = "Output"
os.makedirs(Output_folder, exist_ok=True)

Users_information = "Users_Information"
os.makedirs(Users_information,exist_ok=True)
Users ={}



def save_object(response,reset):
    try:
        filepath = os.listdir(Output_folder)
        i=len(filepath)
        if not reset:
            json_file_path = os.path.join(Output_folder,"responses.json")
            with open(json_file_path, "w") as json_file:
                json.dump(response, json_file,indent=1)
        else:
            json_file_path = os.path.join(Output_folder,f"responses_{i+1}.json")
            with open(json_file_path, "w") as json_file:
                json.dump(response, json_file,indent=1)

    except Exception as e:
        raise ImageAnalysisException(e,sys) 
    
def save_info(Users):
    try:
       with open(os.path.join(Users_information,"info.json"), "w") as json_file:
           json.dump(Users, json_file,indent=1)
    except Exception as e:
        raise ImageAnalysisException(e,sys) 
    
def load_info():
    try:
        with open(os.path.join(Users_information,"info.json"),"r") as json_file:
            return json.load(json_file)
    except Exception as e:
        raise ImageAnalysisException(e,sys)


def sign_up():
    try:
        st.header("Sign Up")
        new_username = st.text_input("New_Username",placeholder="enter new username")
        new_password = st.text_input("New_Password",type="password",placeholder="enter new password")

        if st.button(label="Enter New Username & Password"):
            if new_username in Users:
                st.error("Try Another :warning:")
                return False
            else:
                Users[new_username] = new_password
                st.session_state.sign_up = True
                st.success("Sign Up Successfully")
                save_info(Users)
                if True:
                    return st.button("Go to login..")
                
    except Exception as e:
        raise ImageAnalysisException(e,sys)

def logged_in():
    try:
        st.header("Login :closed_lock_with_key:")
        username = st.text_input("Username",placeholder="enter username")
        password = st.text_input("Password",type='password',placeholder="enter password",max_chars=16)

        if st.button("Enter Username and Password"):
            User_info = load_info()
            if username in User_info and User_info[username] == password:
                st.success(f"Welocme {username}")
                st.session_state.logged_in = True
                if True:
                    return st.button("login :unlock:")

            else:
                st.error("Invalid Username or Password! Re-enter :warning:")
                return False
            
    except Exception as e:
        raise ImageAnalysisException(e,sys)
    
def page_1():
    page_1 = st.set_page_config(page_title= "DIA System",layout="centered",page_icon=":ice-cube:")
    return page_1





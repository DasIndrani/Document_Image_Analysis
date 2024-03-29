import os,sys,glob
import json, dump
import streamlit as st
import boto3
from Doc_Image_Analysis.exception import ImageAnalysisException
from Doc_Image_Analysis.logger import logging




Users_information = "Users_Information"
os.makedirs(Users_information,exist_ok=True)
Users ={}

def output_folder():
    try:
        Output_dir = "Output"
        os.makedirs(Output_dir, exist_ok=True)
        return Output_dir
    except Exception as e:
        raise ImageAnalysisException(e,sys)

def save_responses(response,reset):
    try:
        Output_dir= output_folder() 
        filepath = os.listdir(Output_dir)
        i=len(filepath)
        files = glob.glob(os.path.join(Output_dir, "responses_*"))
        file_numbers = [int(os.path.splitext(os.path.basename(filename))[0].split("_")[1]) for filename in files]
        if st.session_state.logged_in and reset:
            if files:
                last_file_number = max(file_numbers)
            json_file_path = os.path.join(Output_dir, f"responses_{last_file_number}.json")
            with open(json_file_path, "w") as json_file:
                json.dump(response, json_file,indent=1)

        if not reset:
            json_file_path = os.path.join(Output_dir,f"responses_{i+1}.json")
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
        new_password = st.text_input("New_Password",type="password",placeholder="enter new password",max_chars=16)

        if st.button(label="Enter New Username & Password"):
            if os.path.exists(os.path.join(Users_information,"info.json")):
                User_info = load_info()
                if new_username in User_info:
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
 
def logged_out():
    st.header("Log out")
    log_out = st.button("log out")
    if log_out:
        st.session_state.input_list = []
        st.session_state.responses = []
        st.session_state.executed =[]
        st.session_state.logged_in = False
        with st.container():
            st.markdown("Are you sure you want to log out?")
            col1, col2 = st.columns(2)
            if col1.button("Yes"):
                return True
            if col2.button("No"):
                return False
            
    
            
    
def page_1():
    page_1 = st.set_page_config(page_title= "DIA System",layout="centered",page_icon=":ice-cube:")
    return page_1

s3 = boto3.client('s3')

def upload_to_s3(local_folder_path,s3_folder_prefix,bucket_name):
    try:
        for root, dirs, files in os.walk(local_folder_path):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                # Calculate the S3 object key based on the local file's path and the desired prefix
                relative_file_path = os.path.relpath(local_file_path, local_folder_path)
                s3_object_key = os.path.join(s3_folder_prefix, relative_file_path)
                s3.upload_file(local_file_path, bucket_name, s3_object_key)
                logging.info(f"Uploaded '{local_file_path}' to '{bucket_name}/{s3_object_key}'")
    except Exception as e:
        raise ImageAnalysisException(e,sys)



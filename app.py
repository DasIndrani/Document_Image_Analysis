import sys
from Doc_Image_Analysis.components.web_app import App
from Doc_Image_Analysis.components.main import MainFunction
from Doc_Image_Analysis.exception import ImageAnalysisException

if __name__ =="__main__":
    try:
        main_function = MainFunction()
        app = App(main_function=main_function)
        app.start()
    except Exception as e:
        raise ImageAnalysisException(e,sys)
from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirement(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    Requirements=[]
    with open(file_path) as file_obj:
       Requirements=file_obj.readlines()
       Requirements=[req.replace("\n"," ") for req in Requirements] 
       if HYPEN_E_DOT in Requirements:
         Requirements.remove(HYPEN_E_DOT)
    return Requirements

setup(
name='Document Inage Analysis',
version='0.0.1',
author=('Indrani', 'Subhajit'),
author_email='dindrani199@gmail.com',
packages=find_packages(),
install_requries=get_requirement('requirements.txt'),

)
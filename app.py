import os
from pathlib import Path 
import subprocess

def launch_app():
    
    #set root directory
    curr_dir = Path(__file__)
    root_dir = str(curr_dir.parent.absolute())
    os.chdir(root_dir+'/app')
    
    frontend_dir =  root_dir+'/app/frontend/frontend.py'

    # #launch backend
    subprocess.Popen(["uvicorn", "backend.backend:app"])

    #launch frontend
    os.system('streamlit run '+frontend_dir)

if __name__ == "__main__":
    launch_app()

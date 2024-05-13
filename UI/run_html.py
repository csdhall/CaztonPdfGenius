import os  
from flask import Flask, send_from_directory  
from flask_cors import CORS  
  
project_directory = '/Users/cazton/Documents/Projects/CaztonPdfGenius/'  
static_folder_path = os.path.join(project_directory, 'UI')  


  
app = Flask(__name__, static_folder=static_folder_path)  
CORS(app)  # Enable CORS for all routes  
  
@app.route('/')  
def serve_html():  
    print(app.static_folder)
    return send_from_directory(app.static_folder, 'index.html')  
  
if __name__ == '__main__':  
    app.run(debug=True, port=5501)  

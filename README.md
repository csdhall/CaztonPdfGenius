Here's a markdown version of the steps to run the FastAPI application:  
   
---  

## NOTE: Use this if you're already set up
Run this on termincal. This will run HTML with NO CORS. DO NOT use in production
``` cd UI
    python run_html.py```

Then run this
## Server.py has BOTH youtube and PDF working. 

``` cd Server ```
``` python server_WORKS2.py ```

or
``` python pdf_azure_openai_embeddings.py ```
or 
``` python pdf_azure_openai_fast_api.py ```

Make sure CORS is ON on Edge. 
Open URL on edge
```http://127.0.0.1:5000/```
   
## How to Run the FastAPI Application  
   
### 1. Check Python Version  
   
Make sure you have Python 3.7 or higher installed on your system. You can check your Python version by running `python --version` or `python3 --version` in your terminal.  
   
### 2. Set Up a Virtual Environment  
   
Create a virtual environment by running:  
   
```bash  
python3 -m venv env  
```  
   
Activate the virtual environment:  
   
- On macOS/Linux:  
  
  ```bash  
  source env/bin/activate  
  ```  
   
- On Windows:  
  
  ```bash  
  env\Scripts\activate  
  ```  
   
### 3. Install Required Libraries  
   
Install the necessary libraries using pip:  
   
```bash  
pip install fastapi uvicorn PyPDF2 langchain tiktoken openai python-dotenv pydantic faiss-cpu  
```  
   
**Note**: If you're using macOS with Apple Silicon (M1 chip), you may need to install FAISS with Homebrew and then install the Python bindings:  
   
```bash  
brew install faiss  
pip install faiss  
```  
   
### 4. Create a `.env` File  
   
Create a `.env` file in the same directory as the script containing the required API keys:  
   
```  
OPENAI_API_KEY=your_openai_api_key  
OPENAI_API_TYPE=azure  
OPENAI_API_BASE=https://your_openai_api_base_url  
OPENAI_API_VERSION=2023-03-15-preview  
```  
   
Replace `your_openai_api_key` with your actual OpenAI API key and `your_openai_api_base_url` with the appropriate base URL.  
   
### 5. Save the Provided Code  
   
Save the provided code in a file named `app.py` (or any other name you prefer) in the same directory as the `.env` file.  
   
### 6. Run the FastAPI Application  
   
Run the FastAPI application using Uvicorn:  
   
```bash  
uvicorn app:app --reload  
```  
   
This command assumes that the FastAPI app is defined in a file named `app.py`. If you used a different file name, replace `app` in `app:app` with the actual file name (without the .py extension).  
   
### 7. Access the Application  
   
Once the application is running, you can access it at `http://127.0.0.1:8000/`. Use an API client like Postman or CURL to make requests to the `/qa` endpoint, or access the interactive API documentation at `http://127.0.0.1:8000/docs`.  

To use a different port
```uvicorn cazton_pdf_ai_azure:app --reload --port 8080  ```

   
---
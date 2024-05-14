from fastapi import FastAPI, HTTPException, File, UploadFile  
from fastapi.middleware.cors import CORSMiddleware  
import uvicorn  
from PyPDF2 import PdfReader  
import os  
import requests  
import io  
from openai import AzureOpenAI  
from dotenv import load_dotenv  
from urllib.parse import urlparse  
  
# Load environment variables from the .env file  
load_dotenv(".env", override=True)  
  
# Initialize AzureOpenAI client  
client = AzureOpenAI(  
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version=os.getenv("OPENAI_API_VERSION"),  
    azure_deployment=os.getenv("Gpt4Turbo-2023-04-09")  
)  
app = FastAPI()  
  
# Add CORS middleware  
origins = [  
    "http://localhost",  
    "http://localhost:5501",  
    "http://127.0.0.1",  
    "http://127.0.0.1:5501",  
]  
  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  
  
current_context = ""  
clean_text = ""  
  
@app.post("/upload")  
async def upload_pdf(file: UploadFile = File(...)):  
    global clean_text  
    if file.content_type != "application/pdf":  
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")  
  
    raw_text = ""  
    reader = PdfReader(file.file)  
    for page in reader.pages:  
        text = page.extract_text()  
        if text:  
            raw_text += text  
  
    clean_text = raw_text.replace("\n", " ")  
    clean_text = ' '.join(clean_text.split())  
  
    return {"response": f"{file.filename} uploaded successfully"}  
  
@app.post("/qa")  
async def ask_question(request: dict):  
    global clean_text  
  
    query = request.get("key")  
    print("***********")  
    print(f"Query: {query}")  
    if not query:  
        raise HTTPException(status_code=400, detail="Query must not be empty")  
  
    # Check if the query is a URL  
    parsed_url = urlparse(query)  
    if parsed_url.scheme in ("http", "https") and parsed_url.netloc:  
        response = requests.get(query)  
        if response.headers['Content-Type'] != "application/pdf":  
            raise HTTPException(status_code=400, detail="Invalid file type. Please provide a PDF URL.")  
  
        raw_text = ""  
        pdf_file = io.BytesIO(response.content)  
        reader = PdfReader(pdf_file)  
        for page in reader.pages:  
            text = page.extract_text()  
            if text:  
                raw_text += text  
  
        clean_text = raw_text.replace("\n", " ")  
        clean_text = ' '.join(clean_text.split())  
  
    prompt = query + " Text: " + clean_text  
    print("***********")  
    print(f"prompt: {prompt}")  
  
    response = client.chat.completions.create(  
        messages=[  
            {"role": "system", "content": "You are a helpful assistant."},  
            {"role": "user", "content": prompt}  
        ],  
        model=os.getenv("Gpt4Turbo-2023-04-09"),  
    )  
  
    answer = response.choices[0].message.content.strip()  
    print(answer)  
  
    return {"response": answer}  
  
if __name__ == "__main__":  
    uvicorn.run(app, host="127.0.0.1", port=5500)  

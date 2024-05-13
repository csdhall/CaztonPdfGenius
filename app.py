# app.py

from PyPDF2 import PdfReader
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import pickle
from Utilities.video import get_youtube_transcript, parse_youtube_link
from Utilities.vector import *
import CONSTANTS
import tiktoken
# Get your API keys from openai, you will need to create an account. 
# Here is the link to get the keys: https://platform.openai.com/account/billing/overview
import os
from dotenv import load_dotenv

os.environ.clear()
# Load environment variables from the .env file
load_dotenv(".env", override=True)
import os

print("********")

cazton_gpt4_model = os.getenv("Gpt4Turbo-2023-04-09")
openai_api_version = os.getenv("OPENAI_API_VERSION")
chatAzureOpenAI = AzureChatOpenAI(
        azure_deployment=cazton_gpt4_model,
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model=cazton_gpt4_model,
        temperature=0,
    )


file_name=CONSTANTS.FILE

file_path = f'Docs/{file_name}.pdf'

reader = PdfReader(file_path)

print(f"file_path: {file_path}")
print(f"reader: {reader}")

# read data from the file and put them into a variable called raw_text
raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

# raw_text

raw_text[:100]
print(f"raw_text: {raw_text[:100]}")

# Remove newline characters
clean_text = raw_text.replace("\n", " ")

# Remove multiple spaces
clean_text = ' '.join(clean_text.split())

print(clean_text)
# We need to split the text that we read into smaller chunks so that during information retreival we don't hit the token size limits. 

strings_to_remove = ["<|endoftext|>", "endoftext"]

for string in strings_to_remove:
    clean_text = clean_text.replace(string, "")

print(f"\n\n clean_text : {clean_text}\n\n")

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI


chatAzureOpenAI = AzureChatOpenAI(
        azure_deployment=cazton_gpt4_model,
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model=cazton_gpt4_model,
        temperature=0,
    )



from fastapi import FastAPI, HTTPException, Depends  
from fastapi.middleware.cors import CORSMiddleware  
import uvicorn  

  
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
  
from pydantic import BaseModel  
  
class QuestionRequest(BaseModel):  
    key: str  

import os  
  
 
@app.post("/qa")  
async def ask_question(request: QuestionRequest):  
    global current_context  
    global current_docsearch_instance  
  
    query = request.key  
    print("***********")  
    print(query)  
    if not query:  
        raise HTTPException(status_code=400, detail="Query must not be empty")  
  
    # Check if the user wants to switch to the PDF context  
    if query.lower() == "pdf":  
        current_context = clean_text
        return {"response": "Switched to PDF context."}  

    query = query + "Text: " + clean_text
    response = chatAzureOpenAI([HumanMessage(content=query)])
    print(response.content)  
  
    return {"response": response.content}  

 
if __name__ == "__main__":  
    uvicorn.run(app, host="127.0.0.1", port=5500)  



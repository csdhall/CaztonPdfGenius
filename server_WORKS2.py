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

# # List of environment variables to delete
# env_vars_to_delete = ["base_url"]
# # env_vars_to_delete = ["base_url", "OPENAI_API_TYPE", "OPENAI_API_BASE", "OPENAI_API_VERSION"]

# # Delete each environment variable
# for var in env_vars_to_delete:
#     if var in os.environ:
#         del os.environ[var]

# Access the OPENAI_API_KEY environment variable
# openai_api_key = os.environ.get("OPENAI_API_KEY")
# openai_api_type = os.environ.get("OPENAI_API_TYPE")
# openai_api_base = os.environ.get("OPENAI_API_BASE")
# openai_api_version = os.environ.get("OPENAI_API_VERSION")

# print(f"openai_api_base: {openai_api_base}")
# print(f"openai_api_version: {openai_api_version}")
# print(f"openai_api_key: {openai_api_key}")
# print(f"base_url: {os.environ.get('base_url')}")
print("********")
# exit()
cazton_gpt4_model = os.getenv("CaztonGpt4_0125_Preview")
openai_api_version = os.getenv("OPENAI_API_VERSION")
chatAzureOpenAI = AzureChatOpenAI(
        azure_deployment=cazton_gpt4_model,
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model=cazton_gpt4_model,
        temperature=0,
    )

# message = HumanMessage(content="tell a joke")
# response = chatAzureOpenAI([message])
# print(f"response: {response}")
# exit()

# location of the pdf file/files. 
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
# chain = load_qa_chain(ChatOpenAI(engine=gpt4_model, temperature=0.3, max_tokens=3000), chain_type="stuff")

# query = "who are the authors of the article?"
# docs = docsearch.similarity_search(query)
# chain.run(input_documents=docs, question=query)

# Start an infinite loop to continuously ask questions

# NOTE: Uncomment WHILE loop to test
# while True:
#     # Prompt the user to enter a question
#     query = input("Enter your question (or type 'exit' to quit): ")
    
#     # Check if the user wants to exit the loop
#     if query.lower() == 'exit':
#         break

#     # Perform similarity search using the query
#     docs = docsearch.similarity_search(query)
    
#     # Run the question-answering chain
#     response = chain.run(input_documents=docs, question=query)
    
#     # Print the response
#     print(response)

# # # Exit message
# print("Exiting the question-answering loop.")

def get_transcript(query):  
    youtube_url = parse_youtube_link(query)  
    if youtube_url:  
        print("***********")
        print(youtube_url)
        video_id = youtube_url.split("watch?v=")[-1]  
        file_name = f"Data/{video_id}.txt"  
  
        if os.path.exists(file_name):  
            # Read the transcript from the existing file  
            with open(file_name, "r") as file:  
                transcript = file.read()  
        else:  
            # Fetch the transcript and save it to a new file  
            transcript = get_youtube_transcript(video_id)  
            with open(file_name, "w") as file:  
                file.write(transcript)  
  
        global current_context  
        global current_docsearch_instance  
        current_context = "youtube"  
        current_docsearch_instance = search_documents(transcript, embeddings)  
        return transcript  
    else:  
        return None   

# exit()
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



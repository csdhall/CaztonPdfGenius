from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chat_models import ChatOpenAI
import pickle
from Utilities.video import get_youtube_transcript, parse_youtube_link
from Utilities.vector import *
import CONSTANTS
import tiktoken
# Get your API keys from openai, you will need to create an account. 
# Here is the link to get the keys: https://platform.openai.com/account/billing/overview
import os
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv(".env", override=True)

# Access the OPENAI_API_KEY environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_api_type = os.environ.get("OPENAI_API_TYPE")
openai_api_base = os.environ.get("OPENAI_API_BASE")
openai_api_version = os.environ.get("OPENAI_API_VERSION")

# print(f"openai_api_base: {openai_api_base}")
# print(f"openai_api_version: {openai_api_version}")
# print(f"openai_api_key: {openai_api_key}")
# print(f"openai_api_type: {openai_api_type}")
# print("********")


# location of the pdf file/files. 
file_name=CONSTANTS.FILE

file_path = f'Docs/{file_name}.pdf'

# reader = PdfReader(file_path)

# print(f"file_path: {file_path}")
# print(f"reader: {reader}")

# # read data from the file and put them into a variable called raw_text
# raw_text = ''
# for i, page in enumerate(reader.pages):
#     text = page.extract_text()
#     if text:
#         raw_text += text

# # raw_text

# raw_text[:100]
# print(f"raw_text: {raw_text[:100]}")
# We need to split the text that we read into smaller chunks so that during information retreival we don't hit the token size limits. 

# text_splitter = CharacterTextSplitter(        
#     separator = "\n",
#     chunk_size = 1000,
#     chunk_overlap  = 200,
#     length_function = len,
# )
# texts = text_splitter.split_text(raw_text)

# len(texts)
# print(f"len(texts): {len(texts)}")

# texts = [item.replace("<|endoftext|>", "endoftext") for item in texts]
# print(f"len(texts): {len(texts)}")

# for i, text in enumerate(texts):
#     result = "<|endoftext|>" in text
#     if result == True:
#         print(f"i: {result} <|endoftext|>")
#         print(f"********")

# for i, text in enumerate(texts):
#     result = "endoftext" in text
#     if result == True:
#         print(f"i: {result} endoftext")
#         print(f"********")

# texts[0]
# print(f"texts[0]: {texts[0]}")
# texts[1]

# Download embeddings from OpenAI
embeddings_model = "Cazton-ada-2"
tokenizer = tiktoken.get_encoding("cl100k_base")

# NOTE: DO THIS FIRST. Uncomment and run.
embeddings = OpenAIEmbeddings(deployment=embeddings_model,
                              openai_api_base=openai_api_base,
                              openai_api_version=openai_api_version,
                              openai_api_key=openai_api_key,
                              openai_api_type=openai_api_type,
                              chunk_size=1)

print(f"\n\n\ Embeddings: {embeddings} \n")


import pickle  
  
file_path_pkl = get_file_path(file_name)
embeddings = create_embeddings_if_not_exists(file_path_pkl, embeddings)

# print("/n/n/ Embeddings saved to pickle file /n/n/n")
# exit()
import pickle  

file = f'Data/{file_name}.pkl'
with open(file, 'rb') as f:  
    print(f"\n Reading.........{file}")
    embeddings = pickle.load(f)  

docsearch = FAISS.from_texts(texts, embeddings)

current_context = None  # Possible values: None, "youtube", "pdf"  
current_docsearch_instance = docsearch  # Set the initial docsearch instance to the PDF  


from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

# gpt3_model = "CaztonDavinci3"
gpt4_model = "CaztonGpt-4Turbo"

chain = load_qa_chain(ChatOpenAI(engine=gpt4_model, temperature=0.3, max_tokens=3000), chain_type="stuff")
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

def search_documents(input_text, embeddings):  
    text_splitter = CharacterTextSplitter(  
        separator="\n",  
        chunk_size=1000,  
        chunk_overlap=200,  
        length_function=len,  
    )  
    chunks = text_splitter.split_text(input_text)  
    docsearch_instance = FAISS.from_texts(chunks, embeddings)  
    return docsearch_instance  
  
app = FastAPI()  
  
# Add CORS middleware  
origins = [  
    "http://localhost",  
    "http://localhost:5000",  
    "http://127.0.0.1",  
    "http://127.0.0.1:5000",  
]  
  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  
  
# ... (your existing code)  


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
        current_context = "pdf"  
        current_docsearch_instance = docsearch  
        return {"response": "Switched to PDF context."}  
  
    # Check if the query contains a YouTube link  
    youtube_url = parse_youtube_link(query)  
    if youtube_url:  
        transcript = get_transcript(query)  
        query = "Summarize the video. Also share key highlights."  
        current_context = "youtube"  
  
    if current_context == "youtube":  
        docs = current_docsearch_instance.similarity_search(query)  
    else:  
        docs = docsearch.similarity_search(query)  
  
    response = chain.run(input_documents=docs, question=query)  
    print(response)  
  
    return {"response": response}  

 


if __name__ == "__main__":  
    uvicorn.run(app, host="0.0.0.0", port=8080)  



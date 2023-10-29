from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chat_models import ChatOpenAI
import pickle
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import tiktoken
import os

from Utilities.video import *
from Utilities.vector import *

global last_transcript

from dotenv import load_dotenv
load_dotenv(".env", override=True)

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_api_type = os.environ.get("OPENAI_API_TYPE")
openai_api_base = os.environ.get("OPENAI_API_BASE")
openai_api_version = os.environ.get("OPENAI_API_VERSION")

# print(f"openai_api_base: {openai_api_base}")
# print(f"openai_api_version: {openai_api_version}")
# print(f"openai_api_key: {openai_api_key}")
# print(f"openai_api_type: {openai_api_type}")

embeddings_model = "CaztonEmbedAda2"
tokenizer = tiktoken.get_encoding("cl100k_base")

# NOTE: DO THIS FIRST. Uncomment and run.
embeddings = OpenAIEmbeddings(deployment=embeddings_model,
                              openai_api_base=openai_api_base,
                              openai_api_version=openai_api_version,
                              openai_api_key=openai_api_key,
                              openai_api_type=openai_api_type,
                              chunk_size=1)


# gpt3_model = "CaztonDavinci3"
gpt4_model = "CaztonGpt-4"

chain = load_qa_chain(ChatOpenAI(engine=gpt4_model, temperature=0.3, max_tokens=3000), chain_type="stuff")


def get_transcript(query):  
    youtube_url = parse_youtube_link(query)  
    if youtube_url:  
        print("***********")
        print(youtube_url)
        video_id = youtube_url.split("watch?v=")[-1]  
        transcript = create_transcript_if_not_exists(video_id)
        # file_name = video_id 
          
        # file_path_pkl = get_file_path(file_name)
        # embeddings = create_embeddings_if_not_exists(file_path_pkl, embeddings)
         
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
    global last_transcript 
    query = request.key  
    print("***********")  
    print(f"\n\n Query: {query} \n\n")

    if not query:  
        raise HTTPException(status_code=400, detail="Query must not be empty")  
  
    # Check if the query contains a YouTube link  
    youtube_url = parse_youtube_link(query)  
    if youtube_url:  
        transcript = get_transcript(query)
        last_transcript = transcript  
        query = "Summarize the video. Also share key highlights."  

    print(f"\n\n Transcript: {last_transcript[:40]} \n\n")
    docsearch = search_documents(last_transcript, embeddings)
    docs = docsearch.similarity_search(query)  

    response = chain.run(input_documents=docs, question=query)  
    print(response)  
  
    return {"response": response}  

 


if __name__ == "__main__":  
    uvicorn.run(app, host="0.0.0.0", port=8080)  



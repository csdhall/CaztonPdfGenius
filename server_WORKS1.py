from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chat_models import ChatOpenAI
import pickle
from Utilities.video import get_youtube_transcript, parse_youtube_link
from Utilities.vector import create_embeddings_if_not_exists, get_file_path
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

reader = PdfReader(file_path)

print(f"file_path: {file_path}")
print(f"reader: {reader}")

# read data from the file and put them into a variable called raw_text
raw_text = ''
for i, page in enumerate(reader.pages[:22]):
    text = page.extract_text()
    if text:
        raw_text += text

# raw_text

raw_text[:100]
# print(f"raw_text: {raw_text[:100]}")
# We need to split the text that we read into smaller chunks so that during information retreival we don't hit the token size limits. 

text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

len(texts)
print(f"len(texts): {len(texts)}")

texts = [item.replace("<|endoftext|>", "endoftext") for item in texts]
print(f"len(texts): {len(texts)}")

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

print("/n/n/ Embeddings saved to pickle file /n/n/n")
exit()
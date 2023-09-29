from PyPDF2 import PdfReader  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text_splitter import CharacterTextSplitter  
from langchain.vectorstores import FAISS  
import tiktoken  
import os  
from dotenv import load_dotenv  
from pydantic import BaseModel  
import pickle  
  
# Load environment variables from the .env file  
load_dotenv(".env", override=True)  


  
# Access the OPENAI_API_KEY environment variable  
openai_api_key = os.environ.get("OPENAI_API_KEY")  
openai_api_type = os.environ.get("OPENAI_API_TYPE")  
openai_api_base = os.environ.get("OPENAI_API_BASE")  
openai_api_version = os.environ.get("OPENAI_API_VERSION")  

print(openai_api_key)
print(openai_api_type)
print(openai_api_base)
print(openai_api_version)
  
def get_pdf_text(pdf_docs):  
    text = ""  
    for pdf in pdf_docs:  
        pdf_reader = PdfReader(pdf)  
        for page in pdf_reader.pages:  
            text += page.extract_text()  
    return text  
  
raw_text = get_pdf_text(['docs/Orca.pdf'])  
  
text_splitter = CharacterTextSplitter(          
    separator = "\n",  
    chunk_size = 1000,  
    chunk_overlap  = 200,  
    length_function = len,  
)  
texts = text_splitter.split_text(raw_text)  
  
embeddings_model = "CaztonEmbedAda2"  
tokenizer = tiktoken.get_encoding("cl100k_base")  
  
embeddings = OpenAIEmbeddings(  
    deployment = embeddings_model,  
    chunk_size = 1)  
  
docsearch = FAISS.from_texts(texts, embeddings)  
  
with open("docsearch.pkl", "wb") as f:  
    pickle.dump(docsearch, f)  
  
from langchain.chains.question_answering import load_qa_chain  
from langchain.llms import OpenAI  
  
gpt3_model = "CaztonDavinci3"  
  
chain = load_qa_chain(OpenAI(engine=gpt3_model, temperature=0), chain_type="stuff")  
  
def get_answer(query: str):  
    with open("docsearch.pkl", "rb") as f:  
        docsearch = pickle.load(f)  
        docs = docsearch.similarity_search(query)  
      
    response = chain.run(input_documents=docs, question=(query))  
      
    return response  
  
if __name__ == "__main__":  
    while True:  
        question = input("Enter your question (or type 'exit' to quit): ")  
        if question.lower() == "exit":  
            break  
        answer = get_answer(question)  
        print("Answer:", answer)  

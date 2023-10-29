import pickle 
from langchain.embeddings.openai import OpenAIEmbeddings
import os

def create_embeddings(file_name):
    file_path = get_file_path(file_name)
    with open(file_path, 'wb') as f:  
        pickle.dump(embeddings, f)  
        print(f"/n/n/ Embeddings saved to pickle file: {file_path} /n/n/n")


def read_embeddings(file_name):
    file_path = get_file_path(file_name)
    with open(file, 'rb') as f:  
        print(f"\n\n Reading.........{file_path} \n\n\n")
        embeddings = pickle.load(f)  


def get_file_path(file_name):
    return f'Data/{file_name}.pkl'

import os
import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma 
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()

chroma_client = chromadb.PersistentClient(path="./data/chromadb")

embedding_function = OllamaEmbeddings(model="nomic-embed-text")
collection_name = os.getenv("CHROMA_COLLECTION_NAME")

directory = "/Users/kevinshah/Downloads/"

def ingest_file(file_path):    
    print(f"Loading {file_path}")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    chunked_documents = text_splitter.split_documents(documents)

    if not chunked_documents:
        print(f"Skipping {os.path.basename(file_path)}: No extractable text found.")
        return
    
    collection = chroma_client.get_or_create_collection(collection_name)
    print(f"Purging existing chunks for {os.path.basename(file_path)}...")
    collection.delete(where={"source": file_path})

    Chroma.from_documents(
        documents=chunked_documents,
        embedding=embedding_function,
        collection_name=collection_name,
        client=chroma_client,
    )
    print(f"Ingested {os.path.basename(file_path)} successfully!")

if __name__ == "__main__":
    directory = "/Users/kevinshah/Downloads"
    for root,_,files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".pdf"):
                file_path = os.path.join(root,file_name)
                ingest_file(file_path)
                


from fastapi import FastAPI, HTTPException
import langchain
from langchain_groq import ChatGroq
import getpass
import pickle
import faiss
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler
from langchain_community.vectorstores import FAISS
import numpy as np
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import PyPDF2
from langchain.vectorstores import Chroma
import langchain
from langchain import HuggingFaceHub
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import getpass
import os
from tqdm import tqdm

load_dotenv()

inference_api_key = os.getenv('INFERENCE_API_KEY')
os.environ['HUGGINGFACEHUB_API_TOKEN'] = inference_api_key

embeddings_model_name = "mixedbread-ai/mxbai-embed-large-v1"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

index_loc = "D:\\Web Development\\Assignments\\Qilo\\Web Scrapper Tool\\luke_skywalker_index\\index.faiss"


data = []
directory = '.'
total_files = len([name for name in os.listdir(directory) if name.endswith('.pdf')])
print(total_files)

# Use tqdm to iterate over the files with progress bar
for file in tqdm(os.listdir(directory), total=total_files, desc='Processing PDFs'):
    file_path = os.path.join(directory, file)

    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)
        docs = loader.load_and_split(text_splitter=text_splitter)
        data.extend(docs)
        print(f'Done with ${file}')


persist_directory = "D:\\Web Development\\Assignments\\Qilo\\Web Scrapper Tool\\chroma_starwars_character_index"

vectordb = Chroma.from_documents(documents=data, embedding=embeddings, persist_directory=persist_directory)

vectordb.persist()
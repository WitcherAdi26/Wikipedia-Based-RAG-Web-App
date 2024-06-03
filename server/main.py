from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler
from langchain_community.vectorstores import Chroma
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192", max_tokens = 800)

embeddings_model_name = "mixedbread-ai/mxbai-embed-large-v1"

embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

persist_directory = "chroma_starwars_character_index"
saved_vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

retriever = saved_vectordb.as_retriever(search_type = 'mmr')
retriever.search_kwargs['fetch_k'] = 20
retriever.search_kwargs['k'] = 3

question_template = '''You are a smart AI who responds based on the provided context data. When given context data and question, you use the context data to form a relevant, descriptive response(max 800 words) to the question asked. Ensure that the question is answered in the initial part of response. Dont mention anything like 'according to the context' or 'based on the context'. Answer as if you are a huge starwars fan.

context = {context}

question = {question}

Answer:\n'''

question_prompt = PromptTemplate(input_variables = ['context','question'], template = question_template)

chain_query = RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": question_prompt},
    verbose=False
)

handler = StdOutCallbackHandler()


def query_responder(question):
    return chain_query.invoke(question)


class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question
    if not question:
        raise HTTPException(status_code=400, detail="Please provide a question.")
    
    response = query_responder(question)
    return {"response": response}

# PORT = int(os.getenv('PORT', 8000))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=PORT)


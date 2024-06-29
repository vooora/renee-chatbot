from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
import openai
import os
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the specific origin(s) you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FAISS_PATH = 'vectorstores/db_faiss'
OPENAI_API_KEY = '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'

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

custom_prompt_template = """Use the following pieces of information to answer the user's question. If you don't know the answer to the question then just say that you are unaware of the answer do not try to come up with an answer if you are unsure.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.

Helpful answer:
"""

def set_custom_prompt():
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context', 'question'])
    return prompt

def call_openai_model(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Adjust the model name as needed
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.5,
    )
    return response.choices[0].message['content'].strip()

def qa_bot():
    print("Loading embeddings and vector store...")
    start_time = time.time()
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    end_time = time.time()
    print(f"Embeddings and vector store loaded in {end_time - start_time} seconds")
    
    print("Setting up QA chain...")
    qa_prompt = set_custom_prompt()

    print("QA chain set up successfully.")
    return qa_prompt, db

def final_result(query, history):
    print("Setting up QA bot...")
    qa_prompt, db = qa_bot()
    print(f"Processing query: {query}")

    history.append(query)
    full_query = " ".join(history)

    #context = "Context from vector store"

    #Retrieve context from vector store
    retrieved_documents = db.as_retriever().get_relevant_documents(full_query)
    context = " ".join([doc.page_content for doc in retrieved_documents])

    prompt = qa_prompt.format(context=context, question=full_query)
    response = call_openai_model(prompt)
    return response

class QueryModel(BaseModel):
    query: str



@app.post("/chat")
async def chat(query: QueryModel):
    query_history = []
    try:
        print(f"Received query: {query.query}")
        start_time = time.time()

        # Process the query and append to the history
        response = final_result(query.query, query_history)
        query_history.append(response+" This is the chatbot's reply to the latest question")
        end_time = time.time()
        print(f"Response generated in {end_time - start_time} seconds")
        return {"response": response}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
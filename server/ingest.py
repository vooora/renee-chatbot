from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

DATA_PATH = 'data/'
DB_FAISS_PATH = 'vectorstores/db_faiss'

def create_vector_db():
    loader = DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()

    for i, doc in enumerate(documents):
        print(f"Document {i}:")
        print(f"Metadata: {doc.metadata}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    all_embeddings = embeddings.embed_documents([text.page_content for text in texts])
    
    print(f"number of embeddings: {len(all_embeddings)}")

    db = FAISS.from_documents(texts, embeddings)

    db.save_local(DB_FAISS_PATH)
    print("success")

if __name__ == '__main__':
    create_vector_db()

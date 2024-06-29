from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
import os

# Ensure the OpenAI API key is set as an environment variable
OPENAI_API_KEY = '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'

DATA_PATH = 'data/'
DB_FAISS_PATH = 'vectorstores/db_faiss'

def create_vector_db():
    loader = DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()
    
    # Debug: Print the number of documents loaded
    print(f"Number of documents loaded: {len(documents)}")
    
    if not documents:
        print("No documents found. Ensure the data directory and file pattern are correct.")
        return

    # Debug: Print details of the loaded documents
    for i, doc in enumerate(documents):
        print(f"Document {i}:")
        print(f"Metadata: {doc.metadata}")
        if doc.page_content:
            print(f"Content: {doc.page_content[:500]}...")  # Print the first 500 characters of the document content
        else:
            print("No content found for this document.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    # Debug: Print the number of text chunks created
    print(f"Number of text chunks created: {len(texts)}")

    if not texts:
        print("No text chunks created. Ensure the documents are not empty and are processed correctly.")
        return

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    # Generate embeddings
    all_embeddings = embeddings.embed_documents([text.page_content for text in texts])
    
    # Debug: Check if embeddings are created
    print(f"Number of embeddings created: {len(all_embeddings)}")

    if not all_embeddings:
        print("No embeddings created. Check the model and embedding process.")
        return

    db = FAISS.from_documents(texts, embeddings)

    db.save_local(DB_FAISS_PATH)
    print("Vector database created and saved locally.")

if __name__ == '__main__':
    create_vector_db()

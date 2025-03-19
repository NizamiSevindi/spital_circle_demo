import os
import time
from src.helper import load_pdf_file, text_split
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

CHROMA_DB_PATH = "chroma_storage"
os.makedirs(CHROMA_DB_PATH, exist_ok=True)

embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

extracted_data=load_pdf_file(data='Data/')
text_chunks=text_split(extracted_data)

BATCH_SIZE = 200 
WAIT_TIME = 30 

vector_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
existing_docs = set(vector_db.get()["documents"]) if vector_db.get() else set()

new_chunks = [chunk for chunk in text_chunks if chunk.page_content not in existing_docs]

if new_chunks:
    for i in range(0, len(new_chunks), BATCH_SIZE):
        batch = new_chunks[i:i + BATCH_SIZE]

        try:
            vector_db.add_documents(documents=batch)
            print(f"✅ {i+1}/{len(new_chunks)} new documents were added.")
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"⏳ Waiting for {WAIT_TIME} seconds...")
            time.sleep(WAIT_TIME)
            vector_db.add_documents(documents=batch)

    print(f"📂 New PDF data was successfully added in '{CHROMA_DB_PATH}'")
else:
    print("🚀 All documents are already stored. No new documents were added.")
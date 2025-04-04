import os
from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_pdf(data):
    documents = []
    for pdf_file in os.listdir(data):
        if pdf_file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data, pdf_file))
            pages = loader.load() 
            for page in pages:
                page_num = int(page.metadata.get('page_label', page.metadata.get('page', 0) + 1))
                page.metadata['source'] = pdf_file
                page.metadata['page'] = page_num
                print(page.metadata)
            documents.extend(pages)
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
    split_docs = splitter.split_documents(documents)
    return split_docs
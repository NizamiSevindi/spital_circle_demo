import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
import subprocess 
import re
from src.prompt import SYSTEM_PROMPT


app = Flask(__name__)

load_dotenv()

CHROMA_DB_PATH = "chroma_storage"

embeddings = AzureOpenAIEmbeddings(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_EMBED_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

if os.path.isdir(CHROMA_DB_PATH):
    docsearch = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    print("Chroma database found.")
else:
    subprocess.run(["python", "store_index.py"])
    docsearch = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    print("Chroma database not found. Creating a new one.")

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = AzureChatOpenAI(
    model=os.getenv("DEPLOYMENT_NAME"),
    api_key=os.environ["AZURE_OPENAI_API_KEY"] ,  
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.environ["ENDPOINT_URL"]
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input} \n\nContext:\n{context}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    print("User: ", msg)
    
    response = rag_chain.invoke({"input": msg})
    raw_text = response["answer"]
    print("Response: ", response["answer"])
    
    formatted_text = raw_text.replace("\n", "<br>")
    formatted_text = re.sub(r"(\d+)\.\s", r"<li>", formatted_text)  
    formatted_text = formatted_text.replace("</li><br>", "</li>") 
    formatted_text = re.sub(r"(<li>.*?</li>)", r"<ol>\1</ol>", formatted_text) 

    formatted_text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2" target="_blank">\1</a>', formatted_text)

    return formatted_text

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

import os
import subprocess 
from dotenv import load_dotenv
from src.prompt import SYSTEM_PROMPT
from flask import Flask, render_template, request
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from flask import send_from_directory

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
    ("human", "{input}\n\nContext:\n{context}"),
])

def rag_chain_with_links(question):
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    """ 
    context = json.dumps(
        [{"page_content": doc.page_content} for doc in docs],
        ensure_ascii=False,
        indent=2
    ) 
    """

    response = llm.invoke(prompt.format(input=question, context=context))
    
    sources = "".join([
        f"""
            <details style='margin-bottom: 10px;'>
                <summary>
                    Source {i+1} – {doc.metadata.get("source", "Unbekannt")} / Seite {doc.metadata.get("page", 1)}
                </summary>
                <a href="Data/{doc.metadata.get("source", "#")}#page={doc.metadata.get("page", 1)}" target="_blank">
                    🔗 Zum PDF (Seite {doc.metadata.get("page", 1)})
                </a><br><br>
                <pre style="white-space: pre-wrap;">{doc.page_content}</pre>
            </details>
        """
        for i, doc in enumerate(docs)
    ])

    return {"answer": f"{response.content}<br><br>{sources}"}

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    print("User: ", msg)
    
    response = rag_chain_with_links(msg)
    raw_text = response["answer"]
    return raw_text

@app.route('/Data/<path:filename>')
def serve_data(filename):
    return send_from_directory('Data', filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

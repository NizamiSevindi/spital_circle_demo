# End-to-end-Medical-Chatbot-Generative-AI


# How to run?
### STEPS:

### STEP 01- Create a .venv environment 

```bash
python -m venv .venv
```

```bash
.\.venv\Scripts\activate.ps1
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


### Create a `.env` file in the root directory and add your Pinecone & openai credentials as follows:

```ini
AZURE_OPENAI_DEPLOYMENT_NAME="text-embedding-ada-002"
AZURE_OPENAI_EMBED_API_VERSION="2023-05-15"
AZURE_OPENAI_ENDPOINT="xxxxxxxxxx"
AZURE_OPENAI_API_KEY="xxxxxxxxxxx"

DEPLOYMENT_NAME="gpt-4o"
ENDPOINT_URL="xxxxxxx"
AZURE_OPENAI_API_VERSION="2024-05-01-preview"
```


```bash
# run the following command to store embeddings
python store_index.py
```

```bash
# Finally run the following command
python app.py
```


### Techstack Used:

- Python
- LangChain
- Flask
- Azure OpenAI
- ChromaDB


langchain-huggingface-0.1.2 sentence-transformers-3.4.1
pip install -U langchain langchain-community langchain-openai langchain-huggingface
pip install -U sentence-transformers huggingface_hub

 langchain-0.3.21
 langchain-community-0.3.20
 langchain-huggingface-0.1.2
 langchain-openai-0.3.9
 langchain-text-splitters-0.3.7
 pip install --upgrade --quiet  langchain sentence_transformers

 pip install -qU "langchain-chroma>=0.1.2"
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

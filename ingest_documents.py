import os
from pypdf import PdfReader
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import Pinecone as LangchainPineconeStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY environment variable missing")

# Constants
INDEX_NAME = "langchain-bedrock-index"
DATA_DIR = "./data"

pc = Pinecone(api_key=api_key)

# Create index if it doesn't exist
existing_indexes = [idx["name"] for idx in pc.list_indexes().get("indexes", [])]
if INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"🆕 Created Pinecone index: {INDEX_NAME}")
else:
    print(f"✅ Using existing index: {INDEX_NAME}")


# Read PDF/txt documents
documents = []
for fname in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, fname)
    if fname.lower().endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            print ('skipping txt files')
            #documents.append(f.read())
    elif fname.lower().endswith(".pdf"):
        reader = PdfReader(path)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        documents.append(text)

# Split text into chunks
# uses LangChain’s text splitter to chunk documents.
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = [chunk for doc in documents for chunk in splitter.split_text(doc)]

# Create embeddings (using Bedrock)
#embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")
# uses LangChain’s BedrockEmbeddings wrapper to call Amazon Bedrock API.
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", region_name="us-east-1")

# Connect to index
# ✅ Get handle to the index for upsert/query
index = pc.Index(INDEX_NAME)

# not using LangChain’s Pinecone wrapper, you're using Pinecone Python SDK directly.
# Embed and upsert
vectors = []
for i, text in enumerate(texts):
    vec = embeddings.embed_query(text)
    vectors.append({"id": f"chunk-{i}", "values": vec, "metadata": {"text": text}})

index.upsert(vectors=vectors)
print(f"✅ Ingested {len(vectors)} chunks into Pinecone index '{INDEX_NAME}'")

"""
LangChain VectorStore Wrapper (Pinecone) Not Used.
Commening langchain wrapper around pinecone as it is incompatible still uses old pinecone client
# ✅ Store embeddings in Pinecone using LangChain wrapper
store = LangchainPineconeStore.from_texts(
    texts=texts,
    embedding=embeddings,
    index_name=INDEX_NAME
)
"""


print(f"✅ Ingested {len(texts)} text chunks into Pinecone index '{INDEX_NAME}'")

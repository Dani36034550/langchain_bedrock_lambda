import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import BedrockEmbeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import Any, List


class PineconeRetriever(BaseRetriever):
    store: Any
    k: int = 3

    def get_relevant_documents(self, query: str) -> List[Document]:
        matches = self.store.query(query, top_k=self.k)
        docs = [
            Document(page_content=m.metadata.get("text", "")) 
            for m in matches
        ]
        return docs

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return self.get_relevant_documents(query)

# Constants
INDEX_NAME = "langchain-bedrock-index"

def get_vectorstore():
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY env var not set")

    pc = Pinecone(api_key=api_key)

    # Create index if needed
    if INDEX_NAME not in [idx.name for idx in pc.list_indexes()]:
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")

    # ✅ Return direct Pinecone wrapper instead of LangChain wrapper
    return get_pinecone_store(pc, embeddings)


def get_pinecone_store(pc, embeddings):
    index = pc.Index(INDEX_NAME)

    class PineconeStore:
        def __init__(self, index, embed_fn):
            self.index = index
            self.embed_fn = embed_fn

        def upsert(self, texts):
            vectors = []
            for i, text in enumerate(texts):
                vec = self.embed_fn(text)  # embeddings.embed_query(text)
                vectors.append({
                    "id": f"chunk-{i}",
                    "values": vec,
                    "metadata": {"text": text}
                })
            self.index.upsert(vectors=vectors)
            return len(vectors)

        def query(self, query_text, top_k=5):
            query_vec = self.embed_fn(query_text)
            results = self.index.query(
                vector=query_vec,
                top_k=top_k,
                include_metadata=True
            )
            return results.matches
        
        def as_retriever(self, search_kwargs={"k": 3}):
            return PineconeRetriever(store=self, k=search_kwargs.get("k", 3))


    return PineconeStore(index, embeddings.embed_query)

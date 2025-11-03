from langchain.chains import RetrievalQA
from langchain_aws import BedrockLLM
from vectorstore_service import get_vectorstore
from bedrock_client import get_bedrock_client
from langchain_aws import ChatBedrock


def build_chain():
    # Claude-2.1 work with BedrockLLM
    # llm = BedrockLLM(
    #     client=get_bedrock_client(),
    #     model_id="anthropic.claude-v2:1"
    # )

    # Claude-3 work with ChatBedrock
    llm = ChatBedrock(
        client=get_bedrock_client(),
        model_id="anthropic.claude-3-sonnet-20240229-v1:0"
    )
    
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 3})
    
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    return chain
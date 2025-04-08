# scripts/query.py
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.chains import RetrievalQA
from config import *
from langchain_community.vectorstores import AzureSearch
from config import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    query = input("请输入你想鉴别的话（如：转发这条视频能辟邪）：\n> ")

    embeddings = AzureOpenAIEmbeddings(
        model=EMBEDDING_DEPLOYMENT_NAME,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        openai_api_version=EMBEDDING_API_VERSION,
    )

    vectorstore = AzureSearch(
        azure_search_endpoint=AZURE_SEARCH_ENDPOINT,
        azure_search_key=AZURE_SEARCH_API_KEY,
        index_name=AZURE_SEARCH_INDEX_NAME,
        embedding_function=embeddings,
    )

    retriever = vectorstore.as_retriever(search_type="similarity", k=3)


    logger.info("🧠 Initializing GPT model...")
    llm = AzureChatOpenAI(
        azure_deployment="gpt-4",
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-12-01-preview"
    )

    logger.info("🔗 Building RetrievalQA chain...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,  # Use retrieved docs directly
        chain_type="stuff",
        return_source_documents=True
    )

    result = qa_chain.invoke({"query": query})
    logger.info("📢 回答：")
    logger.info(result["result"])

if __name__ == "__main__":
    main()

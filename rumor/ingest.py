from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import AzureOpenAIEmbeddings
# from azure.search.documents.indexes import SearchIndexClient
# from azure.search.documents import SearchClient
# from azure.ai.projects import AIProjectClient
# from azure.ai.projects.models import ConnectionType
# from azure.identity import DefaultAzureCredential
# from azure.core.credentials import AzureKeyCredential
from langchain_community.vectorstores.azuresearch import AzureSearch
from config import *
import os

DATA_DIR = "data/articles"


def load_documents():
    docs = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_DIR, filename)
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())
    return docs

def main():
    print("📄 Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.")

    print("✂️ Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    print("🧠 Embedding and indexing...")
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
        embedding_function=embeddings.embed_query,
    )

    print("📦 Uploading documents to Azure Search...")
    ids = vectorstore.add_documents(docs)

    print(f"🆔 Uploaded document IDs: {ids}")
    print("✅ Done! Indexed into Azure Cognitive Search.")

if __name__ == "__main__":
    main()

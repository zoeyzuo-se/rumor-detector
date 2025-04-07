from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from config import *
import os

DATA_DIR = "data/articles"


def load_documents():
    docs = []
    print(f"Checking files in directory: {DATA_DIR}")
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_DIR, filename)
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())
    return docs

def load_article(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

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

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")
    print("✅ FAISS index created and saved!")

if __name__ == "__main__":
    main()

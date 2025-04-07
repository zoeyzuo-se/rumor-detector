# scripts/query.py
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from config import *

def main():
    # 用户输入内容
    query = input("请输入你想鉴别的话（如：转发这条视频能辟邪）：\n> ")

    # 嵌入模型
    embeddings = AzureOpenAIEmbeddings(
        model=EMBEDDING_DEPLOYMENT_NAME,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        openai_api_version=EMBEDDING_API_VERSION,
    )

    # 加载 FAISS 向量库
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # 初始化 GPT 模型
    llm = AzureChatOpenAI(
        azure_deployment="gpt-4",  # 部署的 GPT 模型名字
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-12-01-preview"
    )

    # 构建问答链
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        return_source_documents=True
    )

    # 执行查询
    result = qa_chain.invoke({"query": query})
    print("\n📢 回答：")
    print(result["result"])

    # print("\n📚 参考内容片段：")
    # for doc in result["source_documents"]:
    #     print(f"---\n{doc.page_content.strip()}")

if __name__ == "__main__":
    main()

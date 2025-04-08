# 🧠 WeChat Rumor Detector | 微信视频号谣言识别系统

A Retrieval-Augmented Generation (RAG) system to identify and debunk misinformation or superstition from WeChat Video Channel content.

一个结合 RAG 技术的系统，旨在识别和澄清来自微信视频号的谣言与迷信信息。



## 🚀 Project Overview | 项目简介

This project builds an intelligent system that:
- Retrieves fact-checking content from trusted WeChat official accounts
- Answers user questions about misinformation using Azure OpenAI
- Supports automatic content ingestion and search

本项目的目标是构建一个智能问答系统，能够：
- 检索权威公众号中的辟谣内容
- 利用 Azure OpenAI 回答用户提出的疑问
- 支持自动采集、处理和检索内容


## 🧱 Architecture | 系统架构

- A[User Query 用户提问] --> B[Retriever 向量检索]

- B --> C[Related Articles 匹配文章]

- C --> D[LLM (GPT) 生成回答]

- D --> E[Final Answer + Sources 答案 + 来源]



## 📦 Features | 功能亮点

✅ Built-in Chinese vector search (text-embedding-ada-002) | 内置中文向量搜索（使用 text-embedding-ada-002）

✅ Automatic article crawling and cleaning | 自动抓取公众号文章并清洗 (TODO)

✅ Store and search using Azure Cognitive Search | 使用 Azure Cognitive Search 构建向量索引

✅ Answer with GPT-4 | 基于 GPT-4 的问答系统

## 🔧 Tech Stack | 技术栈

- [Azure OpenAI](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/)
- [Azure Cognitive Search](https://azure.microsoft.com/en-us/products/search/)
- [LangChain](https://python.langchain.com/)
- Python
- Poetry

### Installation | 安装

```bash
pip install poetry
poetry install
poetry shell
poetry run python ingest.py  # will turn data from data/articles into vectors and upload them into azure cognitive search
poetry run python query.py # will query the azure cognitive search and return the result based on the user input
```

### Environment Variables | 环境变量

```python
AZURE_OPENAI_API_KEY = ""
AZURE_OPENAI_ENDPOINT = "https://rumor-openai.openai.azure.com/"
EMBEDDING_DEPLOYMENT_NAME = "text-embedding-ada-002"
EMBEDDING_API_VERSION = "2023-12-01-preview"
AZURE_SEARCH_ENDPOINT = "https://rumor-ai-search.search.windows.net"
AZURE_SEARCH_API_KEY = ""
AZURE_SEARCH_INDEX_NAME = "your-index-name"
```

### Roadmap | 后续计划
- [ ] Batch ingest multiple articles 批量抓取公众号文章
- [ ] Speech-to-text rumor detection 支持语音内容分析
- [ ] Video rumor detection 支持视频内容分析
- [ ] Made an API for the system 提供系统 API 接口
- [ ] Add a web UI for the system 提供系统 Web 界面
- [ ] Provide metadata for the searched articles 提供搜索文章的元数据


## 👩‍💻 Author | 作者
Created by @Yuru Zuo
开发者：[@YuruZuo]，记录软件工程师的副业与求职故事。

欢迎关注更新，也欢迎反馈建议 ✨
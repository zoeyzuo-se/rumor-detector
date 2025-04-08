from asyncio.log import logger
import requests
from bs4 import BeautifulSoup
import re
import os
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_wechat_article(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    logger.info(f"Fetching article from {url}...")
    res = requests.get(url, headers=headers)
    logger.info(f"Response status code: {res.status_code}")
    res.encoding = 'utf-8'
    logger.info(res.text)

    soup = BeautifulSoup(res.text, 'html.parser')
    content_div = soup.find('div', class_='rich_media_content')
    if not content_div:
        return ""

    # 提取纯文本
    text = content_div.get_text(separator='\n', strip=True)
    return text

def clean_text(text: str) -> str:
    # 删除多余换行、广告、来源等
    text = re.sub(r'（来源：.*?）', '', text)
    text = re.sub(r'点击.*阅读全文.*', '', text)
    text = re.sub(r'微信公众号.*', '', text)
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

def save_article(text: str, url: str, output_dir="data/articles"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Using URL hash as filename to avoid duplication
    filename = hashlib.md5(url.encode('utf-8')).hexdigest() + ".txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ Article saved to {filepath}")

if __name__ == "__main__":
    url = input("Please input article url:")
    article_text = extract_wechat_article(url)
    if not article_text:
        print("❌ Could not extract article content.")
    else:
        cleaned_text = clean_text(article_text)
        save_article(cleaned_text, url)
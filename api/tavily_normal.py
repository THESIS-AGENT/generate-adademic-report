# To install: pip install tavily-python
import json
import logging
import time
from typing import Dict, Any, List, Optional
import requests
from tavily import TavilyClient
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 从环境变量获取API密钥
tavily_api_key = os.getenv('TAVILY_API_KEY')

# 初始化Tavily客户端
client = TavilyClient(tavily_api_key) if tavily_api_key else None

def query_zhihu(prompt, N):
    client = TavilyClient(tavily_api_key)
    response = client.search(
        query=prompt,
        search_depth="advanced",
        max_results=N,
        time_range="year",
        include_answer="advanced",
        include_domains=["zhihu.com"]
    )
    return [r["url"] for r in response["results"]]
        
if __name__ == "__main__":
    pass
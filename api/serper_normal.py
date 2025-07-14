import http.client
import json
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 从环境变量获取API密钥
serper_api_key = os.getenv('SERPER_API_KEY')

def query_singleWebsite(url, includeMarkdown=True):
        """
        输入url
        """
        conn = http.client.HTTPSConnection("scrape.serper.dev")
        payload = json.dumps({
        "url": url,
        "includeMarkdown": includeMarkdown
        })
        headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/", payload, headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data)
        return json_data

if __name__ == "__main__":
    pass
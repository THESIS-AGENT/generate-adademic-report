from tqdm import tqdm
import time
from api.tavily_normal import query_zhihu
from api.serper_normal import query_singleWebsite

def search_zhihu(keywordsList, K):
    # 查询知乎
    zhihu_list = []
    for keyword in tqdm(keywordsList):
        # 添加3次重试
        retry_count = 0
        zhihu_linksList = []
        while retry_count < 3:
            try:
                zhihu_linksList = query_zhihu(keyword, K)
                break
            except Exception as e:
                retry_count += 1
                if retry_count < 3:
                    time.sleep(5)
                else:
                    print(f"Failed to query_zhihu after 3 retries: {e}")
        
        for zhihu_link in zhihu_linksList:
            # 添加3次重试
            retry_count = 0
            tmp_page = {}
            while retry_count < 3:
                try:
                    tmp_page = query_singleWebsite(zhihu_link)
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count < 3:
                        time.sleep(5)
                    else:
                        print(f"Failed to query_singleWebsite after 3 retries: {e}")
            
            if tmp_page and "markdown" in tmp_page:
                tmp_markdown = tmp_page["markdown"]
                # 不清洗, 直接拿来用.
                if tmp_markdown != "# 安全验证\n\n## 进入知乎\n\n系统监测到您的网络环境存在异常，为保证您的正常访问，请点击下方验证按钮进行验证。在您验证完成前，该提示将多次出现。":
                    zhihu_list.append({"keyword": keyword, "zhihu_link": zhihu_link, "content": tmp_markdown})
    return zhihu_list
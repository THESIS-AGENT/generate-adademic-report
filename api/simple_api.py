import json
import time
import logging
from typing import Optional
import requests
import openai
import google.generativeai as genai
import anthropic
import dashscope
import os
from typing import Dict, Any, Optional

# 从环境变量获取API密钥
openai_api_key = os.getenv('OPENAI_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')
claude_api_key = os.getenv('CLAUDE_API_KEY')
ali_bailian_api_key = os.getenv('ALI_BAILIAN_API_KEY')
siliconflow_api_key = os.getenv('SILICONFLOW_API_KEY')
deerapi_api_key = os.getenv('DEERAPI_API_KEY')

logger = logging.getLogger('simple_api')

class SimpleAPIClient:
    """简化的API调用客户端"""
    
    def __init__(self, max_retries: int = 3, retry_delay: int = 5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def call_openai(self, prompt: str, model: str = "gpt-3.5-turbo", timeout: int = 60) -> str:
        """调用OpenAI API"""
        try:
            client = openai.OpenAI(api_key=openai_api_key)
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                timeout=timeout
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API调用失败: {str(e)}")
            raise
    
    def call_gemini(self, prompt: str, model: str = "gemini-1.5-flash", timeout: int = 60) -> str:
        """调用Google Gemini API"""
        try:
            genai.configure(api_key=gemini_api_key)
            model_instance = genai.GenerativeModel(model)
            
            response = model_instance.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API调用失败: {str(e)}")
            raise
    
    def call_claude(self, prompt: str, model: str = "claude-3-sonnet-20240229", timeout: int = 60) -> str:
        """调用Claude API"""
        try:
            client = anthropic.Anthropic(api_key=claude_api_key)
            
            response = client.messages.create(
                model=model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API调用失败: {str(e)}")
            raise
    
    def call_qwen(self, prompt: str, timeout: int = 60) -> str:
        """调用阿里通义千问API"""
        try:
            dashscope.api_key = ali_bailian_api_key
            
            response = dashscope.Generation.call(
                model='qwen-max',
                prompt=prompt,
                result_format='message'
            )
            
            if response.status_code == 200:
                return response.output.choices[0].message.content
            else:
                raise Exception(f"Qwen API调用失败: {response.message}")
        except Exception as e:
            logger.error(f"Qwen API调用失败: {str(e)}")
            raise
    
    def call_siliconflow(self, prompt: str, model: str = "Qwen/Qwen2.5-7B-Instruct", timeout: int = 60) -> str:
        """调用SiliconFlow API"""
        try:
            url = "https://api.siliconflow.cn/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {siliconflow_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4000,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"SiliconFlow API调用失败: {str(e)}")
            raise
    
    def generate_with_fallback(self, prompt: str, timeout: int = 60) -> str:
        """
        使用备用策略生成内容
        
        Args:
            prompt (str): 输入提示
            timeout (int): 超时时间
            
        Returns:
            str: 生成的内容
        """
        # 按优先级尝试不同的API
        api_methods = [
            ("Gemini", lambda: self.call_gemini(prompt, timeout=timeout)),
            ("OpenAI", lambda: self.call_openai(prompt, timeout=timeout)),
            ("SiliconFlow", lambda: self.call_siliconflow(prompt, timeout=timeout)),
            ("Qwen", lambda: self.call_qwen(prompt, timeout=timeout)),
            ("Claude", lambda: self.call_claude(prompt, timeout=timeout))
        ]
        
        last_error = None
        
        for retry in range(self.max_retries):
            for api_name, api_method in api_methods:
                try:
                    logger.info(f"尝试使用 {api_name} API (重试 {retry + 1}/{self.max_retries})")
                    result = api_method()
                    
                    if result and result.strip():
                        logger.info(f"成功使用 {api_name} API 获取响应")
                        return result.strip()
                        
                except Exception as e:
                    last_error = e
                    logger.warning(f"{api_name} API 调用失败: {str(e)}")
                    continue
            
            if retry < self.max_retries - 1:
                logger.info(f"等待 {self.retry_delay} 秒后重试...")
                time.sleep(self.retry_delay)
        
        raise Exception(f"所有API调用都失败了。最后一个错误: {str(last_error)}")

# 创建全局客户端实例
api_client = SimpleAPIClient()

def call_llm(prompt: str, model_name: str = "auto", timeout: int = 60) -> str:
    """
    调用大语言模型
    
    Args:
        prompt (str): 输入提示
        model_name (str): 模型名称，支持 "auto", "gemini", "openai", "claude", "qwen", "siliconflow"
        timeout (int): 超时时间
        
    Returns:
        str: 生成的内容
    """
    if model_name == "auto":
        return api_client.generate_with_fallback(prompt, timeout)
    elif model_name == "gemini":
        return api_client.call_gemini(prompt, timeout=timeout)
    elif model_name == "openai":
        return api_client.call_openai(prompt, timeout=timeout)
    elif model_name == "claude":
        return api_client.call_claude(prompt, timeout=timeout)
    elif model_name == "qwen":
        return api_client.call_qwen(prompt, timeout=timeout)
    elif model_name == "siliconflow":
        return api_client.call_siliconflow(prompt, timeout=timeout)
    else:
        logger.warning(f"未知的模型名称: {model_name}，使用自动备用策略")
        return api_client.generate_with_fallback(prompt, timeout) 
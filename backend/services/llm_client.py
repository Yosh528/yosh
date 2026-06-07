"""
Minimax API 客户端封装模块
用于调用 Minimax 大模型 API 进行剧本生成

依赖：
- requests: HTTP请求库
- python-dotenv: 环境变量管理

配置：
- MINIMAX_API_KEY: API密钥（必需）
- MINIMAX_BASE_URL: API基础URL（可选）
- MINIMAX_MODEL: 模型名称（可选）
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMServiceError(Exception):
    """大模型服务异常"""
    pass

class MinimaxClient:
    def __init__(self):
        self.api_key = os.getenv('MINIMAX_API_KEY')
        self.base_url = os.getenv('MINIMAX_BASE_URL', 'https://api.minimax.chat/v1/text/chatcompletion')
        self.model = os.getenv('MINIMAX_MODEL', 'abab5.5-chat')
        
        if not self.api_key:
            raise LLMServiceError("MINIMAX_API_KEY 未配置")
    
    def call_api(self, prompt: str, max_tokens: int = 8192, temperature: float = 0.7) -> str:
        """调用Minimax大模型API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Minimax API 特定格式
        payload = {
            'model': self.model,
            'tokens_to_generate': max_tokens,
            'temperature': temperature,
            'messages': [
                {
                    'sender_type': 'USER',
                    'text': prompt
                }
            ],
            'bot_setting': [
                {
                    'bot_name': '剧本生成助手',
                    'content': '你是一个专业的剧本创作助手，负责将小说文本转换为结构化的剧本格式。请根据用户提供的文本生成专业的剧本内容。'
                }
            ]
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 检查API错误
            if result.get('base_resp', {}).get('status_code') != 0:
                error_msg = result.get('base_resp', {}).get('status_msg', '未知错误')
                raise LLMServiceError(f"Minimax API错误: {error_msg}")
            
            # 提取回复内容 - Minimax返回格式
            reply = result.get('reply', '')
            if not reply:
                # 尝试从choices提取
                choices = result.get('choices', [])
                if choices and len(choices) > 0:
                    reply = choices[0].get('text', '')
                else:
                    raise LLMServiceError("大模型返回内容为空")
            
            return reply
            
        except requests.exceptions.RequestException as e:
            raise LLMServiceError(f"大模型调用失败: {str(e)}")
        except (KeyError, ValueError) as e:
            raise LLMServiceError(f"大模型返回格式异常: {str(e)}")
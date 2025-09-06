"""
LLM (Large Language Model) API クライアント

Claude API経由でコードレビューや設計支援を行う
"""

import json
import requests
import time
from typing import Dict, Any, Optional, List
from loguru import logger


class LLMClient:
    """LLM APIクライアント"""
    
    def __init__(self, config: Dict[str, Any]):
        self.provider = config.get("provider", "claude")
        self.api_key = config.get("api_key", "")
        self.model = config.get("model", "claude-3-sonnet-20240229")
        self.max_tokens = config.get("max_tokens", 8000)
        self.temperature = config.get("temperature", 0.1)
        self.timeout = config.get("timeout", 60)
        
        # Claude API設定
        if self.provider == "claude":
            self.api_endpoint = "https://api.anthropic.com/v1/messages"
            self.headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
        else:
            raise ValueError(f"未対応のLLMプロバイダー: {self.provider}")
            
    def _make_claude_request(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Claude API リクエストを実行"""
        
        # messagesをClaudeの形式に変換
        if messages and messages[0].get("role") == "system":
            system_message = messages[0]["content"]
            user_messages = messages[1:]
        else:
            system_message = "あなたは優秀なコードレビューアーです。"
            user_messages = messages
            
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "system": system_message,
            "messages": [
                {
                    "role": msg["role"],
                    "content": msg["content"]
                } for msg in user_messages
            ]
        }
        
        try:
            logger.info("Claude API リクエスト送信")
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("content", [])
                
                if content and isinstance(content, list) and len(content) > 0:
                    text_content = content[0].get("text", "")
                    if text_content:
                        logger.success(f"Claude API 成功: {len(text_content)} 文字")
                        return text_content
                        
                logger.warning("Claude API: 空のレスポンス")
                
            else:
                error_detail = ""
                try:
                    error_data = response.json()
                    error_detail = error_data.get("error", {}).get("message", "")
                except:
                    error_detail = response.text
                    
                logger.error(f"Claude API エラー: {response.status_code} - {error_detail}")
                
        except requests.exceptions.Timeout:
            logger.warning("Claude API タイムアウト")
            
        except requests.exceptions.ConnectionError:
            logger.error("Claude API 接続エラー: インターネット接続を確認してください")
            
        except Exception as e:
            logger.error(f"Claude API 予期しないエラー: {e}")
            
        return None
        
    def review_code(self, prompt: str) -> Optional[str]:
        """コードレビュー"""
        messages = [
            {
                "role": "system",
                "content": (
                    "あなたは経験豊富なシニアエンジニアです。"
                    "コードの品質、セキュリティ、パフォーマンス、保守性の観点から"
                    "建設的で具体的なレビューを提供してください。"
                    "日本語で回答してください。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        logger.info("コードレビューリクエスト開始")
        return self._make_claude_request(messages)
        
    def generate_instruction(self, requirement: str) -> Optional[str]:
        """命令書生成支援"""
        messages = [
            {
                "role": "system",
                "content": (
                    "あなたは技術要件を詳細な実装命令書に変換するスペシャリストです。"
                    "SLMが理解しやすい、明確で具体的な実装指示を生成してください。"
                )
            },
            {
                "role": "user", 
                "content": f"""
以下の要件から、DeepSeek-Coderが実装できる詳細な命令書を生成してください：

要件：
{requirement}

命令書には以下を含めてください：
- 関数/クラス名
- 入力パラメータの詳細仕様
- 出力仕様
- エラーハンドリング方法
- バリデーションルール
- テストケース例
- 実装上の注意点

JSON形式で構造化して返してください。
"""
            }
        ]
        
        logger.info("命令書生成リクエスト開始") 
        return self._make_claude_request(messages)
        
    def optimize_code(self, code: str, optimization_type: str = "general") -> Optional[str]:
        """コード最適化"""
        optimization_focus = {
            "general": "全般的な品質向上",
            "performance": "パフォーマンス最適化",
            "security": "セキュリティ強化",
            "readability": "可読性向上",
            "maintainability": "保守性向上"
        }
        
        focus = optimization_focus.get(optimization_type, optimization_focus["general"])
        
        messages = [
            {
                "role": "system",
                "content": (
                    f"あなたは{focus}の専門家です。"
                    "提供されたコードを改善して、最適化されたバージョンを提供してください。"
                    "変更点と改善理由も説明してください。"
                )
            },
            {
                "role": "user",
                "content": f"""
以下のコードを{focus}の観点から最適化してください：

```python
{code}
```

回答形式：
1. 最適化されたコード
2. 主な変更点
3. 改善理由
4. 追加の推奨事項（あれば）
"""
            }
        ]
        
        logger.info(f"コード最適化リクエスト開始 ({optimization_type})")
        return self._make_claude_request(messages)
        
    def test_connection(self) -> bool:
        """API接続テスト"""
        messages = [
            {
                "role": "user",
                "content": "Hello! Please respond with 'Connection successful' in Japanese."
            }
        ]
        
        logger.info("Claude API 接続テスト開始")
        result = self._make_claude_request(messages)
        
        if result and ("成功" in result or "successful" in result):
            logger.success("Claude API 接続テスト成功")
            return True
        else:
            logger.error("Claude API 接続テスト失敗")
            return False
            
    def get_api_info(self) -> Dict[str, Any]:
        """API情報を取得"""
        return {
            "provider": self.provider,
            "model": self.model,
            "api_endpoint": self.api_endpoint,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "has_api_key": bool(self.api_key and len(self.api_key) > 10)
        }
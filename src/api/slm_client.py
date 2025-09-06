"""
SLM (Small Language Model) API クライアント

LM Studio ローカルAPI経由でDeepSeek-Coderとの通信を行う
"""

import json
import random
import requests
import time
from typing import Dict, Any, Optional, List
from loguru import logger


class SLMClient:
    """SLM APIクライアント"""
    
    def __init__(self, config: Dict[str, Any]):
        self.api_endpoint = config["api_endpoint"]
        self.model = config["model"]
        self.max_tokens = config.get("max_tokens", 2000)
        self.temperature = config.get("temperature", 0.2)
        self.timeout = config.get("timeout", 30)
        self.retry_attempts = config.get("retry_attempts", 3)
        
    def _make_request(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """API リクエストを実行（改良版タイムアウト・再接続機能付き）"""
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": False
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        for attempt in range(self.retry_attempts):
            try:
                logger.info(f"SLM API リクエスト送信 (試行 {attempt + 1}/{self.retry_attempts})")
                
                # プログレッシブタイムアウト：試行回数に応じてタイムアウトを延長
                current_timeout = self.timeout + (attempt * 30)  # 30秒ずつ延長
                logger.info(f"タイムアウト設定: {current_timeout}秒")
                
                response = requests.post(
                    self.api_endpoint,
                    json=payload,
                    headers=headers,
                    timeout=current_timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    if content:
                        logger.success(f"SLM API 成功: {len(content)} 文字")
                        return content
                    else:
                        logger.warning("SLM API: 空のレスポンス")
                        
                else:
                    logger.error(f"SLM API エラー: {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"SLM API タイムアウト (試行 {attempt + 1}) - {current_timeout}秒経過")
                logger.info("コンテキスト長が原因の可能性があります。再試行します...")
                
            except requests.exceptions.ConnectionError as e:
                logger.error(f"SLM API 接続エラー: {self.api_endpoint} に接続できません")
                logger.info("LM Studio の状態を確認しています...")
                
                # 接続復旧の試行
                if self._check_connection_health():
                    logger.info("LM Studio への接続が復旧しました")
                else:
                    logger.warning("LM Studio が応答しません。手動確認が必要です")
                
            except Exception as e:
                logger.error(f"SLM API 予期しないエラー: {e}")
                
            # リトライ前の待機（指数バックオフ + ジッター）
            if attempt < self.retry_attempts - 1:
                base_wait = (attempt + 1) * 5  # 5秒ベース
                jitter = random.uniform(0, 2)  # 0-2秒のランダム要素
                wait_time = base_wait + jitter
                
                logger.info(f"{wait_time:.1f}秒待機してリトライします...")
                time.sleep(wait_time)
                
        logger.error("SLM API: 全ての再試行が失敗しました")
        return None

        
    def _check_connection_health(self) -> bool:
        """LM Studio接続のヘルスチェック"""
        try:
            # LM Studioのモデルエンドポイントで簡易チェック
            models_endpoint = self.api_endpoint.replace('/chat/completions', '/models')
            response = requests.get(models_endpoint, timeout=5)
            
            if response.status_code == 200:
                logger.info("LM Studio ヘルスチェック: 正常")
                return True
            else:
                logger.warning(f"LM Studio ヘルスチェック: 応答異常 {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            logger.warning("LM Studio ヘルスチェック: タイムアウト")
            return False
            
        except requests.exceptions.ConnectionError:
            logger.warning("LM Studio ヘルスチェック: 接続不可")
            return False
            
        except Exception as e:
            logger.warning(f"LM Studio ヘルスチェック: エラー {e}")
            return False

    def _is_context_overflow_error(self, error_response: str) -> bool:
        """コンテキストオーバーフローエラーかどうかを判定"""
        overflow_indicators = [
            "context the overflows",
            "context length of only",
            "provide a shorter input",
            "larger context length"
        ]
        return any(indicator in error_response for indicator in overflow_indicators)
    
    def _extract_token_info(self, error_response: str) -> tuple[int, int]:
        """エラーメッセージからトークン情報を抽出"""
        import re
        
        # "Trying to keep the first 5621 tokens when context the overflows. However, the model is loaded with context length of only 4164 tokens"
        required_match = re.search(r'first (\d+) tokens', error_response)
        available_match = re.search(r'context length of only (\d+) tokens', error_response)
        
        required_tokens = int(required_match.group(1)) if required_match else 0
        available_tokens = int(available_match.group(1)) if available_match else self.max_tokens
        
        return required_tokens, available_tokens
    
    def _chunk_prompt(self, prompt: str, chunk_size_ratio: float = 0.8) -> List[str]:
        """プロンプトをチャンクに分割"""
        lines = prompt.split('\n')
        total_lines = len(lines)
        chunk_size = max(1, int(total_lines * chunk_size_ratio))
        
        chunks = []
        for i in range(0, total_lines, chunk_size):
            chunk_lines = lines[i:i + chunk_size]
            chunks.append('\n'.join(chunk_lines))
        
        logger.info(f"プロンプトを{len(chunks)}個のチャンクに分割（チャンクあたり約{chunk_size}行）")
        return chunks
    
    def _merge_code_responses(self, responses: List[str]) -> str:
        """複数のコードレスポンスをマージ"""
        merged_code = []
        
        for i, response in enumerate(responses):
            logger.info(f"チャンク{i+1}のレスポンス処理中...")
            code = self._extract_code(response)
            
            if code.strip():
                if i == 0:
                    # 最初のチャンク：ヘッダーコメントとimport文を含める
                    merged_code.append(f"# === チャンク {i+1} ===")
                    merged_code.append(code)
                else:
                    # 後続のチャンク：継続処理として追加
                    merged_code.append(f"\n# === チャンク {i+1} 継続 ===")
                    # import文を除外して関数・クラス定義のみを追加
                    code_lines = code.split('\n')
                    filtered_lines = [line for line in code_lines 
                                    if not (line.strip().startswith('import ') or 
                                           line.strip().startswith('from '))]
                    merged_code.append('\n'.join(filtered_lines))
        
        final_code = '\n'.join(merged_code)
        logger.success(f"コードマージ完了: {len(final_code)}文字")
        return final_code
    
    def generate_code_with_chunking(self, prompt: str) -> Optional[str]:
        """チャンク分割対応のコード生成"""
        messages = [
            {
                "role": "system",
                "content": (
                    "あなたは優秀なプログラマーです。"
                    "仕様に従って高品質なPythonコードを生成してください。"
                    "コードのみを返し、不要な説明は含めないでください。"
                    "複数回に分けて処理される場合、各部分が独立して実行可能なコードにしてください。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        logger.info("チャンク分割対応コード生成開始")
        
        # 最初の試行
        first_response = self._make_request(messages)
        if first_response:
            logger.success("一括処理でコード生成成功")
            return self._extract_code(first_response)
        
        # コンテキストオーバーフローの場合、チャンク分割処理
        logger.warning("一括処理失敗。チャンク分割処理を開始します...")
        
        # プロンプトを分割
        chunks = self._chunk_prompt(prompt, chunk_size_ratio=0.6)  # 60%サイズで分割
        responses = []
        
        for i, chunk in enumerate(chunks):
            chunk_messages = [
                {
                    "role": "system", 
                    "content": (
                        "あなたは優秀なプログラマーです。"
                        f"大規模な仕様の一部（{i+1}/{len(chunks)}）を処理しています。"
                        "この部分に関連する実装可能なPythonコードを生成してください。"
                        "コードのみを返し、不要な説明は含めないでください。"
                    )
                },
                {
                    "role": "user",
                    "content": f"以下の仕様の一部を実装してください（パート{i+1}/{len(chunks)}）:\n\n{chunk}"
                }
            ]
            
            logger.info(f"チャンク {i+1}/{len(chunks)} 処理中...")
            chunk_response = self._make_request(chunk_messages)
            
            if chunk_response:
                responses.append(chunk_response)
                logger.success(f"チャンク {i+1} 処理完了")
            else:
                logger.error(f"チャンク {i+1} 処理失敗")
                return None
        
        # レスポンスをマージ
        if responses:
            return self._merge_code_responses(responses)
        
        return None
        
    def generate_code(self, prompt: str) -> Optional[str]:
        """コード生成（コンテキストオーバーフロー自動対応）"""
        messages = [
            {
                "role": "system",
                "content": (
                    "あなたは優秀なプログラマーです。"
                    "仕様に従って高品質なPythonコードを生成してください。"
                    "コードのみを返し、不要な説明は含めないでください。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        logger.info("コード生成リクエスト開始")
        result = self._make_request(messages)
        
        if result:
            # 通常の処理成功
            code = self._extract_code(result)
            return code
        
        # 失敗した場合、コンテキストオーバーフローかチェック
        logger.warning("通常のコード生成が失敗。チャンク分割処理を試行します...")
        return self.generate_code_with_chunking(prompt)
        
    def _extract_code(self, response: str) -> str:
        """レスポンスからコードを抽出"""
        # Markdown コードブロックを削除
        lines = response.strip().split('\n')
        
        # ```python または ``` で始まる行を見つけて削除
        start_idx = 0
        end_idx = len(lines)
        
        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                if start_idx == 0:
                    start_idx = i + 1
                else:
                    end_idx = i
                    break
                    
        code_lines = lines[start_idx:end_idx]
        return '\n'.join(code_lines).strip()
        
    def test_connection(self) -> bool:
        """API接続テスト"""
        test_prompt = "print('Hello, World!')"
        messages = [
            {
                "role": "user",
                "content": f"次のPythonコードを実行可能な形で返してください: {test_prompt}"
            }
        ]
        
        logger.info("SLM API 接続テスト開始")
        result = self._make_request(messages)
        
        if result and "Hello" in result:
            logger.success("SLM API 接続テスト成功")
            return True
        else:
            logger.error("SLM API 接続テスト失敗")
            return False
            
    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """モデル情報を取得"""
        try:
            # LM Studio の models エンドポイントを試す
            models_endpoint = self.api_endpoint.replace('/chat/completions', '/models')
            response = requests.get(models_endpoint, timeout=10)
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            logger.warning(f"モデル情報取得失敗: {e}")
            
        return {
            "configured_model": self.model,
            "endpoint": self.api_endpoint,
            "status": "configured"
        }
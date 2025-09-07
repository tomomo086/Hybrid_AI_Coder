#!/usr/bin/env python3
"""
Simple Hybrid Pair Programming System
シンプルハイブリッドペアプログラミングシステム

ClaudeCode + DeepSeek の協調開発システム（超簡略版）
- ClaudeCode: 設計・分析・レビュー（手動）
- DeepSeek: 実装・コード生成（自動）
"""

import json
import os
import requests
import uuid
import datetime
from pathlib import Path
from typing import Dict, List, Optional

class SimpleHybridPair:
    def __init__(self, config_file="simple_config.json"):
        """シンプルハイブリッドペア初期化"""
        self.config_file = config_file
        self.results_dir = Path("simple_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # 設定読み込み
        self.config = self.load_config()
        
        # タスク保存用
        self.tasks_file = "simple_tasks.json"
        self.tasks = self.load_tasks()
    
    def load_config(self) -> Dict:
        """設定ファイル読み込み（なければデフォルト作成）"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # デフォルト設定作成
            default_config = {
                "deepseek_api": {
                    "endpoint": "http://localhost:1234/v1/chat/completions",
                    "model": "deepseek-coder-6.7b-instruct",
                    "temperature": 0.2,
                    "max_tokens": 2000
                }
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            print(f"設定ファイル {self.config_file} を作成しました")
            return default_config
    
    def load_tasks(self) -> List[Dict]:
        """タスク一覧読み込み"""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_tasks(self):
        """タスク一覧保存"""
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)
    
    def create_task(self, title: str, description: str) -> str:
        """新規タスク作成"""
        task_id = str(uuid.uuid4())[:8]
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "status": "created",
            "created_at": datetime.datetime.now().isoformat(),
            "approved": False
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"タスク作成完了: {task_id} - {title}")
        return task_id
    
    def list_tasks(self):
        """タスク一覧表示"""
        if not self.tasks:
            print("タスクはありません")
            return
        
        print("\n=== タスク一覧 ===")
        for task in self.tasks:
            status = "✅承認済み" if task["approved"] else "⏳未承認"
            print(f"ID: {task['id']} | {status} | {task['title']}")
            print(f"    説明: {task['description']}")
            print(f"    作成: {task['created_at'][:16]}")
            print()
    
    def approve_task(self, task_id: str) -> bool:
        """タスク承認"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["approved"] = True
                task["approved_at"] = datetime.datetime.now().isoformat()
                self.save_tasks()
                print(f"タスク {task_id} を承認しました")
                return True
        print(f"タスク {task_id} が見つかりません")
        return False
    
    def _make_api_request(self, prompt: str, attempt: int = 1) -> Optional[str]:
        """DeepSeek APIに単一リクエストを送信"""
        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "model": self.config["deepseek_api"]["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.config["deepseek_api"]["temperature"],
                "max_tokens": self.config["deepseek_api"]["max_tokens"]
            }
            
            # タイムアウトを試行回数に応じて調整
            timeout = 60 + (attempt * 30)
            print(f"API呼び出し中... (試行{attempt}, タイムアウト{timeout}秒)")
            
            response = requests.post(
                self.config["deepseek_api"]["endpoint"],
                headers=headers,
                json=data,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                if content:
                    print(f"✅ API成功: {len(content)}文字")
                    return content
                else:
                    print("⚠️ 空のレスポンス")
                    return None
            else:
                print(f"❌ API エラー: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"⏰ タイムアウト ({timeout}秒経過) - 長いプロンプトの可能性")
            return None
        except requests.exceptions.RequestException as e:
            print(f"🔌 接続エラー: {e}")
            return None
        except Exception as e:
            print(f"💥 予期しないエラー: {e}")
            return None
    
    def _chunk_prompt(self, prompt: str) -> list:
        """プロンプトを行単位でチャンク分割"""
        lines = prompt.split('\n')
        total_lines = len(lines)
        
        # チャンクサイズを計算（60%で分割）
        chunk_size = max(10, int(total_lines * 0.6))
        
        chunks = []
        for i in range(0, total_lines, chunk_size):
            chunk_lines = lines[i:i + chunk_size]
            chunks.append('\n'.join(chunk_lines))
        
        print(f"📦 プロンプトを{len(chunks)}チャンクに分割 (各チャンク約{chunk_size}行)")
        return chunks
    
    def _merge_responses(self, responses: list) -> str:
        """複数のレスポンスをシンプルに結合"""
        merged_parts = []
        
        for i, response in enumerate(responses):
            if response and response.strip():
                # コードブロックのマークダウンを除去
                clean_response = response.strip()
                if clean_response.startswith('```'):
                    lines = clean_response.split('\n')
                    # 最初と最後の```行を除去
                    clean_lines = []
                    skip_first = True
                    for line in reversed(lines):
                        if line.strip() == '```' and skip_first:
                            skip_first = False
                            continue
                        clean_lines.append(line)
                    clean_lines.reverse()
                    
                    if clean_lines and clean_lines[0].strip().startswith('```'):
                        clean_lines = clean_lines[1:]
                    
                    clean_response = '\n'.join(clean_lines)
                
                merged_parts.append(f"# === チャンク{i+1} ===")
                merged_parts.append(clean_response)
        
        result = '\n\n'.join(merged_parts)
        print(f"🔗 {len(responses)}チャンクを結合完了: {len(result)}文字")
        return result
    
    def call_deepseek(self, prompt: str) -> Optional[str]:
        """DeepSeek API呼び出し（チャンク処理対応）"""
        print("🤖 DeepSeek API呼び出し開始")
        
        # 最初は通常の処理を試行
        result = self._make_api_request(prompt)
        
        if result:
            print("✅ 通常処理で成功")
            return result
        
        print("⚠️ 通常処理が失敗、チャンク処理を開始...")
        
        # チャンク分割処理
        chunks = self._chunk_prompt(prompt)
        
        if len(chunks) <= 1:
            print("❌ チャンク分割不可、処理を中断")
            return None
        
        responses = []
        for i, chunk in enumerate(chunks):
            print(f"📝 チャンク{i+1}/{len(chunks)}を処理中...")
            
            # チャンク用のプロンプト準備
            chunk_prompt = f"""以下の要件の一部を実装してください（パート{i+1}/{len(chunks)}）：

{chunk}

実用的で動作するPythonコードのみを返してください。説明は不要です。"""
            
            chunk_result = self._make_api_request(chunk_prompt, attempt=i+1)
            
            if chunk_result:
                responses.append(chunk_result)
                print(f"✅ チャンク{i+1}完了")
            else:
                print(f"❌ チャンク{i+1}失敗")
                return None
        
        # レスポンスを結合
        if responses:
            return self._merge_responses(responses)
        
        print("❌ 全チャンク処理失敗")
        return None
    
    def run_workflow(self, task_id: str) -> bool:
        """ワークフロー実行（タスク → DeepSeek → 結果保存）"""
        # タスク検索
        task = None
        for t in self.tasks:
            if t["id"] == task_id:
                task = t
                break
        
        if not task:
            print(f"タスク {task_id} が見つかりません")
            return False
        
        if not task["approved"]:
            print(f"タスク {task_id} は未承認です。先に承認してください")
            return False
        
        print(f"ワークフロー開始: {task['title']}")
        
        # DeepSeekへの命令書作成
        prompt = f"""
以下の要件に基づいてPythonコードを生成してください：

タイトル: {task['title']}
詳細説明: {task['description']}

要求事項:
1. 実用的で動作するコードを書く
2. 適切なコメントを日本語で追加
3. エラーハンドリングを含める
4. 簡潔で読みやすいコードにする

コードのみを返してください（説明文は不要）。
"""
        
        print("🚀 DeepSeek でコード生成を開始...")
        result = self.call_deepseek(prompt)
        
        if result:
            # 結果保存
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{task_id}_{timestamp}.py"
            result_path = self.results_dir / filename
            
            with open(result_path, 'w', encoding='utf-8') as f:
                f.write(f"# {task['title']}\n")
                f.write(f"# タスクID: {task_id}\n")
                f.write(f"# 生成日時: {timestamp}\n\n")
                f.write(result)
            
            # タスク更新
            task["status"] = "completed"
            task["completed_at"] = datetime.datetime.now().isoformat()
            task["result_file"] = str(result_path)
            self.save_tasks()
            
            print(f"✅ 完了! 結果: {result_path}")
            print(f"📝 コード ({len(result)} 文字):")
            print("-" * 50)
            print(result[:500] + ("..." if len(result) > 500 else ""))
            return True
        else:
            print("❌ DeepSeek からの応答取得に失敗しました")
            return False
    
    def run_cli(self):
        """CLI実行"""
        print("[INFO] Simple Hybrid Pair Programming System")
        print("使用方法:")
        print("  create <タイトル> <説明>  - 新規タスク作成")
        print("  list                     - タスク一覧")
        print("  approve <ID>             - タスク承認")
        print("  run <ID>                 - ワークフロー実行")
        print("  exit                     - 終了")
        
        while True:
            try:
                command = input("\n> ").strip().split()
                if not command:
                    continue
                
                if command[0] == "exit":
                    print("終了します")
                    break
                elif command[0] == "create" and len(command) >= 3:
                    title = command[1]
                    description = " ".join(command[2:])
                    self.create_task(title, description)
                elif command[0] == "list":
                    self.list_tasks()
                elif command[0] == "approve" and len(command) == 2:
                    self.approve_task(command[1])
                elif command[0] == "run" and len(command) == 2:
                    self.run_workflow(command[1])
                else:
                    print("無効なコマンドです")
            except KeyboardInterrupt:
                print("\n終了します")
                break
            except Exception as e:
                print(f"エラー: {e}")

if __name__ == "__main__":
    app = SimpleHybridPair()
    app.run_cli()
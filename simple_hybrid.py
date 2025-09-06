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
    
    def call_deepseek(self, prompt: str) -> Optional[str]:
        """DeepSeek APIを呼び出し"""
        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "model": self.config["deepseek_api"]["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.config["deepseek_api"]["temperature"],
                "max_tokens": self.config["deepseek_api"]["max_tokens"]
            }
            
            response = requests.post(
                self.config["deepseek_api"]["endpoint"],
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"API エラー: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"接続エラー: {e}")
            return None
        except Exception as e:
            print(f"予期しないエラー: {e}")
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
        
        print("DeepSeek に送信中...")
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
        print("🤖 Simple Hybrid Pair Programming System")
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
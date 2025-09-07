#!/usr/bin/env python3
"""
超シンプルハイブリッド実行システム
Ultra Simple Hybrid Execution System

機能：
1. 命令書を受け取る（人間から直接）
2. SLMにコードを生成させる  
3. ClaudeCodeで修正して指定場所に保存する
"""

import json
import os
import requests
import datetime
from pathlib import Path
from typing import Dict, Optional

class UltraSimpleHybrid:
    def __init__(self, config_file="simple_config.json"):
        """超シンプル初期化"""
        self.config_file = config_file
        self.config = self.load_config()
    
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
    
    def call_slm(self, instruction: str) -> Optional[str]:
        """SLM（DeepSeek）にコード生成を依頼"""
        try:
            # SLM用のプロンプトを強化（コードのみ要求）
            enhanced_instruction = f"""
{instruction}

実用的で動作するPythonコードのみを返してください。
説明文や解説は一切不要です。
コメントは日本語で書いてください。
コードブロック（```）も不要です。
"""
            
            headers = {"Content-Type": "application/json"}
            data = {
                "model": self.config["deepseek_api"]["model"],
                "messages": [{"role": "user", "content": enhanced_instruction}],
                "temperature": self.config["deepseek_api"]["temperature"],
                "max_tokens": self.config["deepseek_api"]["max_tokens"]
            }
            
            print("🤖 SLMにコード生成を依頼中...")
            response = requests.post(
                self.config["deepseek_api"]["endpoint"],
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # コードを抽出・クリーンアップ
                cleaned_code = self.extract_code(content)
                
                print(f"✅ SLMからコード取得成功: {len(cleaned_code)}文字")
                return cleaned_code
            else:
                print(f"❌ SLM API エラー: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ SLM呼び出しエラー: {e}")
            return None
    
    def extract_code(self, content: str) -> str:
        """レスポンスからPythonコードを抽出"""
        import re
        
        # コードブロックがある場合は抽出
        code_blocks = re.findall(r'```(?:python)?\n?(.*?)\n?```', content, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()
        
        # コードブロックがない場合、説明文を除去してコード部分を抽出
        lines = content.split('\n')
        code_lines = []
        in_code_section = False
        
        for line in lines:
            stripped = line.strip()
            
            # Pythonコードの開始を検出
            if (stripped.startswith('def ') or 
                stripped.startswith('class ') or 
                stripped.startswith('import ') or 
                stripped.startswith('from ') or
                stripped.startswith('if __name__') or
                (stripped and not stripped.startswith('#') and '=' in stripped)):
                in_code_section = True
            
            # 説明文や例のスキップ
            if (stripped.startswith('以下の') or 
                stripped.startswith('上記の') or
                stripped.startswith('例:') or
                stripped.startswith('出力:') or
                stripped.startswith('### ')):
                in_code_section = False
                continue
                
            if in_code_section and (stripped or not code_lines):
                code_lines.append(line)
        
        result = '\n'.join(code_lines).strip()
        return result if result else content.strip()
    
    def save_to_location(self, content: str, save_path: str) -> str:
        """指定場所にファイル保存"""
        file_path = Path(save_path)
        
        # ディレクトリが存在しない場合は作成
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 ファイル保存完了: {file_path}")
        return str(file_path)
    
    def execute_instruction(self, instruction: str, save_path: str) -> bool:
        """命令書実行：SLM生成 → 保存"""
        print(f"🚀 実行開始")
        print(f"📝 命令内容: {instruction[:100]}...")
        print(f"💾 保存先: {save_path}")
        
        # 1. SLMでコード生成
        generated_code = self.call_slm(instruction)
        if not generated_code:
            print("❌ SLMでのコード生成に失敗しました")
            return False
        
        # 2. 指定場所に保存
        saved_file = self.save_to_location(generated_code, save_path)
        
        print(f"✅ 実行完了!")
        return True

def main():
    """メイン実行"""
    print("=== 超シンプルハイブリッド実行システム ===")
    print("使用方法:")
    print("1. execute_instruction(命令書, 保存パス)")
    print("2. または対話モードで実行")
    print()
    
    hybrid = UltraSimpleHybrid()
    
    # 対話モード
    while True:
        print("\n" + "="*50)
        
        print("\n命令書を入力してください (改行2回で終了):")
        instruction_lines = []
        empty_line_count = 0
        
        while empty_line_count < 2:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
            else:
                empty_line_count = 0
            instruction_lines.append(line)
        
        # 最後の空行を除去
        while instruction_lines and instruction_lines[-1].strip() == "":
            instruction_lines.pop()
        
        instruction = "\n".join(instruction_lines)
        
        if not instruction.strip():
            if input("終了しますか？ (y/n): ").lower() == 'y':
                print("終了します")
                break
            continue
        
        save_path = input("保存パス (例: C:/projects/my_app.py): ").strip()
        if not save_path:
            print("保存パスを入力してください")
            continue
        
        # 実行
        hybrid.execute_instruction(instruction, save_path)

if __name__ == "__main__":
    main()
#!/usr/bin/env python
"""
手動data_analyzer実行テスト
Python環境問題回避のための直接実行スクリプト

Phase 3継続: 複雑な型ヒント対応機能テスト
ID: ed6e1213-1068-42bc-bf7f-0cefea43b0c0
"""

import json
import requests
import time
from pathlib import Path

def load_instruction():
    """data_analyzer命令書を読み込み"""
    instruction_path = Path("data/instructions/ed6e1213-1068-42bc-bf7f-0cefea43b0c0.json")
    
    if not instruction_path.exists():
        print(f"❌ 命令書が見つかりません: {instruction_path}")
        return None
        
    with open(instruction_path, 'r', encoding='utf-8') as f:
        instruction = json.load(f)
    
    print(f"✅ 命令書読み込み完了")
    print(f"   ID: {instruction['id']}")
    print(f"   機能: {instruction['function_name']}")
    print(f"   ステータス: {instruction['status']}")
    
    return instruction

def create_slm_prompt(instruction):
    """DeepSeek-Coder用プロンプト作成"""
    req = instruction['requirements']
    
    # 型ヒント情報を強調
    type_info = []
    for param in req['input']['parameters']:
        type_info.append(f"- {param['name']}: {param['type']} - {param['description']}")
    
    prompt = f"""あなたは優秀なPythonプログラマーです。以下の仕様に従って関数を実装してください。

【実装する関数】
関数名: {instruction['function_name']}

【入力パラメータ（型ヒント重要）】
{chr(10).join(type_info)}

【出力仕様】
- 型: {req['output']['type']}
- 形式: {req['output']['format']}
- 例: {req['output']['example']}

【入力検証要件】
{chr(10).join([f"- {rule}" for rule in req['validation']['input_validation']])}

【出力検証要件】  
{chr(10).join([f"- {rule}" for rule in req['validation']['output_validation']])}

【依存関係】
{chr(10).join([f"- {dep}" for dep in req['dependencies']])}

【コードスタイル要件】
- {req['style']['coding_standard']}
- Docstring: {req['style']['docstring']}
- 型ヒント: {req['style']['type_hints']}
- コメント: {req['style']['comments']}

【重要】
1. 複雑な型ヒント `List[Dict[str, Union[int, float, str]]]` を正確に実装
2. 3つの分析タイプ (basic_stats, distribution, correlation) をサポート  
3. 完全な型安全性とエラーハンドリング
4. docstringと日本語コメントを含む

実装してください："""
    
    return prompt

def call_deepseek_api(prompt):
    """LM Studio経由でDeepSeek-Coder API呼び出し"""
    
    # LM Studio APIエンドポイント（デフォルト設定）
    url = "http://localhost:1234/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "model": "local-model",  # LM Studioのローカルモデル
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,  # 低温度で一貫性重視
        "max_tokens": 2000,  # 長いコード生成用
        "stream": False
    }
    
    print("🤖 DeepSeek-Coder API呼び出し開始...")
    print(f"   エンドポイント: {url}")
    
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data, timeout=30)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            generated_code = result['choices'][0]['message']['content']
            
            print(f"✅ コード生成成功")
            print(f"   応答時間: {elapsed_time:.2f}秒")
            print(f"   生成文字数: {len(generated_code)}文字")
            
            return generated_code
            
        else:
            print(f"❌ API呼び出し失敗")
            print(f"   ステータスコード: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API接続エラー: {e}")
        print("💡 LM Studioが起動してDeepSeek-Coderが読み込まれているか確認してください")
        return None

def save_generated_code(instruction_id, generated_code):
    """生成コードを保存"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"data_analyzer_{instruction_id[:8]}_{timestamp}.py"
    output_path = Path("data/generated_code") / filename
    
    # 出力ディレクトリ作成
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(generated_code)
    
    print(f"✅ 生成コード保存完了: {output_path}")
    return output_path

def main():
    """メイン実行"""
    print("=" * 60)
    print("🤝 LLM×SLM data_analyzer実行テスト")
    print("🎯 Phase 3: 複雑な型ヒント対応機能テスト")
    print("=" * 60)
    
    # Step 1: 命令書読み込み
    instruction = load_instruction()
    if not instruction:
        return 1
    
    if instruction['status'] != 'approved':
        print(f"⚠️ 命令書が承認されていません: {instruction['status']}")
        print("承認後に再実行してください")
        return 1
    
    # Step 2: プロンプト作成
    prompt = create_slm_prompt(instruction)
    print(f"\n📝 プロンプト作成完了 ({len(prompt)}文字)")
    
    # Step 3: DeepSeek-Coder実行
    generated_code = call_deepseek_api(prompt)
    if not generated_code:
        return 1
    
    # Step 4: コード保存
    output_path = save_generated_code(instruction['id'], generated_code)
    
    print(f"\n🎉 data_analyzer実行テスト完了")
    print(f"📄 生成ファイル: {output_path}")
    print(f"\n📋 次のステップ:")
    print(f"1. 生成コードの品質確認")
    print(f"2. 実動テスト実行")
    print(f"3. 型ヒント検証")
    
    return 0

if __name__ == "__main__":
    exit(main())
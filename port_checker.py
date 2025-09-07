#!/usr/bin/env python3
"""
LM Studioのポート検出スクリプト
"""
import requests
import json

def check_port(port):
    """指定ポートでSLMが動作しているかチェック"""
    try:
        url = f"http://localhost:{port}/v1/models"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            models = response.json()
            return models.get('data', [])
        return None
    except:
        return None

def find_available_models():
    """利用可能なモデルを検出"""
    print("🔍 LM Studioのモデルを検出中...")
    
    for port in range(1234, 1240):  # 1234-1239ポートをチェック
        models = check_port(port)
        if models:
            print(f"✅ ポート {port} で発見:")
            for model in models:
                model_id = model.get('id', 'unknown')
                print(f"   - {model_id}")
            print()
        else:
            print(f"❌ ポート {port}: 接続なし")
    
    print("LM Studioの画面で「Reachable at」を確認してください")

if __name__ == "__main__":
    find_available_models()
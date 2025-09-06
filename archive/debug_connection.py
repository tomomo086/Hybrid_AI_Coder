"""
LM Studio接続デバッグツール

接続問題の診断と解決支援を行う
"""

import json
import requests
import time
import sys
from pathlib import Path

def test_lm_studio_connection():
    """LM Studio接続の詳細テスト"""
    print("🔍 LM Studio 接続診断ツール")
    print("=" * 50)
    
    # 設定読み込み
    config_path = Path("config/config.json")
    if not config_path.exists():
        print("❌ config.json が見つかりません")
        print("セットアップを実行してください: python hybrid_pair.py setup")
        return False
        
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    slm_config = config.get("slm_config", {})
    endpoint = slm_config.get("api_endpoint", "http://localhost:1234/v1/chat/completions")
    model = slm_config.get("model", "deepseek-coder-6.7b-instruct")
    
    print(f"📡 テスト対象:")
    print(f"   エンドポイント: {endpoint}")
    print(f"   モデル: {model}")
    print()
    
    # Step 1: 基本接続テスト
    print("1️⃣ 基本接続テスト...")
    try:
        base_url = endpoint.replace('/v1/chat/completions', '')
        response = requests.get(f"{base_url}/v1/models", timeout=5)
        
        if response.status_code == 200:
            print("✅ LM Studio サーバーに接続成功")
            
            models = response.json().get("data", [])
            if models:
                print(f"📚 利用可能なモデル:")
                for model_info in models:
                    print(f"   - {model_info.get('id', 'Unknown')}")
            else:
                print("⚠️ モデルが読み込まれていません")
                
        else:
            print(f"❌ サーバー応答エラー: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 接続エラー: LM Studio が起動していません")
        print("📋 確認項目:")
        print("   1. LM Studio アプリケーションが起動している")
        print("   2. モデルが読み込まれている")  
        print("   3. Local Server が開始されている")
        return False
        
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False
        
    # Step 2: Chat API テスト
    print("\n2️⃣ Chat API テスト...")
    
    test_payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Say 'Hello' in Python code"}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            endpoint,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            print(f"✅ Chat API 成功 (応答時間: {elapsed:.1f}秒)")
            print(f"📝 生成結果:")
            print(f"   {content[:100]}...")
            
            # パフォーマンス評価
            if elapsed < 5:
                print("🚀 パフォーマンス: 高速")
            elif elapsed < 15:
                print("⚡ パフォーマンス: 良好") 
            else:
                print("🐌 パフォーマンス: 低速（最適化を推奨）")
                
        else:
            print(f"❌ Chat API エラー: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"エラー詳細: {error_detail}")
            except:
                print(f"エラー詳細: {response.text}")
                
    except requests.exceptions.Timeout:
        print("❌ タイムアウト: 応答が遅すぎます")
        print("💡 改善提案:")
        print("   - より軽量なモデル (Q4_K_M) を試す")
        print("   - GPU使用を有効にする")
        print("   - Context Lengthを削減する")
        return False
        
    except Exception as e:
        print(f"❌ Chat API エラー: {e}")
        return False
        
    # Step 3: システムリソースチェック
    print("\n3️⃣ システムリソースチェック...")
    
    try:
        import psutil
        
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"💻 CPU使用率: {cpu_percent}%")
        
        # メモリ使用率
        memory = psutil.virtual_memory()
        print(f"🧠 メモリ使用率: {memory.percent}% ({memory.used/1024**3:.1f}GB / {memory.total/1024**3:.1f}GB)")
        
        if memory.percent > 85:
            print("⚠️ メモリ使用量が高いです")
            
        # GPU情報 (NVIDIA)
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                for gpu in gpus:
                    print(f"🎮 GPU: {gpu.name}")
                    print(f"   VRAM: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB ({gpu.memoryUtil*100:.1f}%)")
                    print(f"   温度: {gpu.temperature}°C")
            else:
                print("🎮 GPU: 検出されませんでした (CPU推論モード)")
        except ImportError:
            print("🎮 GPU: 情報取得不可 (GPUtilが未インストール)")
            
    except ImportError:
        print("⚠️ システム情報取得不可 (psutilが未インストール)")
        
    print("\n✅ 診断完了！")
    return True


def show_optimization_tips():
    """最適化のヒントを表示"""
    print("\n💡 パフォーマンス最適化のヒント:")
    print("=" * 40)
    
    print("🚀 高速化:")
    print("   - GPU使用を有効にする")
    print("   - より軽量なモデル (Q4_K_M) を使用")
    print("   - Context Lengthを削減 (4096 → 2048)")
    print("   - 不要なアプリケーションを終了")
    
    print("\n🎯 品質向上:")
    print("   - Temperature を 0.1-0.3 に設定")
    print("   - より大きなモデル (Q8_0) を使用")
    print("   - システムRAMを増設")
    
    print("\n🔧 トラブル解決:")
    print("   - LM Studio を再起動")
    print("   - モデルを再読み込み")
    print("   - ポート競合を確認 (1234番)")
    print("   - Windows Defender除外設定")


def main():
    """メイン関数"""
    if test_lm_studio_connection():
        show_optimization_tips()
    else:
        print("\n🆘 問題が発生しました")
        print("詳細なセットアップガイドを確認してください:")
        print("docs/LM_Studio_Setup_Guide.md")


if __name__ == "__main__":
    main()
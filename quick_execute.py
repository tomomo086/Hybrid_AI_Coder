#!/usr/bin/env python3
"""
クイック実行スクリプト
ClaudeCode用の簡単なラッパー

使用方法:
from quick_execute import quick_hybrid
result = quick_hybrid("電卓アプリを作って", "calculator_app")
"""

from ultra_simple import UltraSimpleHybrid

def quick_hybrid(instruction: str, save_path: str) -> bool:
    """
    ワンライナーでハイブリッド実行
    
    Args:
        instruction: SLMへの命令書
        save_path: 保存パス（フルパス）
    
    Returns:
        bool: 成功したかどうか
    """
    hybrid = UltraSimpleHybrid()
    return hybrid.execute_instruction(instruction, save_path)

def test_system() -> bool:
    """システムテスト"""
    test_instruction = """
シンプルな挨拶アプリを作成してください。
- 名前を入力すると挨拶を返す
- 日本語対応
- 簡潔なコード
"""
    
    print("🧪 システムテスト実行...")
    result = quick_hybrid(test_instruction, "test_greeting.py")
    
    if result:
        print("✅ テスト成功！")
    else:
        print("❌ テスト失敗")
    
    return result

if __name__ == "__main__":
    # テスト実行
    test_system()
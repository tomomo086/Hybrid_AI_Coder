"""
システム統合テスト

全体的なワークフローの動作確認を行う
"""

import json
import time
import sys
from pathlib import Path

def run_system_test():
    """システム統合テスト実行"""
    print("🧪 LLM×SLM システム統合テスト")
    print("=" * 50)
    
    test_results = {
        "setup_test": False,
        "connection_test": False,
        "instruction_creation": False,
        "approval_workflow": False,
        "code_generation": False
    }
    
    # Test 1: セットアップ確認
    print("\n1️⃣ セットアップ確認...")
    setup_ok = check_setup()
    test_results["setup_test"] = setup_ok
    
    if not setup_ok:
        print("❌ セットアップが不完全です")
        show_setup_instructions()
        return False
        
    # Test 2: API接続確認
    print("\n2️⃣ API接続確認...")
    connection_ok = check_api_connections()
    test_results["connection_test"] = connection_ok
    
    if not connection_ok:
        print("❌ API接続に問題があります")
        print("詳細診断: python debug_connection.py")
        return False
        
    # Test 3: 命令書システムテスト
    print("\n3️⃣ 命令書システムテスト...")
    instruction_ok = test_instruction_system()
    test_results["instruction_creation"] = instruction_ok
    
    # Test 4: 承認ワークフローテスト
    print("\n4️⃣ 承認ワークフローテスト...")
    approval_ok = test_approval_workflow()
    test_results["approval_workflow"] = approval_ok
    
    # Test 5: コード生成テスト（オプション）
    print("\n5️⃣ コード生成テスト (簡易版)...")
    generation_ok = test_code_generation()
    test_results["code_generation"] = generation_ok
    
    # 結果サマリー
    print("\n📊 テスト結果サマリー")
    print("=" * 30)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
            
    print(f"\n総合結果: {passed}/{total} テスト成功")
    
    if passed == total:
        print("🎉 すべてのテストが成功しました！")
        print("システムは正常に動作しています")
        return True
    else:
        print("⚠️ 一部のテストが失敗しました")
        print("問題を解決してから再実行してください")
        return False


def check_setup():
    """セットアップ状況を確認"""
    required_files = [
        "config/config.json",
        "data/instructions",
        "data/generated_code", 
        "data/reviews"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        path = Path(file_path)
        if not path.exists():
            missing_files.append(file_path)
            
    if missing_files:
        print(f"❌ 不足ファイル: {missing_files}")
        return False
        
    # 設定ファイル確認
    try:
        with open("config/config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # 必要な設定項目確認
        if not config.get("slm_config", {}).get("api_endpoint"):
            print("❌ SLM API エンドポイントが設定されていません")
            return False
            
        print("✅ セットアップ確認完了")
        return True
        
    except Exception as e:
        print(f"❌ 設定ファイル読み込みエラー: {e}")
        return False


def check_api_connections():
    """API接続確認"""
    try:
        # SLM接続テスト
        from src.api.slm_client import SLMClient
        
        with open("config/config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        slm_client = SLMClient(config["slm_config"])
        
        print("🤖 SLM接続テスト...")
        if not slm_client.test_connection():
            print("❌ SLM接続失敗")
            return False
        print("✅ SLM接続成功")
        
        # LLM接続テスト（APIキーがある場合のみ）
        llm_api_key = config.get("llm_config", {}).get("api_key", "")
        if llm_api_key and len(llm_api_key) > 10:
            from src.api.llm_client import LLMClient
            
            print("🧠 LLM接続テスト...")
            llm_client = LLMClient(config["llm_config"])
            if not llm_client.test_connection():
                print("❌ LLM接続失敗（APIキー確認）")
                return False
            print("✅ LLM接続成功")
        else:
            print("ℹ️ LLM APIキーが未設定（スキップ）")
            
        return True
        
    except Exception as e:
        print(f"❌ API接続テストエラー: {e}")
        return False


def test_instruction_system():
    """命令書システムテスト"""
    try:
        from src.core.instruction_manager import InstructionManager
        
        manager = InstructionManager()
        
        # テスト用命令書作成
        test_requirements = {
            "input": {"description": "テスト用入力"},
            "output": {"description": "テスト用出力"},
            "test_cases": [{"name": "基本テスト", "input": "test", "expected_output": "result"}]
        }
        
        instruction = manager.create_instruction("test_function", test_requirements)
        
        # 基本操作テスト
        retrieved = manager.get_instruction(instruction.id)
        if not retrieved:
            print("❌ 命令書取得失敗")
            return False
            
        # 更新テスト
        updated_requirements = test_requirements.copy()
        updated_requirements["version"] = "2.0"
        
        if not manager.update_instruction(instruction.id, updated_requirements):
            print("❌ 命令書更新失敗") 
            return False
            
        print("✅ 命令書システムテスト成功")
        return True
        
    except Exception as e:
        print(f"❌ 命令書システムエラー: {e}")
        return False


def test_approval_workflow():
    """承認ワークフローテスト"""
    try:
        from src.core.instruction_manager import InstructionManager, InstructionStatus
        
        manager = InstructionManager()
        
        # テスト用命令書で承認フローをテスト
        instructions = list(manager.instructions.values())
        if not instructions:
            print("ℹ️ テスト用命令書を作成中...")
            test_requirements = {"input": {"description": "承認テスト用"}}
            instruction = manager.create_instruction("approval_test", test_requirements)
        else:
            instruction = instructions[0]
            
        # 承認テスト
        instruction.status = InstructionStatus.PENDING_REVIEW
        if not manager.approve_instruction(instruction.id, "システムテスト"):
            print("❌ 承認処理失敗")
            return False
            
        # 承認状態確認
        approved_instruction = manager.get_instruction(instruction.id)
        if approved_instruction.status != InstructionStatus.APPROVED:
            print("❌ 承認状態確認失敗")
            return False
            
        print("✅ 承認ワークフローテスト成功")
        return True
        
    except Exception as e:
        print(f"❌ 承認ワークフローエラー: {e}")
        return False


def test_code_generation():
    """コード生成テスト（簡易版）"""
    try:
        from src.api.slm_client import SLMClient
        
        with open("config/config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        slm_client = SLMClient(config["slm_config"])
        
        # 簡単なコード生成テスト
        test_prompt = "def hello_world():\n    \"\"\"Hello World を出力する関数\"\"\""
        
        print("🔄 簡易コード生成テスト...")
        result = slm_client.generate_code(f"{test_prompt}\n上記の関数を完成させてください。")
        
        if result and len(result) > 20:
            print(f"✅ コード生成成功 ({len(result)} 文字)")
            return True
        else:
            print("❌ コード生成失敗（空の結果）")
            return False
            
    except Exception as e:
        print(f"❌ コード生成テストエラー: {e}")
        return False


def show_setup_instructions():
    """セットアップ手順を表示"""
    print("\n🔧 セットアップが必要です:")
    print("1. python hybrid_pair.py setup")
    print("2. config/config.json でAPIキーを設定")
    print("3. LM Studio を起動し、DeepSeekモデルを読み込み")
    print("4. 詳細ガイド: docs/LM_Studio_Setup_Guide.md")


def main():
    """メイン関数"""
    print("システム統合テストを実行します...")
    print("このテストは基本機能の動作確認を行います")
    print()
    
    try:
        success = run_system_test()
        if success:
            print("\n🎊 システムは正常に動作しています！")
            print("次のステップ: QUICKSTART.md で実際の使用方法を確認")
        else:
            print("\n🔧 問題を解決後、再実行してください")
            
    except KeyboardInterrupt:
        print("\n⏹️ テストを中断しました")
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
        

if __name__ == "__main__":
    main()
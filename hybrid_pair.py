"""
LLM×SLM ハイブリッドペアプログラミング システム
メインCLIエントリーポイント

完全なCMDベースワークフロー：
1. 命令書作成 → 2. 人間承認 → 3. DeepSeek実装 → 4. Claude最適化
"""

import argparse
import sys
import subprocess
import locale
import os
from pathlib import Path
from typing import List

# UTF-8エンコーディング設定（文字化け解決）
def setup_encoding():
    """日本語文字化けを解決するエンコーディング設定"""
    try:
        # 環境変数でPythonのエンコーディングを設定
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        # 標準出力・エラー出力のエンコーディングを再設定
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):  
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
            
        # コンソールの日本語表示を改善
        if sys.platform == 'win32':
            import subprocess
            # Windows コンソールのコードページをUTF-8に設定
            subprocess.run(['chcp', '65001'], shell=True, capture_output=True)
            
        return True
    except Exception as e:
        print(f"エンコーディング設定エラー: {e}")
        return False

# システム起動時にエンコーディングを設定
setup_encoding()

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))


class HybridPairCLI:
    """ハイブリッドペアプログラミング メインCLI"""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        
    def show_workflow(self):
        """ワークフロー説明を表示"""
        print("""
🤝 LLM×SLM ハイブリッドペアプログラミング システム
==========================================

📋 基本ワークフロー:
  1️⃣  命令書作成    → hybrid_pair.py create <機能名>
  2️⃣  命令書確認    → hybrid_pair.py review <ID>  
  3️⃣  人間承認      → hybrid_pair.py approve <ID> --approver <名前>
  4️⃣  コード生成    → hybrid_pair.py execute <ID>
  5️⃣  結果確認      → hybrid_pair.py status

🔧 主要コマンド:
  create     新しい命令書を作成
  list       命令書一覧表示
  review     命令書詳細確認・編集
  approve    命令書承認
  execute    承認済み命令書の実行
  status     システム状況確認
  setup      初期セットアップ

📚 詳細ヘルプ:
  hybrid_pair.py <コマンド> --help
        """)
        
    def run_command(self, module_path: str, args: List[str]) -> int:
        """サブコマンドを実行"""
        try:
            cmd = [sys.executable, '-m', module_path] + args
            result = subprocess.run(cmd, cwd=self.project_root)
            return result.returncode
        except KeyboardInterrupt:
            print("\n⏹️ 操作をキャンセルしました")
            return 1
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            return 1
            
    def setup_project(self):
        """プロジェクト初期セットアップ"""
        print("🔧 LLM×SLM システム初期セットアップ")
        print("=" * 50)
        
        # 設定ファイルのコピー
        config_path = self.project_root / "config" / "config.json"
        example_config = self.project_root / "config" / "config.example.json"
        
        if not config_path.exists() and example_config.exists():
            import shutil
            shutil.copy(example_config, config_path)
            print(f"✅ 設定ファイルを作成しました: {config_path}")
            print("⚠️  APIキーの設定を忘れずに行ってください")
        else:
            print(f"ℹ️  設定ファイルは既に存在します: {config_path}")
            
        # レビューチェックリスト作成
        checklist_path = self.project_root / "config" / "review_checklist.json"
        if not checklist_path.exists():
            import json
            
            default_checklist = {
                "version": "1.0",
                "security": {
                    "sql_injection": ["sql", "query", "execute", "cursor"],
                    "command_injection": ["os.system", "subprocess", "eval", "exec"],
                    "file_traversal": ["../", "..\\", "open(", "file("],
                    "hardcoded_secrets": ["password", "api_key", "secret", "token"]
                },
                "performance": {
                    "inefficient_patterns": ["nested_loops", "redundant_operations"],
                    "memory_leaks": ["unclosed_files", "circular_references"]
                },
                "style": {
                    "naming_conventions": ["snake_case", "UPPER_CASE"],
                    "documentation": ["docstring", "type_hints"],
                    "code_structure": ["function_length", "complexity"]
                }
            }
            
            with open(checklist_path, 'w', encoding='utf-8') as f:
                json.dump(default_checklist, f, ensure_ascii=False, indent=2)
            print(f"✅ レビューチェックリストを作成しました: {checklist_path}")
            
        # 必要ディレクトリの作成確認
        required_dirs = [
            "data/instructions",
            "data/generated_code", 
            "data/reviews",
            "logs"
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            
        print("✅ 必要ディレクトリを確認しました")
        
        print(f"\n🎉 セットアップ完了！")
        print(f"\n📋 次のステップ:")
        print(f"1. config/config.json でAPIキーを設定")
        print(f"2. LM Studio を起動してDeepSeek-Coderを読み込み")
        print(f"3. 接続テスト: hybrid_pair.py test")
        print(f"4. 最初の命令書作成: hybrid_pair.py create sample_function")
        
    def test_connections(self):
        """API接続テスト"""
        print("🔍 API接続テスト")
        print("=" * 30)
        
        try:
            # SLM (DeepSeek) 接続テスト
            from src.api.slm_client import SLMClient
            import json
            
            config_path = self.project_root / "config" / "config.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                print("🤖 SLM (DeepSeek) 接続テスト...")
                slm_client = SLMClient(config["slm_config"])
                if slm_client.test_connection():
                    print("✅ SLM接続成功")
                else:
                    print("❌ SLM接続失敗 - LM Studioを確認してください")
                    
                print("\n🧠 LLM (Claude) 接続テスト...")
                from src.api.llm_client import LLMClient
                llm_client = LLMClient(config["llm_config"])
                if llm_client.test_connection():
                    print("✅ LLM接続成功")
                else:
                    print("❌ LLM接続失敗 - APIキーを確認してください")
                    
            else:
                print("❌ 設定ファイルがありません")
                print("セットアップを実行してください: hybrid_pair.py setup")
                
        except Exception as e:
            print(f"❌ 接続テストエラー: {e}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="LLM×SLM ハイブリッドペアプログラミング システム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # システムセットアップ
  python hybrid_pair.py setup
  
  # 接続テスト
  python hybrid_pair.py test
  
  # 命令書作成
  python hybrid_pair.py create user_authentication_function
  
  # 命令書一覧
  python hybrid_pair.py list
  
  # 命令書詳細確認
  python hybrid_pair.py review abc123def456
  
  # 命令書承認
  python hybrid_pair.py approve abc123def456 --approver "山田太郎"
  
  # コード生成実行
  python hybrid_pair.py execute abc123def456
  
  # システム状況確認
  python hybrid_pair.py status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')
    
    # setup コマンド
    setup_parser = subparsers.add_parser('setup', help='初期セットアップ')
    
    # test コマンド
    test_parser = subparsers.add_parser('test', help='API接続テスト')
    
    # create コマンド
    create_parser = subparsers.add_parser('create', help='命令書作成')
    create_parser.add_argument('function_name', help='実装する機能名')
    create_parser.add_argument('--template', default='basic_function', help='テンプレート名')
    create_parser.add_argument('--no-interactive', action='store_true', help='非対話モード')
    
    # list コマンド
    list_parser = subparsers.add_parser('list', help='命令書一覧')
    list_parser.add_argument('--status', help='ステータスフィルター')
    
    # review コマンド
    review_parser = subparsers.add_parser('review', help='命令書詳細確認')
    review_parser.add_argument('instruction_id', help='命令書ID')
    
    # approve コマンド
    approve_parser = subparsers.add_parser('approve', help='命令書承認')
    approve_parser.add_argument('instruction_id', help='命令書ID')
    approve_parser.add_argument('--approver', required=True, help='承認者名')
    
    # execute コマンド
    execute_parser = subparsers.add_parser('execute', help='承認済み命令書実行')
    execute_parser.add_argument('instruction_id', help='命令書ID')
    execute_parser.add_argument('--skip-review', action='store_true', help='Claudeレビューをスキップ')
    
    # status コマンド
    status_parser = subparsers.add_parser('status', help='システム状況確認')
    
    # workflow コマンド
    workflow_parser = subparsers.add_parser('workflow', help='ワークフロー説明表示')
    
    args = parser.parse_args()
    
    cli = HybridPairCLI()
    
    if not args.command:
        cli.show_workflow()
        return
        
    try:
        if args.command == 'setup':
            cli.setup_project()
            
        elif args.command == 'test':
            cli.test_connections()
            
        elif args.command == 'create':
            cmd_args = ['create', args.function_name, '--template', args.template]
            if args.no_interactive:
                cmd_args.append('--no-interactive')
            return cli.run_command('src.cli.instruction_creator', cmd_args)
            
        elif args.command == 'list':
            cmd_args = ['list']
            if args.status:
                cmd_args.extend(['--status', args.status])
            return cli.run_command('src.cli.instruction_viewer', cmd_args)
            
        elif args.command == 'review':
            return cli.run_command('src.cli.instruction_viewer', ['show', args.instruction_id])
            
        elif args.command == 'approve':
            return cli.run_command('src.cli.instruction_viewer', [
                'approve', args.instruction_id, '--approver', args.approver
            ])
            
        elif args.command == 'execute':
            cmd_args = ['execute', args.instruction_id]
            if args.skip_review:
                cmd_args.append('--skip-review')
            return cli.run_command('src.workflow.executor', cmd_args)
            
        elif args.command == 'status':
            return cli.run_command('src.cli.instruction_viewer', ['summary'])
            
        elif args.command == 'workflow':
            cli.show_workflow()
            
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
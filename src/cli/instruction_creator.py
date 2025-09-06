"""
CMD用命令書作成ツール

Claude Codeから直接実行できる命令書作成ツール
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# プロジェクトのルートパスを追加
sys.path.append(str(Path(__file__).parent.parent))

from core.instruction_manager import InstructionManager


class InstructionCreator:
    """命令書作成ツール"""
    
    def __init__(self):
        self.instruction_manager = InstructionManager()
        
    def create_from_template(self, 
                           function_name: str,
                           template_name: str = "basic_function",
                           interactive: bool = True) -> Optional[str]:
        """テンプレートから命令書を作成"""
        
        print(f"\n[INFO] LLM×SLM 命令書作成ツール")
        print(f"機能名: {function_name}")
        print(f"テンプレート: {template_name}")
        print("-" * 50)
        
        # テンプレート読み込み
        template_path = Path(f"config/instruction_templates/{template_name}.json")
        if not template_path.exists():
            print(f"[ERROR] テンプレートが見つかりません: {template_path}")
            return None
            
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
            
        requirements = template_data["template"]["requirements"].copy()
        
        if interactive:
            # 対話的に要件を入力
            requirements = self._interactive_input(requirements)
        else:
            # 基本情報のみ更新
            requirements = self._basic_setup(requirements, function_name)
            
        # 命令書作成
        instruction = self.instruction_manager.create_instruction(
            function_name, requirements
        )
        
        print(f"\n[SUCCESS] 命令書を作成しました!")
        print(f"ID: {instruction.id}")
        print(f"ファイル: data/instructions/{instruction.id}.json")
        
        # 次のステップを表示
        print(f"\n[LIST] 次のステップ:")
        print(f"1. 命令書を確認・編集: python -m src.cli.instruction_viewer {instruction.id}")
        print(f"2. Web承認画面を開く: python -m src.ui.approval_gui")
        print(f"3. 承認後にDeepSeekに送信: python -m src.workflow.executor {instruction.id}")
        
        return instruction.id
        
    def _interactive_input(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """対話的な要件入力"""
        print(f"\n[REQUIREMENTS] 要件を入力してください (空白でスキップ):")
        
        # 入力パラメータ
        if "input" in requirements:
            print(f"\n[INPUT] 入力パラメータ:")
            input_desc = input(f"入力の説明 [{requirements['input'].get('description', '')}]: ").strip()
            if input_desc:
                requirements["input"]["description"] = input_desc
                
        # 出力仕様
        if "output" in requirements:
            print(f"\n[OUTPUT] 出力仕様:")
            output_desc = input(f"出力の説明 [{requirements['output'].get('description', '')}]: ").strip()
            if output_desc:
                requirements["output"]["description"] = output_desc
                
        # バリデーション
        if "validation" in requirements:
            print(f"\n[VALIDATION] バリデーション:")
            validation_rules = input("入力検証ルール (カンマ区切り): ").strip()
            if validation_rules:
                requirements["validation"]["input_validation"] = [
                    rule.strip() for rule in validation_rules.split(",")
                ]
                
        # 依存関係
        if "dependencies" in requirements:
            print(f"\n[DEPENDENCIES] 依存関係:")
            deps = input("必要なライブラリ (カンマ区切り): ").strip()
            if deps:
                requirements["dependencies"] = [
                    dep.strip() for dep in deps.split(",")
                ]
                
        # テストケース
        if "test_cases" in requirements:
            print(f"\n[TEST] テストケース:")
            add_test = input("テストケースを追加しますか? (y/N): ").strip().lower()
            if add_test == 'y':
                test_name = input("テスト名: ").strip()
                test_input = input("テスト入力: ").strip()
                test_output = input("期待する出力: ").strip()
                
                if test_name and test_input and test_output:
                    requirements["test_cases"].append({
                        "name": test_name,
                        "input": test_input,
                        "expected_output": test_output,
                        "description": f"{test_name}のテストケース"
                    })
                    
        return requirements
        
    def _basic_setup(self, requirements: Dict[str, Any], function_name: str) -> Dict[str, Any]:
        """基本セットアップ（非対話モード）"""
        # テンプレートの{function_name}を置換
        requirements_str = json.dumps(requirements, ensure_ascii=False)
        requirements_str = requirements_str.replace("{function_name}", function_name)
        return json.loads(requirements_str)
        
    def list_templates(self) -> None:
        """利用可能なテンプレート一覧を表示"""
        template_dir = Path("config/instruction_templates")
        if not template_dir.exists():
            print("[ERROR] テンプレートディレクトリが見つかりません")
            return
            
        templates = list(template_dir.glob("*.json"))
        if not templates:
            print("[ERROR] テンプレートが見つかりません")
            return
            
        print(f"\n[LIST] 利用可能なテンプレート:")
        print("-" * 40)
        
        for template_path in templates:
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    
                name = template_path.stem
                description = template_data.get("description", "説明なし")
                version = template_data.get("version", "不明")
                
                print(f"[TEMPLATE] {name}")
                print(f"   説明: {description}")
                print(f"   バージョン: {version}")
                print()
                
            except Exception as e:
                print(f"[ERROR] {template_path.name}: 読み込みエラー ({e})")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="LLM×SLM ハイブリッド命令書作成ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python -m src.cli.instruction_creator create user_auth_function
  python -m src.cli.instruction_creator create data_validator --template basic_function --no-interactive
  python -m src.cli.instruction_creator list-templates
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')
    
    # create コマンド
    create_parser = subparsers.add_parser('create', help='新しい命令書を作成')
    create_parser.add_argument('function_name', help='実装する機能名')
    create_parser.add_argument(
        '--template', 
        default='basic_function',
        help='使用するテンプレート名 (デフォルト: basic_function)'
    )
    create_parser.add_argument(
        '--no-interactive',
        action='store_true',
        help='対話モードを無効にする'
    )
    
    # list-templates コマンド
    list_parser = subparsers.add_parser('list-templates', help='利用可能なテンプレート一覧')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    creator = InstructionCreator()
    
    if args.command == 'create':
        creator.create_from_template(
            args.function_name,
            args.template,
            not args.no_interactive
        )
    elif args.command == 'list-templates':
        creator.list_templates()


if __name__ == "__main__":
    main()
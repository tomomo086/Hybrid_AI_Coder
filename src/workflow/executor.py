"""
ワークフロー実行エンジン

承認済み命令書をDeepSeekに送信し、生成されたコードをClaudeでレビューする
"""

import json
import argparse
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# プロジェクトのルートパスを追加
sys.path.append(str(Path(__file__).parent.parent))

from core.instruction_manager import InstructionManager, InstructionStatus
from api.slm_client import SLMClient
from api.llm_client import LLMClient
from quality_control.code_reviewer import CodeReviewer


class WorkflowExecutor:
    """ワークフロー実行エンジン"""
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        self.instruction_manager = InstructionManager(
            self.config["project_paths"]["instructions_dir"]
        )
        self.slm_client = SLMClient(self.config["slm_config"])
        self.llm_client = LLMClient(self.config["llm_config"])
        self.code_reviewer = CodeReviewer(self.config["quality_control"])
        
        # 出力ディレクトリの作成
        self.code_output_dir = Path(self.config["project_paths"]["generated_code_dir"])
        self.reviews_output_dir = Path(self.config["project_paths"]["reviews_dir"])
        self.code_output_dir.mkdir(parents=True, exist_ok=True)
        self.reviews_output_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込み"""
        if not self.config_path.exists():
            # config.example.jsonからコピーを促す
            example_path = self.config_path.parent / "config.example.json"
            if example_path.exists():
                print(f"[WARNING] 設定ファイルが見つかりません")
                print(f"'{example_path}' を '{self.config_path}' にコピーして編集してください")
            else:
                print(f"[ERROR] 設定ファイルがありません: {self.config_path}")
            sys.exit(1)
            
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def execute_instruction(self, instruction_id: str, skip_review: bool = False) -> bool:
        """命令書を実行"""
        print(f"\n[WORKFLOW] LLM×SLM ワークフロー実行")
        print("=" * 50)
        
        # 命令書取得
        instruction = self.instruction_manager.get_instruction(instruction_id)
        if not instruction:
            print(f"[ERROR] 命令書が見つかりません: {instruction_id}")
            return False
            
        if instruction.status != InstructionStatus.APPROVED:
            print(f"[ERROR] 承認されていない命令書です: {instruction.status.value}")
            print("承認してから実行してください")
            return False
            
        print(f"[TARGET] 実行対象: {instruction.function_name}")
        print(f"[DATE] 承認日時: {instruction.approved_at}")
        print(f"[APPROVER] 承認者: {instruction.approved_by}")
        
        # Step 1: DeepSeekでコード生成
        print(f"\n[STEP1] Step 1: DeepSeek でコード生成中...")
        generated_code, generation_success = self._generate_code_with_deepseek(instruction)
        
        if not generation_success:
            print(f"[ERROR] コード生成に失敗しました")
            return False
            
        # Step 2: 生成されたコードを保存
        code_file_path = self._save_generated_code(instruction, generated_code)
        print(f"[SAVED] 生成コード保存: {code_file_path}")
        
        # Step 3: Claudeでコードレビュー（オプション）
        review_result = None
        if not skip_review:
            print(f"\n[STEP2] Step 2: Claude でコードレビュー中...")
            review_result, review_success = self._review_code_with_claude(instruction, generated_code)
            
            if review_success:
                review_file_path = self._save_review_result(instruction, review_result)
                print(f"[SAVED] レビュー結果保存: {review_file_path}")
            else:
                print(f"[WARNING] コードレビューに失敗しました（コードは生成済み）")
                
        # Step 4: 実行完了マーク
        self.instruction_manager.mark_as_executed(instruction_id)
        
        print(f"\n[SUCCESS] ワークフロー実行完了！")
        print(f"[FILES] 生成ファイル:")
        print(f"   コード: {code_file_path}")
        if review_result:
            print(f"   レビュー: {review_file_path}")
            
        # 次のステップの提案
        print(f"\n[NEXT] 次のステップ:")
        print(f"1. 生成コードを確認: cat {code_file_path}")
        if review_result:
            print(f"2. レビュー結果を確認: cat {review_file_path}")
        print(f"3. コードをテスト・統合")
        
        return True
        
    def _generate_code_with_deepseek(self, instruction) -> Tuple[str, bool]:
        """DeepSeekでコード生成"""
        try:
            # 命令書をDeepSeek用のプロンプトに変換
            prompt = self._create_deepseek_prompt(instruction)
            
            print(f"[REQUEST] DeepSeek にリクエスト送信...")
            response = self.slm_client.generate_code(prompt)
            
            if response:
                print(f"[SUCCESS] コード生成完了 ({len(response)} 文字)")
                return response, True
            else:
                print(f"[ERROR] 空のレスポンスです")
                return "", False
                
        except Exception as e:
            print(f"[ERROR] DeepSeek API エラー: {e}")
            return "", False
            
    def _create_deepseek_prompt(self, instruction) -> str:
        """DeepSeek用のプロンプトを作成"""
        prompt_parts = [
            f"以下の仕様に従って、Pythonで{instruction.function_name}関数を実装してください。",
            "",
            "## 仕様:",
            json.dumps(instruction.requirements, ensure_ascii=False, indent=2),
            "",
            "## 要求事項:",
            "- PEP 8準拠のコーディングスタイル",
            "- 型ヒント必須",
            "- docstringにはGoogle Style使用",
            "- 適切なエラーハンドリング",
            "- 日本語コメントで複雑な処理を説明",
            "",
            "実装コードのみを返してください（説明は不要）:"
        ]
        
        return "\n".join(prompt_parts)
        
    def _review_code_with_claude(self, instruction, code: str) -> Tuple[Dict[str, Any], bool]:
        """Claudeでコードレビュー"""
        try:
            review_prompt = self._create_claude_review_prompt(instruction, code)
            
            print(f"[REQUEST] Claude にレビュー依頼...")
            review_response = self.llm_client.review_code(review_prompt)
            
            if review_response:
                print(f"[SUCCESS] レビュー完了")
                
                # レビュー結果をパース
                review_result = {
                    "instruction_id": instruction.id,
                    "function_name": instruction.function_name,
                    "review_date": datetime.now().isoformat(),
                    "original_code": code,
                    "claude_review": review_response,
                    "review_summary": self._extract_review_summary(review_response)
                }
                
                return review_result, True
            else:
                return {}, False
                
        except Exception as e:
            print(f"[ERROR] Claude API エラー: {e}")
            return {}, False
            
    def _create_claude_review_prompt(self, instruction, code: str) -> str:
        """Claude用レビュープロンプトを作成"""
        prompt_parts = [
            "以下のコードをレビューしてください。",
            "",
            f"## 元の仕様:",
            json.dumps(instruction.requirements, ensure_ascii=False, indent=2),
            "",
            f"## 生成されたコード:",
            "```python",
            code,
            "```",
            "",
            "## レビュー観点:",
            "1. 仕様との適合性",
            "2. コード品質（可読性、保守性）",
            "3. エラーハンドリング",
            "4. セキュリティ",
            "5. パフォーマンス",
            "6. テスト可能性",
            "",
            "## 求める回答形式:",
            "- 総合評価（A-F）",
            "- 良い点",
            "- 改善点",
            "- 重要な修正提案（あれば）",
            "- 最終コード（修正が必要な場合）"
        ]
        
        return "\n".join(prompt_parts)
        
    def _extract_review_summary(self, review_text: str) -> Dict[str, str]:
        """レビューテキストから要約を抽出"""
        # シンプルな実装（後で改善可能）
        return {
            "status": "reviewed",
            "summary": review_text[:200] + "..." if len(review_text) > 200 else review_text
        }
        
    def _save_generated_code(self, instruction, code: str) -> Path:
        """生成されたコードを保存"""
        filename = f"{instruction.function_name}_{instruction.id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        file_path = self.code_output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f'"""\n')
            f.write(f'生成日時: {datetime.now().isoformat()}\n')
            f.write(f'命令書ID: {instruction.id}\n')
            f.write(f'機能名: {instruction.function_name}\n')
            f.write(f'生成AI: DeepSeek-Coder\n')
            f.write(f'"""\n\n')
            f.write(code)
            
        return file_path
        
    def _save_review_result(self, instruction, review_result: Dict[str, Any]) -> Path:
        """レビュー結果を保存"""
        filename = f"review_{instruction.function_name}_{instruction.id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = self.reviews_output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(review_result, f, ensure_ascii=False, indent=2)
            
        return file_path
        
    def list_ready_instructions(self) -> None:
        """実行可能な命令書一覧を表示"""
        approved_instructions = self.instruction_manager.get_approved_instructions()
        
        if not approved_instructions:
            print("実行可能な承認済み命令書がありません。")
            return
            
        print(f"\n[LIST] 実行可能な命令書一覧:")
        print("=" * 80)
        print(f"{'ID':<20} {'機能名':<25} {'承認者':<15} {'承認日時':<20}")
        print("-" * 80)
        
        for instruction in sorted(approved_instructions, key=lambda x: x.approved_at, reverse=True):
            id_short = instruction.id[:18] + ".."
            function_name = (instruction.function_name[:23] + "..") if len(instruction.function_name) > 25 else instruction.function_name
            approver = instruction.approved_by or "-"
            approved_date = instruction.approved_at.strftime('%Y-%m-%d %H:%M')
            
            print(f"{id_short:<20} {function_name:<25} {approver:<15} {approved_date:<20}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="LLM×SLM ワークフロー実行エンジン",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 実行可能な命令書一覧
  python -m src.workflow.executor list
  
  # 命令書実行（レビューあり）
  python -m src.workflow.executor execute abc123def456
  
  # 命令書実行（レビューなし）
  python -m src.workflow.executor execute abc123def456 --skip-review
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')
    
    # execute コマンド
    execute_parser = subparsers.add_parser('execute', help='命令書実行')
    execute_parser.add_argument('instruction_id', help='命令書ID')
    execute_parser.add_argument('--skip-review', action='store_true', help='Claudeレビューをスキップ')
    
    # list コマンド
    list_parser = subparsers.add_parser('list', help='実行可能な命令書一覧')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    try:
        executor = WorkflowExecutor()
        
        if args.command == 'execute':
            success = executor.execute_instruction(args.instruction_id, args.skip_review)
            if not success:
                sys.exit(1)
        elif args.command == 'list':
            executor.list_ready_instructions()
            
    except KeyboardInterrupt:
        print(f"\n[CANCEL] 実行をキャンセルしました")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] エラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
"""
CMD用命令書表示・承認ツール

完全にコマンドラインで命令書の表示、編集、承認を行う
"""

import json
import argparse
import sys
import subprocess
import tempfile
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# プロジェクトのルートパスを追加
sys.path.append(str(Path(__file__).parent.parent))

from core.instruction_manager import InstructionManager, InstructionStatus


class InstructionViewer:
    """命令書表示・管理ツール"""
    
    def __init__(self):
        self.instruction_manager = InstructionManager()
        
    def show_instruction(self, instruction_id: str) -> None:
        """命令書の詳細表示"""
        instruction = self.instruction_manager.get_instruction(instruction_id)
        if not instruction:
            print(f"[ERROR] 命令書が見つかりません: {instruction_id}")
            return
            
        print(f"\n[INFO] LLM×SLM 命令書詳細")
        print("=" * 60)
        print(f"ID: {instruction.id}")
        print(f"機能名: {instruction.function_name}")
        print(f"ステータス: {instruction.status.value}")
        print(f"作成日時: {instruction.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"更新日時: {instruction.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"バージョン: {instruction.version}")
        print(f"ハッシュ: {instruction.hash}")
        
        if instruction.approved_by:
            print(f"承認者: {instruction.approved_by}")
            print(f"承認日時: {instruction.approved_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
        print("\n[REQUIREMENTS] 要件:")
        print("-" * 40)
        print(json.dumps(instruction.requirements, ensure_ascii=False, indent=2))
        
        if instruction.review_comments:
            print(f"\n[COMMENTS] レビューコメント ({len(instruction.review_comments)}件):")
            print("-" * 40)
            for i, comment in enumerate(instruction.review_comments, 1):
                print(f"{i}. {comment['reviewer']} ({comment['timestamp']})")
                print(f"   {comment['comment']}")
                print()
                
    def list_instructions(self, status: Optional[str] = None) -> None:
        """命令書一覧表示"""
        if status:
            try:
                status_enum = InstructionStatus(status)
                instructions = self.instruction_manager.get_instructions_by_status(status_enum)
                print(f"\n[LIST] {status}の命令書一覧:")
            except ValueError:
                print(f"[ERROR] 無効なステータス: {status}")
                print(f"有効な値: {[s.value for s in InstructionStatus]}")
                return
        else:
            instructions = list(self.instruction_manager.instructions.values())
            print(f"\n[LIST] 全命令書一覧:")
            
        if not instructions:
            print("命令書がありません。")
            return
            
        print("=" * 100)
        print(f"{'ID':<20} {'機能名':<25} {'ステータス':<15} {'作成日':<20} {'承認者':<15}")
        print("-" * 100)
        
        for instruction in sorted(instructions, key=lambda x: x.created_at, reverse=True):
            id_short = instruction.id[:18] + ".."
            function_name = (instruction.function_name[:23] + "..") if len(instruction.function_name) > 25 else instruction.function_name
            status_str = instruction.status.value
            created_date = instruction.created_at.strftime('%Y-%m-%d %H:%M')
            approver = instruction.approved_by or "-"
            
            print(f"{id_short:<20} {function_name:<25} {status_str:<15} {created_date:<20} {approver:<15}")
            
    def edit_instruction(self, instruction_id: str) -> None:
        """命令書をエディタで編集"""
        instruction = self.instruction_manager.get_instruction(instruction_id)
        if not instruction:
            print(f"[ERROR] 命令書が見つかりません: {instruction_id}")
            return
            
        if instruction.status not in [InstructionStatus.DRAFT, InstructionStatus.PENDING_REVIEW]:
            print(f"[WARNING] 編集不可なステータスです: {instruction.status.value}")
            response = input("強制的に編集しますか? (y/N): ").strip().lower()
            if response != 'y':
                return
                
        # 一時ファイルに書き出し
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            temp_file = f.name
            json.dump(instruction.requirements, f, ensure_ascii=False, indent=2)
            
        print(f"[EDIT] エディタで編集中... ({temp_file})")
        
        # エディタを開く
        editor = os.environ.get('EDITOR', 'notepad' if os.name == 'nt' else 'nano')
        try:
            subprocess.run([editor, temp_file], check=True)
        except subprocess.CalledProcessError:
            print(f"[ERROR] エディタの起動に失敗しました: {editor}")
            os.unlink(temp_file)
            return
        except FileNotFoundError:
            print(f"[ERROR] エディタが見つかりません: {editor}")
            print("環境変数EDITORを設定するか、notepad/nanoを使用してください")
            os.unlink(temp_file)
            return
            
        # 編集後のファイルを読み込み
        try:
            with open(temp_file, 'r', encoding='utf-8') as f:
                new_requirements = json.load(f)
                
            # 更新
            if self.instruction_manager.update_instruction(instruction_id, new_requirements):
                print("[SUCCESS] 命令書を更新しました！")
            else:
                print("[ERROR] 更新に失敗しました")
                
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON形式エラー: {e}")
        finally:
            os.unlink(temp_file)
            
    def approve_instruction(self, instruction_id: str, approver: str) -> None:
        """命令書を承認"""
        instruction = self.instruction_manager.get_instruction(instruction_id)
        if not instruction:
            print(f"[ERROR] 命令書が見つかりません: {instruction_id}")
            return
            
        if instruction.status != InstructionStatus.PENDING_REVIEW:
            print(f"[WARNING] 承認できないステータスです: {instruction.status.value}")
            return
            
        # 承認前の確認表示
        print(f"\n[APPROVE] 承認対象の命令書:")
        self.show_instruction(instruction_id)
        
        print(f"\n[QUESTION] この命令書を承認しますか?")
        print(f"承認者: {approver}")
        response = input("承認する場合は 'approve' と入力: ").strip()
        
        if response == "approve":
            if self.instruction_manager.approve_instruction(instruction_id, approver):
                print(f"[SUCCESS] 命令書を承認しました！")
                print(f"次のステップ: python -m src.workflow.executor {instruction_id}")
            else:
                print("[ERROR] 承認処理に失敗しました")
        else:
            print("承認をキャンセルしました")
            
    def reject_instruction(self, instruction_id: str, reason: str, reviewer: str) -> None:
        """命令書を却下"""
        instruction = self.instruction_manager.get_instruction(instruction_id)
        if not instruction:
            print(f"[ERROR] 命令書が見つかりません: {instruction_id}")
            return
            
        if self.instruction_manager.reject_instruction(instruction_id, reason, reviewer):
            print(f"[REJECT] 命令書を却下しました")
            print(f"却下理由: {reason}")
        else:
            print("[ERROR] 却下処理に失敗しました")
            
    def show_summary(self) -> None:
        """システム状況サマリー表示"""
        summary = self.instruction_manager.get_instruction_summary()
        
        print(f"\n[STATUS] LLM×SLM システム状況")
        print("=" * 40)
        
        total = sum(summary.values())
        print(f"総命令書数: {total}")
        print()
        
        status_labels = {
            'draft': '[DRAFT]',
            'pending_review': '[PENDING]',
            'under_review': '[REVIEW]',
            'approved': '[APPROVED]',
            'rejected': '[REJECTED]',
            'executed': '[EXECUTED]',
            'archived': '[ARCHIVED]'
        }
        
        for status, count in summary.items():
            label = status_labels.get(status, '[UNKNOWN]')
            print(f"{label} {status}: {count}件")
            
    def add_comment(self, instruction_id: str, comment: str, reviewer: str) -> None:
        """レビューコメントを追加"""
        instruction = self.instruction_manager.get_instruction(instruction_id)
        if not instruction:
            print(f"[ERROR] 命令書が見つかりません: {instruction_id}")
            return
            
        instruction.add_review_comment(comment, reviewer)
        self.instruction_manager._save_instruction(instruction)
        
        print(f"[COMMENT] コメントを追加しました")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="LLM×SLM 命令書表示・管理ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 命令書詳細表示
  python -m src.cli.instruction_viewer show abc123def456
  
  # 命令書一覧
  python -m src.cli.instruction_viewer list
  python -m src.cli.instruction_viewer list --status pending_review
  
  # 命令書編集
  python -m src.cli.instruction_viewer edit abc123def456
  
  # 命令書承認
  python -m src.cli.instruction_viewer approve abc123def456 --approver "山田太郎"
  
  # 命令書却下
  python -m src.cli.instruction_viewer reject abc123def456 --reason "要件が不明確" --reviewer "山田太郎"
  
  # システム状況
  python -m src.cli.instruction_viewer summary
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')
    
    # show コマンド
    show_parser = subparsers.add_parser('show', help='命令書詳細表示')
    show_parser.add_argument('instruction_id', help='命令書ID')
    
    # list コマンド
    list_parser = subparsers.add_parser('list', help='命令書一覧表示')
    list_parser.add_argument('--status', help='ステータスフィルター')
    
    # edit コマンド
    edit_parser = subparsers.add_parser('edit', help='命令書編集')
    edit_parser.add_argument('instruction_id', help='命令書ID')
    
    # approve コマンド
    approve_parser = subparsers.add_parser('approve', help='命令書承認')
    approve_parser.add_argument('instruction_id', help='命令書ID')
    approve_parser.add_argument('--approver', required=True, help='承認者名')
    
    # reject コマンド
    reject_parser = subparsers.add_parser('reject', help='命令書却下')
    reject_parser.add_argument('instruction_id', help='命令書ID')
    reject_parser.add_argument('--reason', required=True, help='却下理由')
    reject_parser.add_argument('--reviewer', required=True, help='レビューアー名')
    
    # comment コマンド
    comment_parser = subparsers.add_parser('comment', help='コメント追加')
    comment_parser.add_argument('instruction_id', help='命令書ID')
    comment_parser.add_argument('--comment', required=True, help='コメント内容')
    comment_parser.add_argument('--reviewer', required=True, help='レビューアー名')
    
    # summary コマンド
    summary_parser = subparsers.add_parser('summary', help='システム状況表示')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    viewer = InstructionViewer()
    
    try:
        if args.command == 'show':
            viewer.show_instruction(args.instruction_id)
        elif args.command == 'list':
            viewer.list_instructions(args.status)
        elif args.command == 'edit':
            viewer.edit_instruction(args.instruction_id)
        elif args.command == 'approve':
            viewer.approve_instruction(args.instruction_id, args.approver)
        elif args.command == 'reject':
            viewer.reject_instruction(args.instruction_id, args.reason, args.reviewer)
        elif args.command == 'comment':
            viewer.add_comment(args.instruction_id, args.comment, args.reviewer)
        elif args.command == 'summary':
            viewer.show_summary()
    except KeyboardInterrupt:
        print(f"\n[CANCEL] 操作をキャンセルしました")
    except Exception as e:
        print(f"[ERROR] エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
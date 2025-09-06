"""
人間承認用Webインターフェース

Streamlitを使用した命令書の確認・編集・承認UI
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# プロジェクトのルートパスを追加
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.instruction_manager import InstructionManager, InstructionStatus


class ApprovalInterface:
    """承認インターフェース"""
    
    def __init__(self):
        self.instruction_manager = InstructionManager()
        
    def run(self):
        """メインアプリケーションを実行"""
        st.set_page_config(
            page_title="LLM×SLM 命令書承認システム",
            page_icon="🤝",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🤝 LLM×SLM ハイブリッド命令書承認システム")
        
        # サイドバーでモード選択
        mode = st.sidebar.selectbox(
            "モード選択",
            ["📋 承認待ち一覧", "✏️ 命令書詳細編集", "📊 ダッシュボード", "🔍 履歴検索"]
        )
        
        if mode == "📋 承認待ち一覧":
            self._show_pending_approvals()
        elif mode == "✏️ 命令書詳細編集":
            self._show_instruction_editor()
        elif mode == "📊 ダッシュボード":
            self._show_dashboard()
        elif mode == "🔍 履歴検索":
            self._show_history_search()
            
    def _show_pending_approvals(self):
        """承認待ち命令書一覧を表示"""
        st.header("📋 承認待ち命令書一覧")
        
        pending_instructions = self.instruction_manager.get_pending_approvals()
        
        if not pending_instructions:
            st.info("現在承認待ちの命令書はありません。")
            return
            
        for instruction in pending_instructions:
            with st.expander(
                f"🔄 {instruction.function_name} (ID: {instruction.id[:8]}...)"
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**作成日時:**", instruction.created_at.strftime("%Y-%m-%d %H:%M"))
                    st.write("**機能名:**", instruction.function_name)
                    
                    # 要件表示
                    st.subheader("📝 要件詳細")
                    st.json(instruction.requirements)
                    
                    # コメント表示
                    if instruction.review_comments:
                        st.subheader("💬 レビューコメント")
                        for comment in instruction.review_comments:
                            st.write(f"**{comment['reviewer']}** ({comment['timestamp']}):")
                            st.write(comment['comment'])
                    
                with col2:
                    st.subheader("🔧 アクション")
                    
                    # 編集ボタン
                    if st.button(f"編集", key=f"edit_{instruction.id}"):
                        st.session_state['edit_instruction_id'] = instruction.id
                        st.experimental_rerun()
                    
                    # 承認ボタン
                    approver = st.text_input(
                        "承認者名", 
                        key=f"approver_{instruction.id}",
                        placeholder="あなたの名前"
                    )
                    
                    if st.button(
                        "✅ 承認", 
                        key=f"approve_{instruction.id}",
                        type="primary"
                    ):
                        if approver:
                            if self.instruction_manager.approve_instruction(
                                instruction.id, approver
                            ):
                                st.success(f"命令書 {instruction.function_name} を承認しました！")
                                st.experimental_rerun()
                            else:
                                st.error("承認処理に失敗しました。")
                        else:
                            st.warning("承認者名を入力してください。")
                    
                    # 却下セクション
                    st.subheader("❌ 却下")
                    reject_reason = st.text_area(
                        "却下理由",
                        key=f"reject_reason_{instruction.id}",
                        placeholder="却下理由を詳しく記述してください..."
                    )
                    
                    if st.button(
                        "❌ 却下", 
                        key=f"reject_{instruction.id}"
                    ):
                        if reject_reason and approver:
                            if self.instruction_manager.reject_instruction(
                                instruction.id, reject_reason, approver
                            ):
                                st.warning(f"命令書 {instruction.function_name} を却下しました。")
                                st.experimental_rerun()
                            else:
                                st.error("却下処理に失敗しました。")
                        else:
                            st.warning("却下理由と名前を入力してください。")
                            
    def _show_instruction_editor(self):
        """命令書詳細編集画面"""
        st.header("✏️ 命令書詳細編集")
        
        # 編集対象の命令書選択
        instruction_id = st.session_state.get('edit_instruction_id', None)
        
        if not instruction_id:
            # 命令書選択
            all_instructions = list(self.instruction_manager.instructions.values())
            if not all_instructions:
                st.info("編集可能な命令書がありません。")
                return
                
            options = [
                f"{inst.function_name} ({inst.id[:8]}...) - {inst.status.value}"
                for inst in all_instructions
            ]
            
            selected = st.selectbox("編集する命令書を選択:", options)
            if selected:
                instruction_id = selected.split('(')[1].split('...')[0]
                # 完全なIDを取得
                for inst in all_instructions:
                    if inst.id.startswith(instruction_id):
                        instruction_id = inst.id
                        break
        
        if instruction_id:
            instruction = self.instruction_manager.get_instruction(instruction_id)
            if not instruction:
                st.error("指定された命令書が見つかりません。")
                return
                
            st.subheader(f"📝 {instruction.function_name} の編集")
            
            # 基本情報表示
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**ID:**", instruction.id[:16] + "...")
            with col2:
                st.write("**ステータス:**", instruction.status.value)
            with col3:
                st.write("**バージョン:**", instruction.version)
            
            # 関数名編集
            new_function_name = st.text_input(
                "関数名",
                value=instruction.function_name,
                key="edit_function_name"
            )
            
            # 要件編集
            st.subheader("📋 要件編集")
            requirements_json = st.text_area(
                "要件 (JSON形式)",
                value=json.dumps(instruction.requirements, ensure_ascii=False, indent=2),
                height=400,
                key="edit_requirements"
            )
            
            # プレビュー
            try:
                parsed_requirements = json.loads(requirements_json)
                st.subheader("👀 プレビュー")
                st.json(parsed_requirements)
                
                # 保存ボタン
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("💾 保存", type="primary"):
                        if instruction.function_name != new_function_name:
                            instruction.function_name = new_function_name
                        
                        if self.instruction_manager.update_instruction(
                            instruction.id, parsed_requirements
                        ):
                            st.success("命令書を更新しました！")
                            st.experimental_rerun()
                        else:
                            st.error("更新に失敗しました。")
                            
                with col2:
                    if st.button("🔄 リセット"):
                        st.experimental_rerun()
                        
            except json.JSONDecodeError as e:
                st.error(f"JSON形式エラー: {str(e)}")
                
    def _show_dashboard(self):
        """ダッシュボード表示"""
        st.header("📊 システムダッシュボード")
        
        # サマリー統計
        summary = self.instruction_manager.get_instruction_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 承認待ち", summary.get('pending_review', 0))
        with col2:
            st.metric("✅ 承認済み", summary.get('approved', 0))
        with col3:
            st.metric("🚀 実行済み", summary.get('executed', 0))
        with col4:
            st.metric("❌ 却下", summary.get('rejected', 0))
            
        # ステータス別詳細
        st.subheader("📈 ステータス別詳細")
        
        for status, count in summary.items():
            if count > 0:
                with st.expander(f"{status}: {count}件"):
                    instructions = self.instruction_manager.get_instructions_by_status(
                        InstructionStatus(status)
                    )
                    
                    for instruction in instructions:
                        st.write(f"- {instruction.function_name} (ID: {instruction.id[:8]}...)")
                        st.write(f"  作成: {instruction.created_at.strftime('%Y-%m-%d %H:%M')}")
                        if instruction.approved_by:
                            st.write(f"  承認者: {instruction.approved_by}")
                            
    def _show_history_search(self):
        """履歴検索画面"""
        st.header("🔍 命令書履歴検索")
        
        # 検索フィルター
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("関数名で検索", placeholder="関数名を入力...")
        with col2:
            status_filter = st.selectbox(
                "ステータスフィルター",
                ["すべて"] + [status.value for status in InstructionStatus]
            )
            
        # 検索結果
        all_instructions = list(self.instruction_manager.instructions.values())
        
        # フィルタリング
        filtered_instructions = all_instructions
        
        if search_term:
            filtered_instructions = [
                inst for inst in filtered_instructions
                if search_term.lower() in inst.function_name.lower()
            ]
            
        if status_filter != "すべて":
            filtered_instructions = [
                inst for inst in filtered_instructions
                if inst.status.value == status_filter
            ]
            
        # 結果表示
        st.write(f"**検索結果: {len(filtered_instructions)}件**")
        
        for instruction in sorted(filtered_instructions, key=lambda x: x.created_at, reverse=True):
            with st.expander(
                f"{instruction.function_name} - {instruction.status.value} "
                f"({instruction.created_at.strftime('%Y-%m-%d')})"
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**ID:**", instruction.id)
                    st.write("**作成日:**", instruction.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    st.write("**更新日:**", instruction.updated_at.strftime('%Y-%m-%d %H:%M:%S'))
                    if instruction.approved_by:
                        st.write("**承認者:**", instruction.approved_by)
                    
                    # 要件プレビュー
                    with st.expander("要件詳細"):
                        st.json(instruction.requirements)
                        
                with col2:
                    if instruction.status in [InstructionStatus.DRAFT, InstructionStatus.PENDING_REVIEW]:
                        if st.button(f"編集", key=f"history_edit_{instruction.id}"):
                            st.session_state['edit_instruction_id'] = instruction.id
                            st.experimental_rerun()


def main():
    """メイン関数"""
    app = ApprovalInterface()
    app.run()


if __name__ == "__main__":
    main()
"""
命令書管理システム

人間承認ワークフローの中核となる命令書の生成・編集・承認管理を行います。
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum
import hashlib

from loguru import logger


class InstructionStatus(Enum):
    """命令書のステータス"""
    DRAFT = "draft"  # ドラフト（Claude生成直後）
    PENDING_REVIEW = "pending_review"  # レビュー待ち
    UNDER_REVIEW = "under_review"  # レビュー中
    APPROVED = "approved"  # 承認済み
    REJECTED = "rejected"  # 却下
    EXECUTED = "executed"  # 実行済み
    ARCHIVED = "archived"  # アーカイブ済み


class Instruction:
    """命令書オブジェクト"""
    
    def __init__(self, 
                 function_name: str,
                 requirements: Dict[str, Any],
                 instruction_id: Optional[str] = None):
        self.id = instruction_id or str(uuid.uuid4())
        self.function_name = function_name
        self.requirements = requirements
        self.status = InstructionStatus.DRAFT
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.approved_at: Optional[datetime] = None
        self.approved_by: Optional[str] = None
        self.version = 1
        self.hash = self._calculate_hash()
        self.review_comments: List[Dict[str, Any]] = []
        
    def _calculate_hash(self) -> str:
        """命令書の内容ハッシュを計算"""
        content = {
            "function_name": self.function_name,
            "requirements": self.requirements
        }
        return hashlib.sha256(
            json.dumps(content, sort_keys=True).encode()
        ).hexdigest()[:16]
        
    def update_requirements(self, requirements: Dict[str, Any]) -> None:
        """要件を更新"""
        self.requirements = requirements
        self.updated_at = datetime.now()
        self.version += 1
        self.hash = self._calculate_hash()
        
    def add_review_comment(self, comment: str, reviewer: str) -> None:
        """レビューコメントを追加"""
        self.review_comments.append({
            "comment": comment,
            "reviewer": reviewer,
            "timestamp": datetime.now().isoformat()
        })
        
    def approve(self, approver: str) -> None:
        """命令書を承認"""
        self.status = InstructionStatus.APPROVED
        self.approved_at = datetime.now()
        self.approved_by = approver
        self.updated_at = datetime.now()
        
    def reject(self, reason: str, reviewer: str) -> None:
        """命令書を却下"""
        self.status = InstructionStatus.REJECTED
        self.add_review_comment(f"却下理由: {reason}", reviewer)
        self.updated_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            "id": self.id,
            "function_name": self.function_name,
            "requirements": self.requirements,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "approved_by": self.approved_by,
            "version": self.version,
            "hash": self.hash,
            "review_comments": self.review_comments
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Instruction':
        """辞書から命令書オブジェクトを復元"""
        instruction = cls(
            function_name=data["function_name"],
            requirements=data["requirements"],
            instruction_id=data["id"]
        )
        
        instruction.status = InstructionStatus(data["status"])
        instruction.created_at = datetime.fromisoformat(data["created_at"])
        instruction.updated_at = datetime.fromisoformat(data["updated_at"])
        instruction.version = data["version"]
        instruction.hash = data["hash"]
        instruction.review_comments = data.get("review_comments", [])
        
        if data.get("approved_at"):
            instruction.approved_at = datetime.fromisoformat(data["approved_at"])
        instruction.approved_by = data.get("approved_by")
        
        return instruction


class InstructionManager:
    """命令書管理システム"""
    
    def __init__(self, storage_path: str = "data/instructions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.instructions: Dict[str, Instruction] = {}
        self._load_all_instructions()
        
    def _get_instruction_file_path(self, instruction_id: str) -> Path:
        """命令書ファイルのパスを取得"""
        return self.storage_path / f"{instruction_id}.json"
        
    def _save_instruction(self, instruction: Instruction) -> None:
        """命令書をファイルに保存"""
        file_path = self._get_instruction_file_path(instruction.id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(instruction.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info(f"命令書保存: {instruction.id} - {instruction.function_name}")
        
    def _load_instruction(self, instruction_id: str) -> Optional[Instruction]:
        """ファイルから命令書を読み込み"""
        file_path = self._get_instruction_file_path(instruction_id)
        if not file_path.exists():
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Instruction.from_dict(data)
        except Exception as e:
            logger.error(f"命令書読み込みエラー {instruction_id}: {e}")
            return None
            
    def _load_all_instructions(self) -> None:
        """全命令書を読み込み"""
        for file_path in self.storage_path.glob("*.json"):
            instruction_id = file_path.stem
            instruction = self._load_instruction(instruction_id)
            if instruction:
                self.instructions[instruction_id] = instruction
                
    def create_instruction(self, 
                          function_name: str,
                          requirements: Dict[str, Any]) -> Instruction:
        """新しい命令書を作成"""
        instruction = Instruction(function_name, requirements)
        self.instructions[instruction.id] = instruction
        self._save_instruction(instruction)
        
        logger.info(f"命令書作成: {instruction.id} - {function_name}")
        return instruction
        
    def get_instruction(self, instruction_id: str) -> Optional[Instruction]:
        """命令書を取得"""
        return self.instructions.get(instruction_id)
        
    def update_instruction(self, 
                          instruction_id: str,
                          requirements: Dict[str, Any]) -> bool:
        """命令書を更新"""
        instruction = self.get_instruction(instruction_id)
        if not instruction:
            return False
            
        instruction.update_requirements(requirements)
        self._save_instruction(instruction)
        
        logger.info(f"命令書更新: {instruction_id}")
        return True
        
    def approve_instruction(self, 
                           instruction_id: str,
                           approver: str) -> bool:
        """命令書を承認"""
        instruction = self.get_instruction(instruction_id)
        if not instruction:
            return False
            
        instruction.approve(approver)
        self._save_instruction(instruction)
        
        logger.info(f"命令書承認: {instruction_id} by {approver}")
        return True
        
    def reject_instruction(self, 
                          instruction_id: str,
                          reason: str,
                          reviewer: str) -> bool:
        """命令書を却下"""
        instruction = self.get_instruction(instruction_id)
        if not instruction:
            return False
            
        instruction.reject(reason, reviewer)
        self._save_instruction(instruction)
        
        logger.warning(f"命令書却下: {instruction_id} - {reason}")
        return True
        
    def get_instructions_by_status(self, 
                                  status: InstructionStatus) -> List[Instruction]:
        """ステータス別に命令書を取得"""
        return [
            instruction for instruction in self.instructions.values()
            if instruction.status == status
        ]
        
    def get_pending_approvals(self) -> List[Instruction]:
        """承認待ちの命令書を取得"""
        return self.get_instructions_by_status(InstructionStatus.PENDING_REVIEW)
        
    def get_approved_instructions(self) -> List[Instruction]:
        """承認済みの命令書を取得"""
        return self.get_instructions_by_status(InstructionStatus.APPROVED)
        
    def mark_as_executed(self, instruction_id: str) -> bool:
        """命令書を実行済みにマーク"""
        instruction = self.get_instruction(instruction_id)
        if not instruction or instruction.status != InstructionStatus.APPROVED:
            return False
            
        instruction.status = InstructionStatus.EXECUTED
        instruction.updated_at = datetime.now()
        self._save_instruction(instruction)
        
        logger.info(f"命令書実行完了: {instruction_id}")
        return True
        
    def get_instruction_summary(self) -> Dict[str, int]:
        """命令書のステータス別サマリーを取得"""
        summary = {}
        for status in InstructionStatus:
            summary[status.value] = len(self.get_instructions_by_status(status))
        return summary
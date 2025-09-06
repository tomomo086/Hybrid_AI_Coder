# LLM×SLM ハイブリッドペアプログラミング - アーキテクチャ・設計パターン

## システム全体アーキテクチャ

### 基本設計思想
- **人間中心設計**: 重要な判断は必ず人間が行う
- **責任分離**: LLMとSLMの役割を明確に分離
- **段階的承認**: セキュリティと品質のための多段階チェック
- **トレーサビリティ**: 全ての操作履歴を記録・追跡可能

### コンポーネント構成
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     人間UI      │    │   Claude LLM    │    │  DeepSeek SLM   │
│  (承認・監督)    │    │  (設計・レビュー) │    │   (実装・生成)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌────────────────────────────────────────────────────────────────┐
│                    ハイブリッドペアプログラミング                     │
│                         システムコア                              │
└────────────────────────────────────────────────────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   命令書管理     │    │  ワークフロー    │    │   品質管理      │
│   システム       │    │   制御          │    │   システム       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 主要な設計パターン

### 1. Command Pattern（コマンドパターン）
CLIの各操作をコマンドオブジェクトとして実装

```python
# hybrid_pair.py での実装例
class HybridPairCLI:
    def run_command(self, module_path: str, args: List[str]) -> int:
        """サブコマンドを実行"""
        cmd = [sys.executable, '-m', module_path] + args
        return subprocess.run(cmd, cwd=self.project_root).returncode

    # 各コマンドは独立したモジュールとして実装
    # - src.cli.instruction_creator (create コマンド)
    # - src.cli.instruction_viewer (list, review コマンド)
    # - src.workflow.executor (execute コマンド)
```

### 2. State Machine Pattern（状態機械パターン）
命令書のライフサイクル管理

```python
class InstructionStatus(Enum):
    DRAFT = "draft"           # Claude生成直後
    PENDING_REVIEW = "pending_review"  # レビュー待ち
    UNDER_REVIEW = "under_review"      # レビュー中
    APPROVED = "approved"              # 承認済み
    REJECTED = "rejected"              # 却下
    EXECUTED = "executed"              # 実行済み
    ARCHIVED = "archived"              # アーカイブ済み

# 状態遷移制御
def approve_instruction(self, instruction_id: str, approver: str):
    if self.status != InstructionStatus.PENDING_REVIEW:
        raise ValueError("承認可能な状態ではありません")
    self.status = InstructionStatus.APPROVED
    self.approved_by = approver
    self.approved_at = datetime.now()
```

### 3. Factory Pattern（ファクトリーパターン）
APIクライアントの生成管理

```python
class APIClientFactory:
    @staticmethod
    def create_llm_client(config: Dict[str, Any]) -> LLMClient:
        """LLMクライアントの生成"""
        provider = config.get("provider", "claude")
        if provider == "claude":
            return ClaudeClient(config)
        elif provider == "openai":
            return OpenAIClient(config)
        else:
            raise ValueError(f"未対応のLLMプロバイダー: {provider}")
    
    @staticmethod
    def create_slm_client(config: Dict[str, Any]) -> SLMClient:
        """SLMクライアントの生成"""
        provider = config.get("provider", "lm_studio")
        if provider == "lm_studio":
            return LMStudioClient(config)
        else:
            raise ValueError(f"未対応のSLMプロバイダー: {provider}")
```

### 4. Observer Pattern（オブザーバーパターン）
ワークフロー進捗の監視・通知

```python
from typing import List, Callable

class WorkflowExecutor:
    def __init__(self):
        self._observers: List[Callable[[str, Dict], None]] = []
    
    def add_observer(self, observer: Callable[[str, Dict], None]):
        """進捗監視者を追加"""
        self._observers.append(observer)
    
    def notify_progress(self, event: str, data: Dict[str, Any]):
        """進捗を通知"""
        for observer in self._observers:
            observer(event, data)
    
    def execute_instruction(self, instruction_id: str):
        self.notify_progress("started", {"instruction_id": instruction_id})
        # 実行処理
        self.notify_progress("completed", {"instruction_id": instruction_id})

# 使用例
def log_progress(event: str, data: Dict):
    logger.info(f"ワークフロー進捗: {event}, データ: {data}")

executor = WorkflowExecutor()
executor.add_observer(log_progress)
```

### 5. Strategy Pattern（ストラテジーパターン）
コードレビューの戦略選択

```python
from abc import ABC, abstractmethod

class ReviewStrategy(ABC):
    @abstractmethod
    def review(self, code: str) -> Dict[str, Any]:
        pass

class SecurityReviewStrategy(ReviewStrategy):
    def review(self, code: str) -> Dict[str, Any]:
        # セキュリティ観点でのレビュー
        return {"security_issues": [], "score": 85}

class PerformanceReviewStrategy(ReviewStrategy):
    def review(self, code: str) -> Dict[str, Any]:
        # パフォーマンス観点でのレビュー
        return {"performance_issues": [], "score": 90}

class CodeReviewer:
    def __init__(self):
        self.strategies: List[ReviewStrategy] = []
    
    def add_strategy(self, strategy: ReviewStrategy):
        self.strategies.append(strategy)
    
    def review_code(self, code: str) -> Dict[str, Any]:
        results = {}
        for strategy in self.strategies:
            review_result = strategy.review(code)
            results[strategy.__class__.__name__] = review_result
        return results
```

### 6. Template Method Pattern（テンプレートメソッドパターン）
ワークフロー実行の骨格定義

```python
from abc import ABC, abstractmethod

class AbstractWorkflow(ABC):
    """ワークフロー実行の骨格"""
    
    def execute(self, instruction_id: str) -> bool:
        """テンプレートメソッド - 実行順序を定義"""
        try:
            # 1. 前処理
            if not self.pre_process(instruction_id):
                return False
            
            # 2. メイン処理（サブクラスで実装）
            result = self.main_process(instruction_id)
            
            # 3. 後処理
            self.post_process(instruction_id, result)
            return True
            
        except Exception as e:
            self.handle_error(instruction_id, e)
            return False
    
    def pre_process(self, instruction_id: str) -> bool:
        """前処理（共通）"""
        logger.info(f"ワークフロー開始: {instruction_id}")
        return True
    
    @abstractmethod
    def main_process(self, instruction_id: str) -> Dict[str, Any]:
        """メイン処理（サブクラスで実装）"""
        pass
    
    def post_process(self, instruction_id: str, result: Dict[str, Any]):
        """後処理（共通）"""
        logger.info(f"ワークフロー完了: {instruction_id}")
    
    def handle_error(self, instruction_id: str, error: Exception):
        """エラーハンドリング（共通）"""
        logger.error(f"ワークフロー失敗: {instruction_id}, エラー: {error}")

# 具体的な実装
class CodeGenerationWorkflow(AbstractWorkflow):
    def main_process(self, instruction_id: str) -> Dict[str, Any]:
        # DeepSeekでのコード生成処理
        return {"generated_code": "...", "status": "success"}
```

## データ管理パターン

### 1. Repository Pattern（リポジトリパターン）
データアクセスの抽象化

```python
from abc import ABC, abstractmethod
from typing import Optional, List

class InstructionRepository(ABC):
    @abstractmethod
    def save(self, instruction: Instruction) -> bool:
        pass
    
    @abstractmethod
    def find_by_id(self, instruction_id: str) -> Optional[Instruction]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Instruction]:
        pass

class JSONInstructionRepository(InstructionRepository):
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
    
    def save(self, instruction: Instruction) -> bool:
        file_path = self.data_dir / f"{instruction.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(instruction.to_dict(), f, ensure_ascii=False, indent=2)
        return True
```

### 2. Value Object Pattern（値オブジェクトパターン）
不変データの表現

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class InstructionRequirements:
    """命令書の要求仕様（不変オブジェクト）"""
    function_name: str
    description: str
    input_params: Dict[str, Any]
    output_format: Dict[str, Any]
    constraints: List[str]
    
    def __post_init__(self):
        if not self.function_name:
            raise ValueError("関数名は必須です")
        if not self.description:
            raise ValueError("説明は必須です")

@dataclass(frozen=True)
class APICredentials:
    """API認証情報（不変オブジェクト）"""
    provider: str
    api_key: str
    endpoint: str
    
    def is_valid(self) -> bool:
        return all([self.provider, self.api_key, self.endpoint])
```

## エラーハンドリングパターン

### 1. Exception Hierarchy（例外階層）
ドメイン固有の例外定義

```python
class HybridPairError(Exception):
    """ベース例外クラス"""
    pass

class InstructionError(HybridPairError):
    """命令書関連エラー"""
    pass

class InstructionNotFoundError(InstructionError):
    """命令書が見つからない"""
    pass

class InstructionNotApprovedError(InstructionError):
    """命令書が未承認"""
    pass

class APIError(HybridPairError):
    """API関連エラー"""
    def __init__(self, provider: str, message: str, status_code: Optional[int] = None):
        self.provider = provider
        self.status_code = status_code
        super().__init__(f"{provider} API エラー: {message}")

class LLMError(APIError):
    """LLM API エラー"""
    pass

class SLMError(APIError):
    """SLM API エラー"""
    pass
```

### 2. Circuit Breaker Pattern（サーキットブレーカーパターン）
API呼び出しの障害対策

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"    # 正常状態
    OPEN = "open"        # 遮断状態
    HALF_OPEN = "half_open"  # 試験状態

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise APIError("Circuit Breaker", "サービス一時停止中")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

## セキュリティパターン

### 1. 入力検証パターン
```python
import re
from typing import Union

class InputValidator:
    @staticmethod
    def validate_instruction_id(instruction_id: str) -> bool:
        """命令書IDの形式検証"""
        if not instruction_id or len(instruction_id) != 32:
            return False
        return bool(re.match(r'^[a-f0-9]{32}$', instruction_id))
    
    @staticmethod
    def validate_function_name(function_name: str) -> bool:
        """関数名の妥当性検証"""
        if not function_name or len(function_name) > 100:
            return False
        return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', function_name))
    
    @staticmethod
    def sanitize_user_input(user_input: str) -> str:
        """ユーザー入力のサニタイズ"""
        # HTMLエスケープ、SQLインジェクション対策など
        import html
        return html.escape(user_input.strip())
```

### 2. 監査ログパターン
```python
class AuditLogger:
    def __init__(self, log_file: Path):
        self.log_file = log_file
    
    def log_action(self, user: str, action: str, resource: str, result: str):
        """監査ログの記録"""
        timestamp = datetime.now().isoformat()
        audit_entry = {
            "timestamp": timestamp,
            "user": user,
            "action": action,
            "resource": resource,
            "result": result,
            "ip_address": self._get_client_ip()
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(audit_entry, ensure_ascii=False) + '\n')
    
    def _get_client_ip(self) -> str:
        # クライアントIPの取得（実装依存）
        return "127.0.0.1"

# 使用例
audit_logger = AuditLogger(Path("logs/audit.log"))
audit_logger.log_action("山田太郎", "命令書承認", "instruction_abc123", "成功")
```

## 設定管理パターン

### 1. Configuration Management（設定管理）
```python
from pydantic import BaseModel, Field
from typing import Optional

class LLMConfig(BaseModel):
    provider: str = "claude"
    api_key: str = Field(..., min_length=1)
    model: str = "claude-3-sonnet-20240229"
    max_tokens: int = Field(8000, ge=1, le=100000)
    temperature: float = Field(0.1, ge=0.0, le=2.0)
    timeout: int = Field(60, ge=1, le=300)

class SLMConfig(BaseModel):
    provider: str = "lm_studio"
    api_endpoint: str = "http://localhost:1234/v1/chat/completions"
    model: str = "deepseek-coder-6.7b-instruct-q5_k_m.gguf"
    max_tokens: int = Field(2000, ge=1, le=8000)
    temperature: float = Field(0.2, ge=0.0, le=2.0)

class SystemConfig(BaseModel):
    name: str = "LLM×SLM ハイブリッドペアプログラミング システム"
    version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"
    llm_config: LLMConfig
    slm_config: SLMConfig

# 使用例
config = SystemConfig.parse_file("config/config.json")
```

これらの設計パターンにより、保守性・拡張性・セキュリティを兼ね備えたシステムアーキテクチャを実現しています。
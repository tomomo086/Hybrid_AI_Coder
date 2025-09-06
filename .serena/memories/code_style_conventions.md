# LLM×SLM ハイブリッドペアプログラミング - コードスタイル・規約

## 全般的なコード規約

### プログラミング言語
- **Python 3.12** を使用
- **UTF-8** エンコーディング統一
- **日本語コメント・ドキュメント** を推奨

### ファイル構成規約
- モジュール名: `snake_case`
- クラス名: `PascalCase`
- 関数・変数名: `snake_case`
- 定数名: `UPPER_CASE`

## Python コードスタイル

### フォーマッター設定
- **Black** (>=23.0.0) を使用
- 行長制限: 88文字（Blackデフォルト）
- 自動フォーマット適用

```bash
# フォーマット実行
black .
black src/
black --check .  # 確認のみ
```

### リンター設定
- **Flake8** (>=6.0.0) を使用
- 基本的なPEP8準拠チェック
- 未使用変数・インポートチェック

```bash
# リンターチェック実行
flake8 .
flake8 src/
flake8 --show-source --statistics .
```

## ドキュメンテーション規約

### Docstring スタイル
```python
"""
関数・クラスの概要（日本語）

詳細説明も日本語で記述します。
複数行の場合は適切に改行します。

Args:
    param1 (str): パラメータ1の説明
    param2 (int, optional): パラメータ2の説明. デフォルトは0.

Returns:
    bool: 戻り値の説明

Raises:
    ValueError: エラーの説明
    ConnectionError: 接続エラーの説明

Example:
    >>> result = sample_function("test", 123)
    >>> print(result)
    True
"""
```

### インラインコメント
```python
# 日本語でのコメント記述を推奨
def process_instruction(instruction_id: str) -> bool:
    # 命令書IDの検証
    if not instruction_id:
        return False
    
    # 承認状態の確認
    status = check_approval_status(instruction_id)
    
    return status == "approved"
```

## 型ヒント規約

### 基本的な型ヒント
```python
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime

def create_instruction(
    function_name: str,
    requirements: Dict[str, Any],
    template_path: Optional[Path] = None
) -> Optional[str]:
    """命令書を作成します"""
    pass

# 戻り値の型も明記
def get_instruction_status(instruction_id: str) -> InstructionStatus:
    """命令書のステータスを取得します"""
    pass
```

### クラス定義での型ヒント
```python
from dataclasses import dataclass
from enum import Enum

class InstructionStatus(Enum):
    """命令書のステータス定義"""
    DRAFT = "draft"
    APPROVED = "approved"
    EXECUTED = "executed"

@dataclass
class Instruction:
    """命令書データクラス"""
    id: str
    function_name: str
    requirements: Dict[str, Any]
    status: InstructionStatus
    created_at: datetime
```

## エラーハンドリング規約

### 例外処理パターン
```python
import logging
from loguru import logger

def safe_api_call(endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """安全なAPI呼び出し"""
    try:
        response = requests.post(endpoint, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        logger.error(f"API呼び出しタイムアウト: {endpoint}")
        return None
        
    except requests.exceptions.ConnectionError:
        logger.error(f"API接続エラー: {endpoint}")
        return None
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTPエラー: {endpoint}, ステータス: {e.response.status_code}")
        return None
        
    except Exception as e:
        logger.exception(f"予期しないエラー: {endpoint}")
        return None
```

### ログ記録規約
```python
from loguru import logger

# 情報ログ
logger.info("命令書を作成しました: {}", instruction_id)

# 警告ログ
logger.warning("API接続が不安定です: {}", endpoint)

# エラーログ
logger.error("命令書の承認に失敗しました: {}", instruction_id)

# デバッグログ
logger.debug("デバッグ情報: {}", debug_data)

# 例外ログ（スタックトレース付き）
logger.exception("予期しないエラーが発生しました")
```

## ファイル・ディレクトリ構成規約

### インポート順序
```python
# 1. 標準ライブラリ
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 2. サードパーティライブラリ
import requests
from loguru import logger
from pydantic import BaseModel

# 3. ローカルモジュール
from src.core.instruction_manager import InstructionManager
from src.api.llm_client import LLMClient
```

### ディレクトリ・ファイル命名規約
```
src/
├── core/                    # コアロジック
│   ├── __init__.py
│   └── instruction_manager.py
├── api/                     # API関連
│   ├── __init__.py
│   ├── llm_client.py       # LLM（Claude）クライアント
│   └── slm_client.py       # SLM（DeepSeek）クライアント
├── cli/                     # CLI関連
│   ├── __init__.py
│   ├── instruction_creator.py
│   └── instruction_viewer.py
└── workflow/                # ワークフロー管理
    ├── __init__.py
    └── executor.py
```

## 設定・データファイル規約

### JSON設定ファイル
```json
{
  "system_config": {
    "name": "LLM×SLM ハイブリッドペアプログラミング システム",
    "version": "0.1.0",
    "debug": true,
    "log_level": "INFO"
  },
  "llm_config": {
    "provider": "claude",
    "api_key": "YOUR_API_KEY_HERE",
    "model": "claude-3-sonnet-20240229"
  }
}
```

### データファイル命名規約
```
data/
├── instructions/           # 命令書保存
│   └── {instruction_id}.json
├── generated_code/        # 生成コード保存
│   └── {instruction_id}/
└── reviews/              # レビュー結果保存
    └── {instruction_id}_review.json
```

## セキュリティ規約

### 機密情報の取り扱い
```python
# ❌ ハードコード禁止
API_KEY = "sk-1234567890abcdef..."

# ✅ 環境変数・設定ファイル使用
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CLAUDE_API_KEY")

# ✅ 設定ファイル使用
with open("config/config.json", "r") as f:
    config = json.load(f)
    api_key = config["llm_config"]["api_key"]
```

### 入力検証
```python
def validate_instruction_id(instruction_id: str) -> bool:
    """命令書IDの検証"""
    if not instruction_id:
        return False
    if len(instruction_id) != 32:  # UUID4の長さ
        return False
    if not instruction_id.replace("-", "").isalnum():
        return False
    return True
```

## テスト規約

### テストファイル命名
```
tests/
├── test_instruction_manager.py
├── test_llm_client.py
├── test_slm_client.py
└── integration/
    └── test_workflow.py
```

### テストケース作成
```python
import pytest
from src.core.instruction_manager import InstructionManager

class TestInstructionManager:
    """命令書管理システムのテスト"""
    
    def setup_method(self):
        """各テストメソッドの前に実行"""
        self.manager = InstructionManager()
    
    def test_create_instruction(self):
        """命令書作成のテスト"""
        instruction_id = self.manager.create_instruction(
            "sample_function", 
            {"description": "テスト機能"}
        )
        assert instruction_id is not None
        assert len(instruction_id) == 32
    
    def test_invalid_instruction_creation(self):
        """不正な命令書作成のテスト"""
        with pytest.raises(ValueError):
            self.manager.create_instruction("", {})
```
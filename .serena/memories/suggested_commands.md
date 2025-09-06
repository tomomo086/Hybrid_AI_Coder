# LLM×SLM ハイブリッドペアプログラミング - 推奨コマンド一覧

## システム管理コマンド

### 初期セットアップ
```bash
# バッチファイル実行（推奨）
run_hybrid_pair.bat setup

# 直接実行
python hybrid_pair.py setup
```

### API接続テスト
```bash
# バッチファイル実行
run_hybrid_pair.bat test

# 直接実行
python hybrid_pair.py test
```

### システム状況確認
```bash
# バッチファイル実行
run_hybrid_pair.bat status

# 直接実行
python hybrid_pair.py status
```

### システム統合テスト
```bash
python run_system_test.py
```

### API接続デバッグ
```bash
python debug_connection.py
```

## 命令書管理コマンド

### 新規命令書作成
```bash
# 基本作成
run_hybrid_pair.bat create <機能名>

# テンプレート指定
run_hybrid_pair.bat create <機能名> --template <テンプレート名>

# 非対話モード
run_hybrid_pair.bat create <機能名> --no-interactive

# 例
run_hybrid_pair.bat create user_authentication_function
python hybrid_pair.py create sample_function --template basic_function
```

### 命令書一覧表示
```bash
# 全体一覧
run_hybrid_pair.bat list

# ステータスフィルター
run_hybrid_pair.bat list --status approved
python hybrid_pair.py list --status pending_review
```

### 命令書詳細確認・編集
```bash
# 詳細確認（エディタ起動）
run_hybrid_pair.bat review <命令書ID>

# 例
run_hybrid_pair.bat review abc123def456
```

### 命令書承認
```bash
# 承認実行
run_hybrid_pair.bat approve <命令書ID> --approver <承認者名>

# 例
run_hybrid_pair.bat approve abc123def456 --approver "山田太郎"
python hybrid_pair.py approve xyz789abc123 --approver "佐藤花子"
```

## コード生成・実行コマンド

### 承認済み命令書の実行
```bash
# 標準実行（Claudeレビュー付き）
run_hybrid_pair.bat execute <命令書ID>

# Claudeレビューをスキップして実行
run_hybrid_pair.bat execute <命令書ID> --skip-review

# 例
run_hybrid_pair.bat execute abc123def456
python hybrid_pair.py execute xyz789abc123 --skip-review
```

## ワークフロー・ヘルプコマンド

### ワークフロー説明表示
```bash
run_hybrid_pair.bat workflow
python hybrid_pair.py workflow

# または引数なしで実行
run_hybrid_pair.bat
python hybrid_pair.py
```

### ヘルプ表示
```bash
# 全体ヘルプ
python hybrid_pair.py --help

# サブコマンドヘルプ
python hybrid_pair.py create --help
python hybrid_pair.py execute --help
python hybrid_pair.py approve --help
```

## 典型的な作業フロー例

### 1. 初回セットアップ
```bash
run_hybrid_pair.bat setup
run_hybrid_pair.bat test
```

### 2. 新機能開発
```bash
# 1. 命令書作成
run_hybrid_pair.bat create user_authentication

# 2. 命令書確認・編集
run_hybrid_pair.bat review abc123def456

# 3. 承認
run_hybrid_pair.bat approve abc123def456 --approver "山田太郎"

# 4. 実行
run_hybrid_pair.bat execute abc123def456

# 5. 結果確認
# 生成コード: data/generated_code/
# レビュー結果: data/reviews/
```

### 3. システム状況確認
```bash
run_hybrid_pair.bat status
run_hybrid_pair.bat list
```

## Windows特有のコマンド

### 文字エンコーディング設定
```bash
chcp 65001  # UTF-8設定（バッチファイルに含まれている）
```

### ログ確認
```bash
type logs\latest.log
dir logs\
```

### 設定ファイル編集
```bash
notepad config\config.json
```

### データディレクトリ確認
```bash
dir data\instructions\
dir data\generated_code\
dir data\reviews\
```

## 開発・デバッグコマンド

### Python環境確認
```bash
python --version
python -m pip list
python -c "import sys; print(sys.path)"
```

### 依存関係インストール
```bash
pip install -r requirements.txt
```

### モジュール単体テスト
```bash
python -m src.core.instruction_manager
python -m src.api.llm_client
python -m src.api.slm_client
```

### JSON設定ファイル検証
```bash
python -c "import json; print(json.load(open('config/config.json', 'r', encoding='utf-8')))"
```
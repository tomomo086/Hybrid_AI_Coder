# 🚀 LLM×SLM ハイブリッドペアプログラミング コマンドリファレンス

## 🔧 基本セットアップ（初回のみ）

### 環境準備
```bash
# プロジェクトディレクトリに移動
cd "C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming"

# 依存関係インストール
pip install -r requirements.txt

# LM Studio動作確認
python debug_connection.py
```

## 📋 日常的な開発コマンド

### 1. システム状況確認
```bash
# システム全体の状況確認
PYTHONIOENCODING=utf-8 PYTHONPATH=src "/c/Python313/python.exe" hybrid_pair.py status

# 全命令書一覧表示
PYTHONIOENCODING=utf-8 PYTHONPATH=src "/c/Python313/python.exe" hybrid_pair.py list
```

**短縮版**（エイリアス設定推奨）:
```bash
python hybrid_pair.py status
python hybrid_pair.py list
```

### 2. 新機能作成フロー

#### Step 1: 命令書作成
```bash
# 対話式で新しい命令書を作成
python hybrid_pair.py create "機能名"

# 例:
python hybrid_pair.py create "file_processor"
python hybrid_pair.py create "csv_reader"  
python hybrid_pair.py create "api_client"
```

#### Step 2: 命令書確認・レビュー
```bash
# IDを確認
python hybrid_pair.py list

# 特定の命令書をレビュー
python hybrid_pair.py review <命令書ID>

# 例:
python hybrid_pair.py review ed6e1213-1068-42bc-bf7f-0cefea43b0c0
```

#### Step 3: 承認
```bash
# 命令書を承認（人間がレビュー後）
python hybrid_pair.py approve <命令書ID>
```

#### Step 4: コード生成実行
```bash
# DeepSeekでコード生成
python hybrid_pair.py execute <命令書ID>
```

#### Step 5: 結果確認
```bash
# 生成されたコードを確認
cat "data/generated_code/<生成ファイル名>.py"

# 生成コード一覧
ls data/generated_code/

# 実動テスト実行
python "data/generated_code/<生成ファイル名>.py"
```

## 🎯 実用的なワークフロー例

### 例1: CSVリーダー作成
```bash
# 1. 作成
python hybrid_pair.py create "csv_reader"
# → 対話式で要件入力（pandas使用、エラーハンドリング等）

# 2. 確認
python hybrid_pair.py list
# → ID: abc123-def456... を確認

# 3. レビュー  
python hybrid_pair.py review abc123-def456...
# → 内容確認、修正点チェック

# 4. 承認・実行
python hybrid_pair.py approve abc123-def456...
python hybrid_pair.py execute abc123-def456...

# 5. テスト
python "data/generated_code/csv_reader_abc123_20250906_150000.py"
```

### 例2: API エンドポイント作成
```bash
python hybrid_pair.py create "user_api"
# 要件: FastAPI、CRUD操作、JWT認証、PostgreSQL

python hybrid_pair.py list
python hybrid_pair.py review <新しいID>
python hybrid_pair.py approve <新しいID>
python hybrid_pair.py execute <新しいID>
```

## 🔄 品質改善ワークフロー

### 品質スコアが低い場合の改善手順
```bash
# 1. 品質評価確認
python hybrid_pair.py execute <ID>
# → 品質スコア75点（改善が必要）

# 2. Claude Codeに相談
# "ID <xxx> の命令書を改善したい。品質スコア75点で、
#  エラーハンドリングが不足している。改善案をください。"

# 3. 改善版作成
python hybrid_pair.py create "機能名_v2"
# → 改善された要件で再作成

# 4. 再実行・比較
python hybrid_pair.py execute <新しいID>
# → 品質スコア90点（改善成功）
```

## 🛠️ トラブルシューティング

### よくある問題と解決方法

#### Unicode文字化けエラー
```bash
# 環境変数を明示的に設定
PYTHONIOENCODING=utf-8 PYTHONPATH=src "/c/Python313/python.exe" hybrid_pair.py <コマンド>
```

#### LM Studio接続エラー
```bash
# 接続診断実行
python debug_connection.py

# LM Studio再起動
# モデル再読み込み
```

#### 依存関係エラー
```bash
# パッケージ再インストール
pip install -r requirements.txt --force-reinstall
```

## 📚 便利なエイリアス設定（推奨）

### Windows (PowerShell)
```powershell
# プロファイル設定ファイルを開く
notepad $PROFILE

# 以下を追加:
function hp { 
    PYTHONIOENCODING=utf-8 PYTHONPATH=src "/c/Python313/python.exe" hybrid_pair.py $args 
}

# 使用例:
hp status
hp list
hp create "new_function"
```

### Windows (Git Bash)
```bash
# ~/.bashrc に追加:
alias hp='PYTHONIOENCODING=utf-8 PYTHONPATH=src "/c/Python313/python.exe" hybrid_pair.py'

# 使用例:
hp status
hp list  
hp create "new_function"
```

## 🎯 効率的な使用パターン

### パターン1: 継続開発
```bash
# 毎日の開発開始時
hp status              # システム状況確認
hp list                # 進行中の命令書確認

# 新機能追加
hp create "new_feature"
hp review <ID>
hp approve <ID>
hp execute <ID>
```

### パターン2: バッチ処理
```bash
# 複数機能を一度に作成
for func in "data_loader" "data_processor" "data_saver"; do
    hp create "$func"
done

# 順次実行
hp list
# IDを確認して順次 approve → execute
```

### パターン3: 品質重視
```bash
# 高品質を目指す場合
hp create "critical_function"
hp review <ID>         # 詳細レビュー
# Claude Codeと相談して改善
hp approve <ID>        # 厳密チェック後承認
hp execute <ID>
# 品質スコア95点以上を目標
```

## 📖 参考ファイル

- `MEMORY.md`: 詳細な開発履歴・技術仕様
- `QUICKSTART.md`: 5分で始めるガイド  
- `README.md`: プロジェクト全体説明
- `requirements.txt`: 必要パッケージ一覧
- `config/config.example.json`: 設定テンプレート

## 🚨 重要な注意点

1. **承認は人間が行う**: 命令書の内容を必ず人間がチェック
2. **品質スコア確認**: 80点未満は改善検討
3. **実動テスト必須**: 生成コードは必ず動作確認
4. **バックアップ**: 重要な命令書は別途保存推奨
5. **LM Studio起動**: コード生成前にLM Studioが起動していることを確認

---
*作成日: 2025-09-06*  
*バージョン: 1.0*
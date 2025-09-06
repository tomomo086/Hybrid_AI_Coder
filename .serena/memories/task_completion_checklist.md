# LLM×SLM ハイブリッドペアプログラミング - タスク完了チェックリスト

## コード変更・開発完了時の必須チェック項目

### 1. コード品質チェック

#### フォーマット確認
```bash
# Black フォーマットチェック・適用
black --check .                # 確認のみ
black .                       # フォーマット適用
black src/                    # src ディレクトリのみ
```

#### リンターチェック
```bash
# Flake8 リンターチェック
flake8 .                      # 全体チェック
flake8 src/                   # src ディレクトリのみ
flake8 --show-source --statistics .  # 詳細表示
```

#### 型ヒントチェック（推奨）
```bash
# MyPyがインストールされている場合
mypy src/
mypy --strict src/
```

### 2. 機能テスト

#### システム統合テスト
```bash
# システム全体の動作確認
python run_system_test.py
```

#### API接続テスト
```bash
# API接続の確認
run_hybrid_pair.bat test
python hybrid_pair.py test

# 詳細診断（問題がある場合）
python debug_connection.py
```

#### 基本ワークフロー確認
```bash
# 命令書作成テスト
run_hybrid_pair.bat create test_function --no-interactive

# 命令書一覧確認
run_hybrid_pair.bat list

# システム状況確認
run_hybrid_pair.bat status
```

### 3. 設定・依存関係確認

#### 設定ファイル検証
```bash
# JSON設定ファイルの構文確認
python -c "import json; print('設定OK:', json.load(open('config/config.json', 'r', encoding='utf-8')))"

# 設定例ファイルとの整合性確認
python -c "
import json
with open('config/config.json', 'r', encoding='utf-8') as f: config = json.load(f)
with open('config/config.example.json', 'r', encoding='utf-8') as f: example = json.load(f)
missing = set(example.keys()) - set(config.keys())
if missing: print('不足キー:', missing)
else: print('設定完整性OK')
"
```

#### 依存関係確認
```bash
# requirements.txt の検証
pip check                     # 依存関係の整合性確認
pip list --outdated          # アップデート可能パッケージ確認

# 新しい依存関係の追加確認
pip freeze > requirements_current.txt
diff requirements.txt requirements_current.txt
```

### 4. ファイル・ディレクトリ構造確認

#### 必須ディレクトリの存在確認
```bash
# 必須ディレクトリの確認
python -c "
import os
dirs = ['config', 'data/instructions', 'data/generated_code', 'data/reviews', 'logs', 'src/core', 'src/api', 'src/cli', 'src/workflow']
for d in dirs:
    if os.path.exists(d):
        print(f'✅ {d}')
    else:
        print(f'❌ {d} - 作成が必要')
"
```

#### __init__.py ファイル確認
```bash
# パッケージ化のための __init__.py 確認
find src -type d -exec test -f {}/__init__.py \; -print
```

### 5. ログ・デバッグ情報確認

#### ログファイル確認
```bash
# 最新ログの確認
type logs\latest.log          # Windows
cat logs/latest.log           # Linux/Mac

# エラーログの検索
findstr "ERROR" logs\*.log    # Windows
grep "ERROR" logs/*.log       # Linux/Mac
```

#### デバッグ情報クリーンアップ
```bash
# 開発用デバッグコードの除去確認
findstr /R "print.*debug" src\*.py     # Windows
grep -r "print.*debug" src/           # Linux/Mac

# TODO/FIXME コメントの確認
findstr /R "TODO\|FIXME" src\*.py     # Windows
grep -r "TODO\|FIXME" src/           # Linux/Mac
```

### 6. セキュリティチェック

#### 機密情報漏洩確認
```bash
# ハードコードされたAPIキー等の確認
findstr /R "sk-\|api.*key.*=" src\*.py config\*.py    # Windows
grep -r "sk-\|api.*key.*=" src/ config/              # Linux/Mac

# パスワード・秘密情報の確認
findstr /R "password\|secret\|token.*=" src\*.py     # Windows
grep -r "password\|secret\|token.*=" src/            # Linux/Mac
```

#### ファイル権限確認（Unix系のみ）
```bash
# 設定ファイルの権限確認
ls -la config/
chmod 600 config/config.json  # 必要に応じて制限
```

### 7. ドキュメント更新確認

#### README.md の更新
- 新機能の追加説明
- コマンド例の更新
- トラブルシューティング情報の追加

#### CHANGELOG.md の更新（推奨）
```markdown
## [0.1.1] - 2024-XX-XX
### Added
- 新機能の説明

### Changed
- 変更された機能の説明

### Fixed
- 修正されたバグの説明
```

### 8. 実行テスト（End-to-End）

#### 完全ワークフローテスト
```bash
# 1. システムセットアップテスト
run_hybrid_pair.bat setup

# 2. 接続テスト
run_hybrid_pair.bat test

# 3. 命令書作成テスト
run_hybrid_pair.bat create test_feature_$(date +%s)

# 4. 生成された命令書IDを使用してレビュー
run_hybrid_pair.bat review [生成されたID]

# 5. テスト承認
run_hybrid_pair.bat approve [生成されたID] --approver "テストユーザー"

# 6. 実行テスト（DeepSeekが利用可能な場合）
run_hybrid_pair.bat execute [生成されたID]
```

#### パフォーマンステスト
```bash
# 起動時間測定
time python hybrid_pair.py status     # Unix系
# Windows では PowerShell で Measure-Command を使用
```

## 緊急時・リリース前チェックリスト

### 本番環境デプロイ前
1. ✅ すべてのAPIキーが正しく設定されている
2. ✅ デバッグモードが無効化されている
3. ✅ ログレベルが適切に設定されている
4. ✅ 不要なテストファイルが除去されている
5. ✅ セキュリティチェックが完了している

### バックアップ・復旧確認
```bash
# 設定ファイルのバックアップ
copy config\config.json config\config.backup.json

# データディレクトリのバックアップ
xcopy data data_backup /E /I

# Git での変更追跡（リポジトリがある場合）
git status
git diff
git add .
git commit -m "機能追加: [変更内容の説明]"
```

## 自動化スクリプト例

### チェックリスト自動実行
```python
#!/usr/bin/env python
"""
task_completion_check.py - 完了チェック自動化スクリプト
"""
import subprocess
import sys

def run_check(command, description):
    print(f"🔍 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {description}: OK")
        return True
    else:
        print(f"❌ {description}: NG")
        print(f"エラー: {result.stderr}")
        return False

if __name__ == "__main__":
    checks = [
        ("black --check .", "コードフォーマット確認"),
        ("flake8 .", "リンターチェック"),
        ("python run_system_test.py", "システムテスト"),
        ("python hybrid_pair.py test", "API接続テスト"),
    ]
    
    all_passed = True
    for command, description in checks:
        if not run_check(command, description):
            all_passed = False
    
    if all_passed:
        print("\n🎉 すべてのチェックが完了しました！")
        sys.exit(0)
    else:
        print("\n❌ 一部のチェックが失敗しました。")
        sys.exit(1)
```
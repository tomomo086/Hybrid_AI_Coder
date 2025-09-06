# ⚡ クイックコマンドリファレンス

## 🔥 最もよく使うコマンド

```bash
# システム状況確認
python hybrid_pair.py status

# 命令書一覧
python hybrid_pair.py list

# 新機能作成
python hybrid_pair.py create "機能名"

# レビュー
python hybrid_pair.py review <ID>

# 承認
python hybrid_pair.py approve <ID>

# 実行
python hybrid_pair.py execute <ID>
```

## 🎯 1分でコード生成

```bash
# ①作成
python hybrid_pair.py create "file_reader"

# ②ID確認
python hybrid_pair.py list

# ③承認・実行
python hybrid_pair.py approve abc123-...
python hybrid_pair.py execute abc123-...

# ④結果確認
ls data/generated_code/
```

## 🛠️ トラブル時の対処

```bash
# 文字化けエラー時
PYTHONIOENCODING=utf-8 PYTHONPATH=src "/c/Python313/python.exe" hybrid_pair.py status

# LM Studio接続エラー時  
python debug_connection.py

# 依存関係エラー時
pip install -r requirements.txt
```

## 📝 IDの見つけ方

```bash
# 最新の命令書IDを確認
python hybrid_pair.py list | tail -n 1

# 特定機能のIDを検索
python hybrid_pair.py list | grep "file_processor"
```

## ⚡ エイリアス（推奨設定）

```bash
# Git Bash用 (~/.bashrc に追加)
alias hp='PYTHONIOENCODING=utf-8 PYTHONPATH=src "/c/Python313/python.exe" hybrid_pair.py'

# 使用例:
hp status
hp create "new_func" 
hp list
```

---
*保存場所: プロジェクトルート*  
*いつでも `cat QUICK_COMMANDS.md` で確認可能*
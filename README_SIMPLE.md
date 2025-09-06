# Simple Hybrid Pair Programming System

超シンプル版 - ClaudeCode + DeepSeek 協調開発システム

## 🎯 概要

元の複雑なシステム（15+ファイル）を1ファイル（180行）に簡略化。
核心機能のみを残して、実用性と理解しやすさを重視。

## ⚡ クイックスタート

```bash
# 1. システム実行
python simple_hybrid.py

# 2. タスク作成
> create calculator "簡単な電卓機能を実装"

# 3. タスク承認 
> approve <task_id>

# 4. 実行（DeepSeekがコード生成）
> run <task_id>
```

## 🔧 必要な設定

### LM Studio設定
1. [LM Studio](https://lmstudio.ai/) をダウンロード・起動
2. DeepSeek-Coder 6.7B GGUF モデルを読み込み
3. ローカルAPIサーバー起動 (http://localhost:1234)

### 設定ファイル
初回実行時に `simple_config.json` が自動作成されます。
必要に応じてエンドポイントやモデル名を編集してください。

## 🏗️ アーキテクチャ

### ファイル構成
```
simple_hybrid.py    # メインプログラム（全機能統合）
simple_config.json  # 設定ファイル（自動生成）  
simple_tasks.json   # タスク保存（自動生成）
simple_results/     # 生成コード保存ディレクトリ
```

### 主要機能
- **SimpleHybridPair** クラス1つに全機能集約
- タスク管理（作成・一覧・承認）
- DeepSeek API通信
- ワークフロー実行
- CLI インターフェース

## 🚀 使用方法

### 基本コマンド
```bash
create <タイトル> <説明>  # 新規タスク作成
list                     # タスク一覧表示
approve <ID>             # タスク承認
run <ID>                 # ワークフロー実行
exit                     # 終了
```

### 典型的な作業フロー
1. **タスク作成**: `create web_scraper "Webスクレイピング機能"`
2. **確認・承認**: `list` → `approve abc123de`
3. **実行**: `run abc123de` → DeepSeekがコード生成
4. **結果確認**: `simple_results/` ディレクトリの生成コードをチェック

## 🔍 元システムとの比較

| 項目 | 元システム | Simple版 |
|------|------------|----------|
| ファイル数 | 15+ファイル | 1ファイル |
| 行数 | 2000+行 | 180行 |
| クラス数 | 8+クラス | 1クラス |
| 設定ファイル | 複数JSON | 1つのJSON |
| 学習コスト | 高（1時間+） | 低（5分） |
| メンテナンス性 | 複雑 | 簡単 |

## ✅ メリット

- **理解しやすい**: 全機能が1ファイルで見渡せる
- **導入簡単**: 依存関係最小限、設定自動生成
- **高速動作**: オーバーヘッドなし
- **拡張容易**: 必要な機能だけ追加可能
- **デバッグ簡単**: エラー箇所の特定が容易

## 🔧 カスタマイズ

### API設定変更
`simple_config.json` を編集:
```json
{
  "deepseek_api": {
    "endpoint": "http://localhost:1234/v1/chat/completions",
    "model": "your-model-name", 
    "temperature": 0.2,
    "max_tokens": 2000
  }
}
```

### 機能拡張
`SimpleHybridPair` クラスにメソッドを追加するだけで機能拡張可能。

## 🎉 実用例

```bash
# 実際の使用例
> create data_analyzer "CSVファイルを読み込んで基本統計を表示"
> approve f3a1b2c4
> run f3a1b2c4
# → simple_results/f3a1b2c4_20240906_143022.py が生成される
```

**シンプルでも強力な協調開発を体験してください！** 🚀
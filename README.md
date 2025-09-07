# 🤖 超シンプルハイブリッドAI開発システム

**人間 → ClaudeCode/GeminiCLI → LM Studio** の完璧な開発フローで、アイデアを瞬時にコードに変換。

## 🎯 概要・設計意図

**3つの機能だけの究極シンプル設計**：
1. 命令書を受け取る（人間から直接）
2. SLMにコードを生成させる（LM Studio経由）
3. 指定場所にファイル保存（任意パス）

### 💡 設計意図：LLMコンテキスト節約
**メイン目的**: LLM（ClaudeCode・GeminiCLI）の**コンテキスト消費を劇的削減**

- **従来**: LLMがコード生成 → 大量のコンテキスト消費
- **このシステム**: SLMがコード生成 → LLMはコンテキスト節約
- **効果**: LLMは設計・レビューに集中、SLMは実装に特化

### 🔄 SLM随時交換による品質制御
- **DeepSeek-Coder**: 軽量高速、シンプルなコード
- **Qwen2.5-Coder**: 高品質、複雑なロジック対応
- **CodeLlama**: バランス型、汎用性高い
- **即座切り替え**: LM Studio側でモデル変更するだけ

## 🚀 開発フロー

```
人間のアイデア → ClaudeCode/GeminiCLI → このシステム → LM Studio → 完成コード
```

1. **人間**: 「○○のアプリを作りたい」と要求
2. **ClaudeCode/GeminiCLI**: 仕様整理・このシステム実行  
3. **このシステム**: 仕様をLM Studioに送信
4. **LM Studio**: DeepSeek/Qwen等でコード生成
5. **結果**: 指定場所に完成コードが保存

## ⚡ 使用方法

### 1. ClaudeCodeでの実行（推奨）
**プロンプト例**：
```
このシステムを使って、事前に作成した命令書を元に
以下のプロジェクトをC:/projects/フォルダに
SLMで生成してください。修正はその後で行います。

命令書: 「家計簿アプリを作成：収入支出管理、月別集計表示、CSV出力機能、tkinter GUI」
保存先: C:/projects/household_budget/main.py

よろしくお願いします。
```

**ClaudeCodeの実行**：
```python
from quick_execute import quick_hybrid

quick_hybrid(
    "家計簿アプリを作成：収入支出管理、月別集計、CSV出力、tkinter GUI", 
    "C:/projects/household_budget/main.py"
)
```

### 2. GeminiCLIでの実行
**プロンプト例**：
```
準備済みの命令書を使って、このハイブリッドシステムで
SLMにコード生成させてください。出力先は指定フォルダで。
後で修正・改善は一緒に行いましょう。

命令書: 「Webスクレイピングツール：Beautiful Soup使用、CSV出力、エラーハンドリング」
出力先: C:/dev/scraping_tools/scraper.py
```

**GeminiCLIの実行**：
```python
exec(open('quick_execute.py').read())
quick_hybrid(
    "Webスクレイピングツール：Beautiful Soup使用、CSV出力、エラーハンドリング", 
    "C:/dev/scraping_tools/scraper.py"
)
```

### 3. 対話モード（学習用）
```bash
python ultra_simple.py
```
- 命令書を入力（改行2回で終了）
- 保存パスを指定（例: C:/projects/my_app.py）
- 自動でコード生成・保存

## 🛠️ 必要な環境

### 1. AI支援開発環境（いずれか必須）
- **[ClaudeCode](https://claude.ai/code)** - Anthropic公式CLI（推奨）
- **[GeminiCLI](https://ai.google.dev/)** - Google製コマンドライン
- その他AI支援開発ツール

### 2. LM Studio設定（必須）
1. [LM Studio](https://lmstudio.ai/) をダウンロード・起動
2. 推奨モデル（いずれか）を読み込み：
   - **DeepSeek-Coder-6.7B** (軽量・高速)
   - **Qwen2.5-Coder-14B** (高品質・重い)
   - **CodeLlama** (バランス型)
3. ローカルAPIサーバー起動 (http://localhost:1234)

### 3. Python環境
```bash
pip install requests  # 必要なライブラリはこれだけ
```

## 📁 ファイル構成（4ファイルのみ）

```
LLM_SLM_Hybrid_Pair_Programming/
├── ultra_simple.py          # メインシステム（150行）
├── quick_execute.py         # ワンライナー実行（50行）
├── simple_config.json       # SLM接続設定
└── README.md               # このファイル
```

### 設定ファイル
`simple_config.json` が自動作成されます：

```json
{
  "deepseek_api": {
    "endpoint": "http://localhost:1234/v1/chat/completions",
    "model": "qwen2.5-coder-14b-instruct",
    "temperature": 0.2,
    "max_tokens": 2000
  }
}
```

**LM Studioでモデル切り替えするだけ** - 設定ファイルのmodel名は参考程度

## 🔄 実際のワークフロー

### 従来の開発
```
アイデア → 設計 → コーディング → テスト → デバッグ
（時間: 数時間〜数日）
```

### このシステムでの開発
```
アイデア → ClaudeCode/GeminiCLI → 完成コード
（時間: 数分）
```

## 🔮 実用例とコンテキスト節約効果

### 従来のLLMのみ開発
```
人間: 「数独ソルバーを作って」
↓
ClaudeCode: [大量のコード生成でコンテキスト消費]
↓
結果: コンテキスト不足で途中で中断、品質低下
```

### このシステムでの開発
```python
# 人間のプロンプト例
「事前に作成した数独の命令書を使って、
このハイブリッドシステムでC:/games/フォルダに
SLMで生成してください。修正は後で一緒にやりましょう。」

# ClaudeCodeの実行（コンテキスト節約）
from quick_execute import quick_hybrid
quick_hybrid(
    "数独ソルバー：9x9グリッド、バックトラッキング算法、tkinter GUI表示",
    "C:/games/sudoku_solver.py"
)

# 結果
- SLM: 完全なソルバー生成（コンテキスト消費なし）
- LLM: コンテキスト温存で修正・レビューに集中可能
- 効果: 70-90%のコンテキスト削減
```

### SLM比較実験例
```python
# 同じ命令書で異なるSLMを試す
命令書 = "REST API サーバー：Flask使用、認証機能、エラーハンドリング"

# DeepSeek-Coder（軽量高速）
quick_hybrid(命令書, "C:/api/server_deepseek.py")

# Qwen2.5-Coder（高品質）  
quick_hybrid(命令書, "C:/api/server_qwen.py")

# CodeLlama（バランス）
quick_hybrid(命令書, "C:/api/server_llama.py")

# → 3つのアプローチを比較・選択可能
```

## 🎉 なぜこのシステム？

### 🚀 革命的な開発速度
- **従来**: アイデア → 完成まで数時間〜数日
- **このシステム**: アイデア → 完成まで数分

### 💾 LLMコンテキスト大幅節約
- **従来のLLM使用**: コード生成で大量トークン消費
- **このシステム**: SLMが実装担当、LLMは設計に集中
- **効果**: **70-90%のコンテキスト削減**、長時間の開発セッション可能

### 🔄 SLMによる品質制御
- **リアルタイム切り替え**: LM Studioでワンクリック
- **用途別最適化**: 
  - 軽量タスク → DeepSeek-Coder (高速)
  - 複雑ロジック → Qwen2.5-Coder (高品質)
  - バランス重視 → CodeLlama (汎用)
- **品質実験**: 同じ命令書で複数SLM比較可能

### 🎯 最適な役割分担
- **人間**: 創造性・要件定義・最終判断
- **LLM（ClaudeCode/GeminiCLI）**: 仕様整理・品質管理・レビュー（**コンテキスト節約**）
- **SLM（LM Studio）**: 高速・正確なコード実装

### 🌍 完全日本語対応
- 日本語での要件定義可能
- 日本語コメント付きコード生成
- 日本の開発文化に適応

### ⚡ 究極のシンプル設計
- **4ファイルのみ** - 不要な複雑さを完全排除
- **200行程度** - 全体把握が容易
- **即座に開始** - セットアップ不要
- **面倒なコマンド不要** - プロンプトで依頼するだけ

## 🚦 システム要件

- **Python 3.7+**
- **requests ライブラリ**
- **LM Studio + 任意のコーディングモデル**
- **ClaudeCode または GeminiCLI**（推奨）

これだけです！

---

**人間の創造性 × AIの実装力 = 未来の開発スタイル** 🚀

*アイデアを持った瞬間から数分でコードが完成する時代へ*
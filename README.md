# 🤖 超シンプルハイブリッドAI開発システム

**人間 → ClaudeCode/GeminiCLI → LM Studio** の完璧な開発フローで、アイデアを瞬時にコードに変換。

## 🎯 概要

**3つの機能だけの究極シンプル設計**：
1. 命令書を受け取る（人間から直接）
2. SLMにコードを生成させる（LM Studio経由）
3. 指定場所にファイル保存（任意パス）

現代のAI支援開発環境（ClaudeCode・GeminiCLI）とローカルSLM（LM Studio）を連携させ、人間の創造性とAIの実装力を組み合わせた次世代開発システム。

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

### 1. ClaudeCodeからの実行（推奨）
```python
# ClaudeCodeで以下を実行
from quick_execute import quick_hybrid

# ワンライナーで完了
quick_hybrid(
    "家計簿アプリを作成：収入支出管理、月別集計、CSV出力、tkinter GUI", 
    "C:/projects/budget_app.py"
)
```

### 2. GeminiCLIからの実行
```python
# GeminiCLIで以下を実行
exec(open('quick_execute.py').read())
quick_hybrid("Webスクレイピングツール作成", "C:/tools/scraper.py")
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

## 🔮 実用例

```python
# ClaudeCodeで実行
人間: 「数独ソルバーを作りたい」
↓
ClaudeCode: 「要件を整理して実行しますね」
from quick_execute import quick_hybrid
quick_hybrid(
    "数独ソルバー：9x9グリッド、バックトラッキング算法、tkinter GUI表示",
    "C:/games/sudoku_solver.py"
)
↓
LM Studio: Qwen2.5-Coderで完全なソルバー生成
↓  
結果: 完成した数独ソルバーがC:/games/sudoku_solver.pyに保存
```

## 🎉 なぜこのシステム？

### 革命的な開発速度
- **従来**: アイデア → 完成まで数時間〜数日
- **このシステム**: アイデア → 完成まで数分

### 最適な役割分担
- **人間**: 創造性・要件定義・最終判断
- **ClaudeCode/GeminiCLI**: 仕様整理・品質管理・レビュー
- **LM Studio**: 高速・正確なコード実装

### 完全日本語対応
- 日本語での要件定義可能
- 日本語コメント付きコード生成
- 日本の開発文化に適応

### 究極のシンプル設計
- **4ファイルのみ** - 不要な複雑さを完全排除
- **200行程度** - 全体把握が容易
- **即座に開始** - セットアップ不要

## 🚦 システム要件

- **Python 3.7+**
- **requests ライブラリ**
- **LM Studio + 任意のコーディングモデル**
- **ClaudeCode または GeminiCLI**（推奨）

これだけです！

---

**人間の創造性 × AIの実装力 = 未来の開発スタイル** 🚀

*アイデアを持った瞬間から数分でコードが完成する時代へ*
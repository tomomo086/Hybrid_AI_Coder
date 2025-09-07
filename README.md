# 🤖 Hybrid_AI_Coder

> LLMコンテキスト節約型のハイブリッドAI開発システム

## 🎯 コンセプト

**LLM + SLMの最適分担**: LLMは設計・レビュー、SLMは実装

### 3つの基本機能
1. 命令書を受け取り
2. SLMでコード生成（LM Studio）
3. 指定場所に保存

### 効果
- **コンテキスト節約**: LLMのトークン消費を20-40%削減
- **品質制御**: SLMをリアルタイム切り替え（DeepSeek/Qwen/CodeLlama）

## 🚀 開発フロー

```
アイデア → LLM対話 → 要件定義 → 具体的命令書 → SLM実行 → 完成コード
```

## ⚡ 使用方法

### 環境準備
1. [LM Studio](https://lmstudio.ai/)でSLMを起動
2. `pip install requests`

### 実行方法
- **ClaudeCode/GeminiCLI**: プロンプトで命令書と保存先指定
- **対話モード**: `ultra_simple.py`を直接実行

## 📁 ファイル構成

```
Hybrid_AI_Coder/
├── ultra_simple.py          # メインシステム
├── quick_execute.py         # ワンライナー実行
├── simple_config.json       # SLM接続設定（自動生成）
└── README.md               # このファイル
```

## 🎯 特徴

### コンテキスト節約の仕組み
- **従来**: LLMが全工程担当 → 大量トークン消費
- **本システム**: 
  - LLM: 設計・要件整理・レビュー
  - SLM: 具体的コード実装
  - 結果: 20-40%のトークン削減

### SLM命令書作成のコツ
- **具体的指示**: 曖昧表現を避け詳細に記述
- **技術仕様明示**: ライブラリ、エラー処理、命名規則を指定
- **実装詳細**: ファイル構造、関数名、コメント内容まで明記

### 推奨SLM
- **DeepSeek-Coder**: 軽量・高速
- **Qwen2.5-Coder**: 高品質・複雑ロジック
- **CodeLlama**: バランス型

## 🛠️ 技術要件

- Python 3.7+
- requests ライブラリ
- LM Studio + コーディングモデル
- ClaudeCode（推奨）または GeminiCLI

---

**人間の創造性 × AIの実装力 = 効率的開発** 🚀

*作成者: tomomo086 + Claude4 | 最終更新: 2025年9月7日*
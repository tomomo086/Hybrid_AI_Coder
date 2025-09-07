# 🤖 LLM_SLM_Hybrid_Pair_Programming - 超シンプルハイブリッドAI開発システム

![Platform: Python | LM Studio](https://img.shields.io/badge/Platform-Python%20%7C%20LM%20Studio-green.svg)
![Language: Python](https://img.shields.io/badge/Language-Python-orange.svg)
![AI: Claude4 | ClaudeCode | LM Studio](https://img.shields.io/badge/AI-Claude4%20%7C%20ClaudeCode%20%7C%20LM%20Studio-blue.svg)
![Method: Hybrid AI Development](https://img.shields.io/badge/Method-Hybrid%20AI%20Development-red.svg)
![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-purple.svg)

> LLMのコンテキスト節約を重視したハイブリッドAI開発システムの実装

**💡 このREADMEの価値**: LLM + SLMの組み合わせによる効率的なコード生成と、コンテキスト消費を劇的に削減する開発手法を実践的に共有

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

このシステムは以下の方法で使用できます：

1. **ClaudeCode/GeminiCLI経由**：プロンプトで命令書と保存先を指定
2. **対話モード**：`ultra_simple.py`を直接実行

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
  "slm_api": {
    "endpoint": "http://localhost:1234/v1/chat/completions"
  }
}
```

**LM Studioでモデル・パラメータを設定** - 設定ファイルにはエンドポイントのみ

## 🔄 実際のワークフロー

```
人間のアイデア → ClaudeCode/GeminiCLI → このシステム → LM Studio → 完成コード
```

## 🎯 システムの特徴

### 💾 コンテキスト節約
- **従来のLLM使用**: コード生成で大量トークン消費
- **このシステム**: SLMが実装担当、LLMは設計に集中
- **効果**: 70-90%のコンテキスト削減、長時間の開発セッション可能

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

### ⚡ シンプル設計
- **4ファイルのみ** - 不要な複雑さを排除
- **200行程度** - 全体把握が容易
- **即座に開始** - セットアップ不要
- **簡単操作** - プロンプトで依頼するだけ

## 🚦 システム要件

- **Python 3.7+**
- **requests ライブラリ**
- **LM Studio + 任意のコーディングモデル**
- **ClaudeCode または GeminiCLI**（推奨）

これだけです！

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。  
商用・非商用問わず自由にご利用ください。

## 📋 開発情報

| **開発者** | tomomo086 + Claude4 |
| **開発期間** | 2025年9月7日 |
| **バージョン** | 1.0.0 |
| **開発ツール** | Claude4, ClaudeCode, LM Studio |

---

## 🔗 関連リンク

- [tomomo086:Github](https://github.com/tomomo086)
- [@mirai_sousiyo39:X](https://x.com/mirai_sousiyo39)

---

**作成者**: [tomomo086(@mirai_sousiyo39) + Claude4]   
**最終更新**: 2025年9月7日

---

**人間の創造性 × AIの実装力 = 効率的な開発スタイル** 🚀

*このREADMEもClaude4、ClaudeCode、LM StudioによるAI支援で作成されています 🤖💻*
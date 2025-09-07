# 🤖 ハイブリッドAI開発システム

**人間 → ClaudeCode/GeminiCLI → LM Studio** の完璧な開発フローで、アイデアを瞬時にコードに変換。

## 🎯 概要

現代のAI支援開発環境（ClaudeCode・GeminiCLI）とローカルSLM（LM Studio）を連携させ、人間の創造性とAIの実装力を組み合わせた次世代開発システムです。

## 🚀 開発フロー

```
人間のアイデア → ClaudeCode/GeminiCLI → このシステム → LM Studio → 完成コード
```

1. **人間**: 「○○のアプリを作りたい」と要求
2. **ClaudeCode/GeminiCLI**: 仕様整理・このシステム実行  
3. **このシステム**: 仕様をLM Studioに送信
4. **LM Studio**: DeepSeek/Qwen等でコード生成
5. **結果**: 指定場所に完成コードが保存

## 💡 2つのアプローチ

### 1. **Complete Version** (`hybrid_pair.py`)
- **本格開発用**: 企業・チーム開発
- **フル機能**: 承認フロー、品質管理、履歴追跡
- **対象**: 長期プロジェクト、複数人開発

### 2. **Simple Version** (`simple_hybrid.py`) ⭐ 推奨  
- **個人・学習用**: 即座に開始可能
- **超軽量**: 核心機能のみ、理解しやすい
- **対象**: プロトタイプ、アイデア検証、学習

## ⚡ クイックスタート

### ClaudeCodeからの実行（推奨）
```python
# ClaudeCodeで以下を実行
exec(open('simple_hybrid.py').read())

# タスク作成・実行
app = SimpleHybridPair()
app.create_task("calculator", "電卓アプリを作成してください")
task_id = "<生成されたID>"
app.approve_task(task_id)
app.run_workflow(task_id)
```

### GeminiCLIからの実行
```python  
# GeminiCLIで以下を実行
exec(open('simple_hybrid.py').read())

# 直接実行も可能
hybrid = SimpleHybridPair()
hybrid.execute_instruction("Webスクレイピングツール", "scraping_tool")
```

### 対話モード（学習用）
```bash
python simple_hybrid.py
# コマンドラインでの対話的実行
```

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

## 📁 プロジェクト構造

```
LLM_SLM_Hybrid_Pair_Programming/
├── simple_hybrid.py       # Simple版（推奨開始点）
├── README_SIMPLE.md       # Simple版詳細ガイド
├── hybrid_pair.py         # Complete版メインCLI
├── README.md              # このファイル
├── run_hybrid_pair.bat    # Windows実行用
├── requirements.txt       # 依存関係
├── config/                # 設定ファイル
├── data/                  # 実行データ（命令書・生成コード）
├── src/                   # Complete版ソースコード
└── archive/               # アーカイブファイル
```

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

### 詳細フロー
1. **要件定義** (人間): 「○○を作りたい」
2. **仕様整理** (ClaudeCode/GeminiCLI): 技術要件整理
3. **システム実行** (AI支援環境): このシステムを呼び出し
4. **コード生成** (LM Studio): ローカルSLMで実装
5. **品質確保** (ClaudeCode/GeminiCLI): レビュー・修正
6. **完成** (自動): 指定場所にファイル保存

## 📚 ドキュメント

- **Simple版**: `README_SIMPLE.md` - 超軽量版の詳細
- **アーカイブ**: `archive/` - 過去の詳細ドキュメント

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

## 🚦 どちらを選ぶ？

| 用途 | 推奨版 | 理由 |
|------|--------|------|
| **個人開発** | Simple | 軽量・即座に開始可能 |
| **学習・実験** | Simple | 仕組み理解しやすい |
| **プロトタイプ** | Simple | アイデア検証に最適 |
| **企業開発** | Complete | 承認フロー・品質管理 |
| **チーム開発** | Complete | 履歴管理・責任明確化 |

**迷ったらSimple版から始めてください！** 🎯

## 🔮 実用例

```python
# ClaudeCodeで実行
人間: 「家計簿アプリを作りたい」
↓
ClaudeCode: 「要件を整理して実行します」
exec(open('simple_hybrid.py').read())
app = SimpleHybridPair()
app.create_task("household_budget", "家計簿アプリ：収入支出管理、月別集計、CSV出力、tkinter GUI")
app.approve_task("<ID>")  
app.run_workflow("<ID>")
↓
LM Studio: 完全なGUIアプリケーション生成
↓  
結果: 完成した家計簿アプリが指定場所に保存
```

---

**人間の創造性 × AIの実装力 = 未来の開発スタイル** 🚀
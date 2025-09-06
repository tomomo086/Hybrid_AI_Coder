# LLM×SLM ハイブリッドペアプログラミング システム

Claude Code + DeepSeek-Coder の協調開発システム

## 🎯 概要

ClaudeCode（設計・分析・レビュー）とDeepSeek-Coder（実装）を組み合わせて、効率的で高品質なコード生成を実現します。

## 🚀 2つのバージョン

### 1. **Complete Version** (`hybrid_pair.py`)
- **フル機能**: 命令書管理、品質評価、ワークフロー制御
- **対象**: 本格的な開発プロジェクト
- **構造**: モジュラー設計、拡張可能

### 2. **Simple Version** (`simple_hybrid.py`) ⭐ 推奨
- **超軽量**: 1ファイル180行、5分で理解
- **対象**: 学習・プロトタイプ・個人利用
- **構造**: シンプル、即座に使用可能

## ⚡ クイックスタート

### Simple Version の使用
```bash
# 1. 実行
python simple_hybrid.py

# 2. タスク作成・承認・実行
> create calculator "電卓機能を実装"
> approve <task_id>
> run <task_id>
```

### Complete Version の使用
```bash
# 1. 初期設定
python hybrid_pair.py setup

# 2. ワークフロー実行
python hybrid_pair.py create <機能名>
python hybrid_pair.py approve <ID> --approver "担当者"
python hybrid_pair.py execute <ID>
```

## 🛠️ 必要な環境

### LM Studio設定
1. [LM Studio](https://lmstudio.ai/) をダウンロード・起動
2. DeepSeek-Coder 6.7B GGUF モデルを読み込み
3. ローカルAPIサーバー起動 (http://localhost:1234)

### Python依存関係
```bash
pip install -r requirements.txt
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

## 🔄 ワークフロー

1. **要件整理** (ClaudeCode)
2. **命令書作成** (ClaudeCode) 
3. **人間承認** ⭐ 重要な品質管理
4. **コード実装** (DeepSeek-Coder)
5. **レビュー・最適化** (ClaudeCode)

## 📚 ドキュメント

- **Simple版**: `README_SIMPLE.md` - 超軽量版の詳細
- **アーカイブ**: `archive/` - 過去の詳細ドキュメント

## 🎉 特徴

- **日本語対応**: 全面的な日本語サポート
- **人間中心**: 重要な判断は人間が実施
- **モジュラー**: 必要な機能のみ選択可能
- **実用的**: 実際のコード生成に特化

## 🚦 どちらを選ぶ？

| 用途 | 推奨版 | 理由 |
|------|--------|------|
| **学習・理解** | Simple | 5分で全体把握可能 |
| **プロトタイプ** | Simple | 即座に開始、軽量 |
| **本格開発** | Complete | 詳細な品質管理 |
| **チーム利用** | Complete | 承認フロー、履歴管理 |

**迷ったらSimple版から始めてください！** 🎯

---

**効率的で高品質なコード開発を、LLM×SLMハイブリッドで実現しましょう！** 🤖
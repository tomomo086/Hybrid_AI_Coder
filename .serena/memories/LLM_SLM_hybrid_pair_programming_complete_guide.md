# LLM×SLM ハイブリッドペアプログラミングシステム - 完全ガイド

## プロジェクト概要

**目的**: ClaudeCode + DeepSeek-Coder の協調開発システム
**場所**: `C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming`
**ブランチ**: `simple-hybrid-pair` (整理済み)

## 2つのバージョン体系

### Simple Version (`simple_hybrid.py`) ⭐ 推奨
- **ファイル**: 1ファイル、180行
- **特徴**: 超軽量、5分で理解可能
- **対象**: 学習、プロトタイプ、個人利用
- **構造**: 全機能を1クラス`SimpleHybridPair`に統合

### Complete Version (`hybrid_pair.py` + `src/`)
- **ファイル**: 15+ファイル、2000+行
- **特徴**: モジュラー設計、拡張可能
- **対象**: 本格開発、チーム利用
- **構造**: 複数クラスによる責任分離

## 技術アーキテクチャ

### ワークフロー
1. **要件整理** (ClaudeCode)
2. **命令書作成** (ClaudeCode) 
3. **人間承認** ⭐ 重要な品質管理ポイント
4. **コード実装** (DeepSeek-Coder)
5. **レビュー・最適化** (ClaudeCode)

### API構成
- **LLM**: ClaudeCode (設計・分析・レビュー)
- **SLM**: DeepSeek-Coder 6.7B (実装・コード生成)
- **環境**: LM Studio + ローカルAPI (http://localhost:1234)

## Simple Version 詳細仕様

### クラス構造
```python
class SimpleHybridPair:
    # 1. 設定・初期化 (20行)
    def __init__(self, config_file="simple_config.json")
    def load_config(self) -> Dict
    def load_tasks(self) -> List[Dict]
    def save_tasks(self)
    
    # 2. タスク管理 (30行)
    def create_task(self, title: str, description: str) -> str
    def list_tasks(self)
    def approve_task(self, task_id: str) -> bool
    
    # 3. API通信 (30行)
    def call_deepseek(self, prompt: str) -> Optional[str]
    
    # 4. ワークフロー実行 (80行)
    def run_workflow(self, task_id: str) -> bool
    
    # 5. CLI インターフェース (20行)
    def run_cli(self)
```

### データ構造
```json
// simple_tasks.json
{
  "id": "abc123de",
  "title": "タスクタイトル", 
  "description": "詳細説明",
  "status": "created|completed",
  "created_at": "ISO datetime",
  "approved": true|false,
  "result_file": "path/to/generated/code.py"
}

// simple_config.json
{
  "deepseek_api": {
    "endpoint": "http://localhost:1234/v1/chat/completions",
    "model": "deepseek-coder-6.7b-instruct",
    "temperature": 0.2,
    "max_tokens": 2000
  }
}
```

### 使用方法
```bash
# 実行
python simple_hybrid.py

# 対話式コマンド
> create calculator "電卓機能を実装"     # タスク作成
> list                                  # 一覧表示
> approve abc123de                      # 承認
> run abc123de                         # 実行
> exit                                 # 終了
```

## Complete Version 詳細仕様

### ディレクトリ構造
```
src/
├── core/
│   └── instruction_manager.py     # 命令書管理（16メソッド）
├── api/
│   ├── llm_client.py              # Claude API
│   └── slm_client.py              # DeepSeek API
├── cli/
│   ├── instruction_creator.py     # 命令書作成ツール
│   └── instruction_viewer.py      # 命令書表示・管理
├── workflow/
│   └── executor.py                # ワークフロー実行エンジン
├── quality_control/
│   └── code_reviewer.py           # コードレビューシステム
└── ui/
    └── approval_interface.py      # 承認インターフェース
```

### 主要クラス
- **InstructionManager**: 命令書のCRUD、承認管理
- **WorkflowExecutor**: ワークフロー制御、API呼び出し統合
- **CodeReviewer**: AST解析による品質評価
- **HybridPairCLI**: 統合CLIインターフェース

## プロジェクト構造（整理後）

```
LLM_SLM_Hybrid_Pair_Programming/
├── simple_hybrid.py       # Simple版（推奨開始点）
├── README_SIMPLE.md       # Simple版詳細ガイド
├── hybrid_pair.py         # Complete版メインCLI
├── README.md              # 統合メインドキュメント
├── run_hybrid_pair.bat    # Windows実行用
├── requirements.txt       # 依存関係
├── config/                # 設定ファイル
│   ├── config.json        # Complete版設定
│   ├── config.example.json
│   └── instruction_templates/
├── data/                  # 実行データ
│   ├── instructions/      # 命令書JSON
│   ├── generated_code/    # 生成されたPythonコード
│   └── reviews/          # レビュー結果
├── src/                   # Complete版ソースコード
└── archive/               # 整理済みアーカイブ
    ├── MEMORY.md         # 旧詳細記録（436行）
    ├── PROJECT_DASHBOARD.md
    ├── debug_connection.py
    └── ... (12ファイル)
```

## 実装履歴・成果

### 達成した技術成果
- **高品質コード生成**: DeepSeek-Coder 6.7Bで95点評価
- **エンドツーエンド動作**: 完全な命令書→実行→評価サイクル
- **品質自動評価**: AST解析による客観的品質測定
- **Unicode問題解決**: Windows環境での日本語対応完全対応

### 生成されたコード例
- `simple_calculator`: 基本電卓機能
- `data_analyzer`: CSV解析・統計表示（複雑機能、1951文字）
- `batch_processor`: バッチ処理機能（2089文字）

## 選択指針

| 用途 | 推奨版 | 理由 |
|------|--------|------|
| **学習・理解** | Simple | 5分で全体把握可能 |
| **プロトタイプ** | Simple | 即座に開始、軽量 |
| **本格開発** | Complete | 詳細な品質管理 |
| **チーム利用** | Complete | 承認フロー、履歴管理 |

## 環境要件

### 必須環境
- **Python**: 3.12+ (WinPython想定)
- **LM Studio**: DeepSeek-Coder 6.7B GGUF
- **API**: http://localhost:1234 (LM Studio)

### 依存関係
```txt
requests>=2.31.0
json5>=0.9.0  
pathlib>=1.0.0
```

## 日本語対応仕様

### 文字エンコーディング
- **ソースコード**: UTF-8
- **設定ファイル**: UTF-8 JSON
- **生成コード**: UTF-8、日本語コメント対応
- **Windows**: `chcp 65001` + `-X utf8` フラグ

### 出力形式
- 絵文字を文字ラベル化（[SUCCESS], [ERROR]）
- 日本語メッセージ優先
- Windows Console cp932対応

## 拡張・カスタマイズポイント

### Simple Version拡張
- `SimpleHybridPair`クラスにメソッド追加
- `simple_config.json`でAPI設定変更
- 新しいコマンドを`run_cli()`に追加

### Complete Version拡張
- 新しいAPIクライアント追加（`src/api/`）
- カスタムレビューア実装（`src/quality_control/`）
- 命令書テンプレート追加（`config/instruction_templates/`）

## トラブルシューティング

### よくある問題
1. **LM Studio接続エラー**: ポート1234確認、モデル読み込み確認
2. **Unicode文字化け**: `-X utf8`フラグ使用
3. **命令書が見つからない**: `data/instructions/`存在確認

### デバッグツール（archive/に保管）
- `debug_connection.py`: API接続診断
- `run_system_test.py`: システム統合テスト

## プロジェクトの価値

### 技術的価値
- **LLM×SLMハイブリッド**: 設計品質と実装効率の両立
- **人間承認システム**: AI生成コードの品質管理
- **シンプル化成功例**: 2000行→180行の機能保持簡略化

### 学習価値
- AIペアプログラミングの実践例
- 複雑システムの段階的簡略化手法
- 日本語対応システム開発のベストプラクティス
# LLM×SLM ハイブリッドペアプログラミング システム - プロジェクト概要

## プロジェクトの目的
Claude 4 (LLM) と DeepSeek-Coder 6.7B (SLM) を組み合わせた協調開発システムです。効率的で高品質なコード生成を実現する革新的なアプローチを提供します。

### 役割分担
- **Claude (LLM)**: 設計・分析・レビュー・最適化
- **DeepSeek (SLM)**: 実装・コード生成・基本機能構築

### 人間承認ワークフロー
1. 人間 → 要件・機能説明
2. Claude → 命令書ドラフト作成
3. 人間 → 命令書レビュー・修正・承認 ★重要な人間判断
4. Claude → 承認された命令書をDeepSeekに送信
5. DeepSeek → 実装
6. Claude → コードレビュー・最適化

## 技術スタック

### プログラミング言語
- **Python 3.12** (WinPython環境想定)

### Webフレームワーク
- **Streamlit** (>=1.28.0) - 人間承認UI用
- **Flask** (>=2.3.0) - API インターフェース用

### API・AI関連
- **OpenAI API** (>=1.0.0) - LM Studio API互換用
- **Claude API** - LLM機能用
- **requests** (>=2.31.0) - HTTP通信用

### データ処理・設定管理
- **pandas** (>=1.5.0) - データ処理用
- **json5** (>=0.9.0) - 設定ファイル用
- **pydantic** (>=2.0.0) - データバリデーション用
- **python-dotenv** (>=1.0.0) - 環境変数管理用

### 日本語対応
- **japanize-matplotlib** (>=1.1.3) - 日本語グラフ表示用

### 開発・品質管理
- **pytest** (>=7.4.0) - テストフレームワーク
- **black** (>=23.0.0) - コードフォーマッター
- **flake8** (>=6.0.0) - コードリンター
- **loguru** (>=0.7.0) - ログ管理

### セキュリティ・ユーティリティ
- **cryptography** (>=41.0.0) - セキュリティ機能
- **watchdog** (>=3.0.0) - ファイル監視用
- **pathlib** (>=1.0.0) - パス操作用

## プロジェクト構造

```
LLM_SLM_Hybrid_Pair_Programming/
├── hybrid_pair.py              # メインCLIエントリーポイント
├── run_hybrid_pair.bat         # Windows実行用バッチファイル
├── run_system_test.py          # システム統合テスト
├── debug_connection.py         # API接続デバッグツール
├── requirements.txt            # 依存関係
├── README.md                   # プロジェクト説明書
├── QUICKSTART.md              # クイックスタートガイド
├── MEMORY.md                  # メモリ管理仕様
├── config/                    # 設定ファイル群
│   ├── config.json           # メイン設定ファイル（要編集）
│   ├── config.example.json   # 設定例ファイル
│   └── instruction_templates/ # 命令書テンプレート群
├── src/                      # ソースコード
│   ├── core/                 # コアシステム
│   │   └── instruction_manager.py  # 命令書管理システム
│   ├── api/                  # APIクライアント
│   │   ├── llm_client.py     # Claude APIクライアント
│   │   └── slm_client.py     # DeepSeek APIクライアント
│   ├── cli/                  # コマンドラインツール
│   │   ├── instruction_creator.py   # 命令書作成ツール
│   │   └── instruction_viewer.py    # 命令書表示・管理ツール
│   ├── workflow/             # ワークフロー管理
│   │   └── executor.py       # ワークフロー実行エンジン
│   ├── quality_control/      # 品質管理
│   │   └── code_reviewer.py  # コードレビューシステム
│   └── ui/                   # ユーザーインターフェース
│       └── approval_interface.py  # 承認インターフェース
├── data/                     # データ保存ディレクトリ
│   ├── instructions/         # 命令書保存先
│   ├── generated_code/       # 生成コード保存先
│   └── reviews/             # レビュー結果保存先
├── tests/                    # テストコード（現在空）
└── logs/                     # ログファイル保存先
```

## 主要な特徴

### CLI中心設計
- `hybrid_pair.py` を中心とする統一CLIインターフェース
- Windows環境向け `.bat` ファイルによる簡単実行
- 段階的ワークフローサポート

### 人間承認システム
- 命令書の人間レビュー・承認機能
- 承認者記録とトレーサビリティ
- セキュリティと品質のための必須承認プロセス

### 日本語対応
- 全コメント・ドキュメント日本語対応
- 日本語出力サポート
- UTF-8エンコーディング統一

### モジュラー設計
- 明確な責任分離（API、CLI、ワークフロー、品質管理）
- 拡張性を考慮したプラグイン構造
- 設定ベース動作制御
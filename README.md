# LLM×SLM ハイブリッドペアプログラミング システム

Claude 4 (LLM) と DeepSeek-Coder 6.7B (SLM) の協調開発システム  
効率的なコード生成と高品質な設計を両立させる革新的アプローチ

## 🎯 概要

このシステムは、Large Language Model (Claude) と Small Language Model (DeepSeek-Coder) を組み合わせて、効率的で高品質なコード生成を実現します。

### 役割分担
- **Claude (LLM)**: 設計・分析・レビュー・最適化
- **DeepSeek (SLM)**: 実装・コード生成・基本機能構築

### 人間承認ワークフロー
```
1. 人間 → 要件・機能説明
2. Claude → 命令書ドラフト作成
3. 人間 → 命令書レビュー・修正・承認  ★重要な人間判断
4. Claude → 承認された命令書をDeepSeekに送信
5. DeepSeek → 実装
6. Claude → コードレビュー・最適化
```

## 🚀 クイックスタート

### 1. 初期セットアップ
```bash
# バッチファイル実行（推奨）
run_hybrid_pair.bat setup

# または直接実行
python hybrid_pair.py setup
```

### 2. API設定
`config/config.json` を編集してAPIキーを設定：
- Claude API キー
- LM Studio エンドポイント設定

### 3. LM Studio準備
- [LM Studio](https://lmstudio.ai/) をダウンロード・起動
- DeepSeek-Coder 6.7B GGUF モデルを読み込み
- ローカルAPIサーバーを起動 (通常: http://localhost:1234)

### 4. 接続テスト
```bash
run_hybrid_pair.bat test
```

### 5. 最初の命令書作成
```bash
run_hybrid_pair.bat create sample_function
```

## 📋 基本的な使い方

### コマンド一覧

```bash
# システム管理
run_hybrid_pair.bat setup     # 初期セットアップ
run_hybrid_pair.bat test      # API接続テスト
run_hybrid_pair.bat status    # システム状況確認

# 命令書管理
run_hybrid_pair.bat create <機能名>         # 新規作成
run_hybrid_pair.bat list                    # 一覧表示
run_hybrid_pair.bat review <命令書ID>       # 詳細確認
run_hybrid_pair.bat approve <ID> --approver <名前>  # 承認

# 実行
run_hybrid_pair.bat execute <命令書ID>      # コード生成実行
```

### 典型的な作業フロー

1. **命令書作成**
   ```bash
   run_hybrid_pair.bat create user_authentication
   ```

2. **命令書確認・編集**
   ```bash
   run_hybrid_pair.bat review abc123def456
   # エディタが開くので内容を確認・編集
   ```

3. **承認**
   ```bash
   run_hybrid_pair.bat approve abc123def456 --approver "山田太郎"
   ```

4. **実行**
   ```bash
   run_hybrid_pair.bat execute abc123def456
   ```

5. **結果確認**
   - 生成されたコード: `data/generated_code/`
   - レビュー結果: `data/reviews/`

## 📁 プロジェクト構造

```
LLM_SLM_Hybrid_Pair_Programming/
├── hybrid_pair.py              # メインCLI
├── run_hybrid_pair.bat         # Windows実行用
├── requirements.txt            # 依存関係
├── config/
│   ├── config.json            # 設定ファイル（要編集）
│   ├── config.example.json    # 設定例
│   └── instruction_templates/ # 命令書テンプレート
├── src/
│   ├── core/                  # コアシステム
│   │   └── instruction_manager.py
│   ├── api/                   # APIクライアント
│   │   ├── llm_client.py      # Claude API
│   │   └── slm_client.py      # DeepSeek API
│   ├── cli/                   # コマンドラインツール
│   │   ├── instruction_creator.py
│   │   └── instruction_viewer.py
│   ├── workflow/              # ワークフロー管理
│   │   └── executor.py
│   └── quality_control/       # 品質管理
│       └── code_reviewer.py
├── data/                      # データ保存
│   ├── instructions/          # 命令書
│   ├── generated_code/        # 生成コード
│   └── reviews/              # レビュー結果
└── logs/                     # ログファイル
```

## ⚙️ 設定

### config.json の主要設定

```json
{
  "llm_config": {
    "api_key": "YOUR_CLAUDE_API_KEY_HERE",
    "model": "claude-3-sonnet-20240229"
  },
  "slm_config": {
    "api_endpoint": "http://localhost:1234/v1/chat/completions",
    "model": "deepseek-coder-6.7b-instruct-q5_k_m.gguf"
  },
  "workflow_config": {
    "require_human_approval": true
  }
}
```

## 💡 高度な使用方法

### カスタム命令書テンプレート
`config/instruction_templates/` に独自テンプレートを追加可能

### コードレビューカスタマイズ
`config/review_checklist.json` でレビュー基準をカスタマイズ

### 非対話モード
```bash
run_hybrid_pair.bat create batch_function --no-interactive
```

## 🔧 トラブルシューティング

### よくある問題

1. **LM Studio接続エラー**
   - LM Studioが起動しているか確認
   - ポート1234が使用されているか確認
   - ファイアウォール設定を確認

2. **Claude API エラー**
   - APIキーが正しく設定されているか確認
   - アカウントの残高・制限を確認

3. **命令書が見つからない**
   - `data/instructions/` ディレクトリの存在確認
   - 命令書IDの入力ミスを確認

### ログ確認
```bash
# 詳細ログは logs/ ディレクトリに保存されます
type logs\\latest.log
```

## 📈 パフォーマンス最適化

### 推奨設定
- **DeepSeek温度**: 0.2 (コード生成用)
- **Claude温度**: 0.1 (レビュー用)
- **SLMトークン**: 2000 (機能単位実装に最適)
- **LLMトークン**: 8000 (詳細レビュー用)

### リソース使用量
- SLM: ローカル実行 (GPU 4-6GB推奨)
- LLM: クラウドAPI (従量課金)

## 🤝 貢献・サポート

### フィードバック
- 問題報告やアイデアをお待ちしています
- `data/reviews/` の結果を共有していただけると改善に役立ちます

### カスタマイズ
- モジュラー設計により、容易に拡張・カスタマイズ可能
- 新しいSLMモデルの追加も簡単

## 📄 ライセンス

MIT License

## 🌟 今後の展望

- 複数SLMモデルの並列使用
- 言語特化モデルの統合
- CI/CDパイプライン連携
- Function Calling + Fine-tuning ハイブリッド

---

**🎉 効率的で高品質なコード開発を、LLM×SLMハイブリッドで実現しましょう！**
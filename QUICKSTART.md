# 🚀 LLM×SLM ハイブリッドシステム クイックスタート

5分でシステムの動作確認を行うためのガイド

## 🎯 目標
- システムの基本動作確認
- 簡単な電卓関数の生成テスト
- 人間承認ワークフローの実践

## ⚡ 高速セットアップ（5分）

### Step 1: 初期化 (1分)
```bash
# プロジェクトディレクトリに移動
cd C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming

# システム初期化
run_hybrid_pair.bat setup
```

### Step 2: API設定 (2分)
`config/config.json` を編集：
```json
{
  "llm_config": {
    "api_key": "YOUR_CLAUDE_API_KEY_HERE"
  },
  "slm_config": {
    "api_endpoint": "http://localhost:1234/v1/chat/completions"
  }
}
```

### Step 3: LM Studio 準備 (2分)
- LM Studio を起動
- DeepSeek-Coder 6.7B を読み込み
- Local Server を開始

## 🧪 動作テスト（5分）

### Test 1: 接続確認 (1分)
```bash
# 基本接続テスト
run_hybrid_pair.bat test

# 詳細診断（問題がある場合）
python debug_connection.py
```

### Test 2: 命令書作成 (2分)
```bash
# テスト用電卓関数の命令書作成
run_hybrid_pair.bat create simple_calculator --template simple_calculator

# 生成された命令書IDをメモ（例: abc123def456）
```

### Test 3: 人間承認 (1分)
```bash
# 命令書の内容確認
run_hybrid_pair.bat review abc123def456

# 承認実行
run_hybrid_pair.bat approve abc123def456 --approver "テスト実行者"
```

### Test 4: コード生成 (1分)
```bash
# DeepSeek でコード生成 + Claude レビュー
run_hybrid_pair.bat execute abc123def456

# 生成ファイル確認
type data\generated_code\simple_calculator_*.py
type data\reviews\review_simple_calculator_*.json
```

## ✅ 成功確認チェックリスト

- [ ] `run_hybrid_pair.bat test` が成功
- [ ] 命令書作成が完了
- [ ] 人間承認が成功
- [ ] コード生成が完了
- [ ] 生成されたPythonファイルが存在
- [ ] Claudeレビューファイルが存在

## 🎉 成功時の出力例

**接続テスト成功:**
```
🔍 API接続テスト
===============================
🤖 SLM (DeepSeek) 接続テスト...
✅ SLM接続成功
🧠 LLM (Claude) 接続テスト...
✅ LLM接続成功
```

**コード生成成功:**
```
🚀 LLM×SLM ワークフロー実行
==================================
📋 実行対象: simple_calculator
⚙️ Step 1: DeepSeek でコード生成中...
✅ コード生成完了 (1247 文字)
🔍 Step 2: Claude でコードレビュー中...
✅ レビュー完了
✅ ワークフロー実行完了！
```

## 🚨 よくある問題

### 問題1: SLM接続失敗
```
❌ SLM接続失敗 - LM Studioを確認してください
```
**解決策:**
- LM Studio が起動しているか確認
- モデルが読み込まれているか確認
- Local Server が開始されているか確認

### 問題2: Claude API エラー
```
❌ LLM接続失敗 - APIキーを確認してください
```
**解決策:**
- `config/config.json` の `api_key` を確認
- Claude API の残高・制限を確認

### 問題3: 設定ファイルなし
```
❌ config.json が見つかりません
```
**解決策:**
```bash
run_hybrid_pair.bat setup
```

## 📚 次のステップ

基本動作確認後：

1. **カスタム関数作成:**
   ```bash
   run_hybrid_pair.bat create my_function --template basic_function
   ```

2. **システム状況確認:**
   ```bash
   run_hybrid_pair.bat status
   ```

3. **詳細ガイド確認:**
   - `README.md`: 完全な使用方法
   - `docs/LM_Studio_Setup_Guide.md`: 環境構築詳細
   - `MEMORY.md`: 開発進捗・詳細記録

## 💡 ヒント

- **初回は時間がかかる**: DeepSeekの初回実行は読み込みで5-10秒
- **GPU推奨**: CPUでも動作するがGPUの方が高速
- **メモリ確保**: 8GB以上のRAM空き容量を確保
- **継続実行**: 一度セットアップすれば次回から高速

---
*作成日: 2025-09-06*
*対象: システム動作確認・初回テスト*
# LM Studio セットアップガイド

DeepSeek-Coder 6.7B を使用したローカルSLM環境の構築手順

## 🎯 目標
- LM Studio でローカルSLMを稼働
- DeepSeek-Coder 6.7B GGUF モデルの動作確認
- ハイブリッドシステムとのAPI接続テスト

## 📋 前提条件

### システム要件
- **OS**: Windows 10/11 (64bit)
- **RAM**: 16GB以上推奨 (最低12GB)
- **GPU**: NVIDIA GPU 6GB VRAM以上推奨 (CPU推論も可能)
- **ストレージ**: 空き容量 10GB以上

### 推奨スペック
- **CPU**: Intel i7/AMD Ryzen 7 以上
- **GPU**: RTX 3060/4060 以上 (VRAM 8GB+)
- **RAM**: 32GB (複数モデル同時実行用)

## 🔧 Step 1: LM Studio のインストール

### 1.1 ダウンロード
1. [LM Studio公式サイト](https://lmstudio.ai/) へアクセス
2. "Download for Windows" をクリック
3. インストーラーをダウンロード (約 100MB)

### 1.2 インストール実行
```bash
# ダウンロードしたファイルを実行
LM_Studio-x.x.x-Setup.exe
```

### 1.3 初期設定
1. LM Studio を起動
2. 初期設定ウィザードを実行
3. GPU使用設定を確認 (NVIDIA GPU がある場合)

## 🤖 Step 2: DeepSeek-Coder モデルの取得

### 2.1 モデル検索
1. LM Studio で "Search" タブを開く
2. 検索ボックスに「deepseek coder」と入力
3. 以下のモデルを探す：
   - `deepseek-ai/deepseek-coder-6.7b-instruct-gguf`
   - ファイル名: `deepseek-coder-6.7b-instruct.Q5_K_M.gguf`

### 2.2 推奨モデル選択基準
```
モデルサイズと品質のバランス:

Q5_K_M (推奨): 
- ファイルサイズ: ~4.8GB
- RAM使用量: ~8GB
- 品質: 高品質とパフォーマンスのバランス

Q4_K_M (軽量版):
- ファイルサイズ: ~4.1GB  
- RAM使用量: ~6GB
- 品質: やや軽量だが実用的

Q8_0 (高品質版):
- ファイルサイズ: ~7.2GB
- RAM使用量: ~12GB
- 品質: 最高品質だがリソース消費大
```

### 2.3 ダウンロード実行
1. `deepseek-coder-6.7b-instruct.Q5_K_M.gguf` を選択
2. "Download" ボタンをクリック
3. ダウンロード完了まで待機 (約 4.8GB)

## ⚙️ Step 3: モデルの読み込みと設定

### 3.1 モデル読み込み
1. "My Models" タブに移動
2. ダウンロードしたモデルを選択
3. "Load Model" をクリック

### 3.2 推奨設定
```yaml
Context Length: 4096
Temperature: 0.2        # コード生成用（低め）
Top P: 0.9
Top K: 40
Repeat Penalty: 1.1
```

### 3.3 GPU設定 (該当する場合)
- "GPU Acceleration" を有効化
- GPU layers: 自動設定を使用
- VRAM使用量を監視

## 🌐 Step 4: ローカルAPI サーバー起動

### 4.1 サーバー設定
1. "Local Server" タブを開く
2. 以下の設定を確認：
   ```
   Port: 1234 (デフォルト)
   Host: localhost
   CORS: Enabled
   ```

### 4.2 サーバー起動
1. モデルが読み込まれていることを確認
2. "Start Server" をクリック
3. 状態が "Server Running" になることを確認

### 4.3 動作確認
```bash
# PowerShell でテスト
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-coder-6.7b-instruct",
    "messages": [{"role": "user", "content": "print hello world in python"}],
    "max_tokens": 100,
    "temperature": 0.2
  }'
```

## 🔍 Step 5: ハイブリッドシステム接続テスト

### 5.1 設定ファイル準備
```bash
cd C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming
python hybrid_pair.py setup
```

### 5.2 config.json 編集
```json
{
  "slm_config": {
    "api_endpoint": "http://localhost:1234/v1/chat/completions",
    "model": "deepseek-coder-6.7b-instruct",
    "max_tokens": 2000,
    "temperature": 0.2,
    "timeout": 30
  }
}
```

### 5.3 接続テスト実行
```bash
python hybrid_pair.py test
```

期待される出力：
```
🔍 API接続テスト
===============================
🤖 SLM (DeepSeek) 接続テスト...
✅ SLM接続成功
```

## 🚨 トラブルシューティング

### よくある問題と解決策

#### 問題1: モデル読み込み失敗
```
エラー: "Failed to load model"
解決策:
- RAMの空き容量を確認 (8GB以上必要)
- 他のアプリケーションを終了
- より小さいモデル (Q4_K_M) を試す
```

#### 問題2: API接続エラー
```
エラー: "Connection refused"
解決策:
- LM Studio サーバーが起動していることを確認
- ポート1234が他のプロセスで使用されていないか確認
- Windowsファイアウォール設定を確認
```

#### 問題3: 生成速度が遅い
```
原因: CPU推論モード
解決策:
- GPU使用が有効になっているか確認
- GPU layers設定を調整
- システムリソース監視 (Task Manager)
```

#### 問題4: メモリ不足
```
エラー: "Out of memory"
解決策:
- Context Lengthを削減 (4096 → 2048)
- より軽量なモデル (Q4_K_M) に変更
- 他のアプリケーションを終了
```

## 📊 パフォーマンス最適化

### CPU使用時の最適化
- Context Length: 2048-4096
- Batch Size: 1-2
- Threads: CPU コア数の50-70%

### GPU使用時の最適化  
- GPU Layers: 自動設定
- VRAM監視: 使用量80%以下を維持
- GPU温度: 80°C以下を推奨

## ✅ セットアップ完了確認リスト

- [ ] LM Studio インストール完了
- [ ] DeepSeek-Coder 6.7B ダウンロード完了
- [ ] モデル読み込み成功
- [ ] ローカルAPIサーバー起動成功
- [ ] curl テスト成功
- [ ] hybrid_pair.py test 成功

## 📝 次のステップ

セットアップ完了後：
1. 最初の命令書作成: `python hybrid_pair.py create sample_function`
2. 実際のコード生成テスト
3. Claude レビュー機能テスト

---
*作成日: 2025-09-06*
*対象: Phase 1 - LM Studio環境構築*
# LLM-SLMハイブリッドシステム トラブルシューティングガイド

## システムの核心目的
**ClaudeCodeの負担軽減 → 作業時間延長**

## 役割分担の明確化
- **🤖 SLM（DeepSeek）:** メインのコード生成担当
- **🧠 Claude Code:** 小修正・最適化・判断・エラー対応・レビュー担当

## よく発生するエラーと解決方法

### 1. 依存関係エラー
**問題:** `ModuleNotFoundError: No module named 'loguru'`
**解決方法:**
```bash
# システムPythonを使用
C:/Python313/python.exe -m pip install -r requirements.txt
# または個別インストール
C:/Python313/python.exe -m pip install loguru
```

### 2. パス・エンコーディング問題
**問題:** Pythonパスの認識エラー、Unicode文字エラー
**解決方法:**
- システムPython: `C:/Python313/python.exe` を明示的に使用
- エンコーディング: UTF-8絵文字を避け、ASCII文字を使用

### 3. 対話モード入力エラー
**問題:** `EOFError: EOF when reading a line`
**解決方法:**
- `--no-interactive` フラグを常に使用
- 直接JSONファイルを編集してステータス変更

### 4. 命令書ステータス問題
**有効なステータス:** `draft`, `pending_review`, `under_review`, `approved`, `rejected`, `executed`, `archived`
**承認フロー:** `draft` → `pending_review` → `approved` → `executed`

## システム使用の最適化手順

### 1. 環境確認
```bash
cd "C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming"
C:/Python313/python.exe hybrid_pair.py setup  # 初回のみ
```

### 2. テンプレート準備
- 事前に適切な instruction_template を準備
- 複雑な要件は詳細なテンプレートで対応

### 3. 命令書作成（非対話モード）
```bash
C:/Python313/python.exe hybrid_pair.py create <function_name> --template <template_name> --no-interactive
```

### 4. 承認処理（手動編集）
ステータス変更: `"status": "pending_review"` → `"status": "approved"`
承認情報追加:
```json
"approved_at": "2025-09-06T20:02:30.000000",
"approved_by": "Claude-4"
```

### 5. 実行
```bash
C:/Python313/python.exe hybrid_pair.py execute <instruction_id>
```

## Pythonパス設定
**優先順位:**
1. `C:/Python313/python.exe` (システムPython)
2. `python` (環境変数Python)
3. `py -3` (Pythonランチャー)

## 設定ファイルの注意点
- `config/config.json` - APIキー設定が必要だが、テスト目的では無視可能
- LM Studio設定は実際の使用時のみ必要
- 接続テストエラーは無視可能（コード生成機能は動作する）

## ファイル配置ルール
- **開発用:** LLM_SLM_Hybrid_Pair_Programming フォルダ内
- **配布用:** デスクトップや目的のフォルダに移動
- **クリーンアップ:** システムフォルダから配布物を削除

## エラー回避のベストプラクティス
1. **非対話モード使用:** 常に `--no-interactive` フラグ
2. **明示的Pythonパス:** `C:/Python313/python.exe` を使用
3. **ステータス手動管理:** JSONファイル直接編集
4. **エンコーディング注意:** 絵文字・特殊文字を避ける
5. **依存関係事前確認:** requirements.txt のインストール確認

## 成功パターンのワークフロー
1. テンプレート作成/選択
2. 非対話モードで命令書作成
3. JSONファイル直接編集で承認
4. SLMでコード生成実行
5. ClaudeCodeで小修正・最適化
6. 配布用ディレクトリに移動・整理

## 次回セッション用チェックリスト
- [ ] Pythonパス確認: `C:/Python313/python.exe`
- [ ] 依存関係確認: `pip install -r requirements.txt`
- [ ] システム設定確認: `hybrid_pair.py setup`
- [ ] 非対話モード使用: `--no-interactive`
- [ ] ステータス管理: JSON直接編集
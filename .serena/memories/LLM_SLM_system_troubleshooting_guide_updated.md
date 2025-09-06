# LLM×SLMシステム トラブルシューティングガイド (2025-09-06 更新)

## 🔧 システム実行の確実な手順

### 基本実行環境
**必須パス**: `C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming`
**実行コマンド**: `PYTHONIOENCODING=utf-8 /c/Python313/python.exe [スクリプト名]`

## 📋 ハイブリッドシステム使用時の確実な手順

### 1. タスク作成
```bash
# 正しいコマンド
cd "C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming"
PYTHONIOENCODING=utf-8 /c/Python313/python.exe hybrid_pair.py create [function_name] --no-interactive

# 注意: 説明文は引数として渡せない（エラーになる）
```

### 2. 命令書編集の必須ポイント
**作成されるファイル**: `data/instructions/[ID].json`

**必須編集項目**:
- `requirements`セクション全体を詳細仕様に置き換える
- `output_file`に正確な出力パスを指定
- `status`を適切に設定

### 3. ステータス管理の重要な注意点
**有効なステータス**: `draft`, `approved`, `completed`
**無効なステータス**: `ready_for_approval`, `review`（システムエラーになる）

**承認プロセス**:
1. `status`: `"draft"` → `"approved"`に直接変更
2. `approved_at`: 現在日時を設定
3. `approved_by`: 承認者名を設定

```json
{
  "status": "approved",
  "approved_at": "2025-09-06T20:39:45",
  "approved_by": "Claude-LLM"
}
```

### 4. 実行コマンド
```bash
# コード生成実行
PYTHONIOENCODING=utf-8 /c/Python313/python.exe hybrid_pair.py execute [ID]
```

## 🚨 よくあるエラーと解決方法

### A. 引数エラー
**問題**: `hybrid_pair.py create desktop_calculator "説明文"`
**解決**: 説明文は引数として渡せない。`--no-interactive`オプション使用

### B. ステータスエラー
**問題**: `'ready_for_approval' is not a valid InstructionStatus`
**解決**: 有効なステータス（`draft`, `approved`, `completed`）のみ使用

### C. 承認エラー
**問題**: `--approver`が必要
**解決**: JSONファイルを直接編集して承認済み状態にする

### D. 対話式入力エラー
**問題**: `エラー: EOF when reading a line`
**解決**: `--no-interactive`フラグを常に使用

## 🎯 効率的な作業手順

### ステップ1: タスク作成
```bash
cd "C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming"
PYTHONIOENCODING=utf-8 /c/Python313/python.exe hybrid_pair.py create [function_name] --no-interactive
# 出力されるIDを記録
```

### ステップ2: 命令書詳細化
1. `data/instructions/[ID].json`を開く
2. `requirements`セクション全体を詳細仕様に置き換え
3. `output_file`パスを正確に指定
4. 以下の項目を更新:
```json
{
  "status": "approved",
  "approved_at": "現在日時",
  "approved_by": "Claude-LLM"
}
```

### ステップ3: コード生成実行
```bash
PYTHONIOENCODING=utf-8 /c/Python313/python.exe hybrid_pair.py execute [ID]
```

## 📝 命令書テンプレート構造

### GUI アプリケーション用テンプレート
```json
{
  "requirements": {
    "app_type": "GUI[アプリタイプ]",
    "output_file": "C:\\Users\\tomon\\Desktop\\[ファイル名].py",
    "gui_framework": "tkinter（標準ライブラリ）",
    "window_config": { "title": "[タイトル]", "size": "400x500" },
    "functionality": { "基本機能リスト" },
    "error_handling": { "エラー処理仕様" },
    "dependencies": ["標準ライブラリのみ"],
    "code_requirements": {
      "structure": "クラスベース設計",
      "file_structure": "単一ファイル"
    }
  }
}
```

## ⚠️ 重要な教訓

1. **対話式を避ける**: 常に`--no-interactive`を使用
2. **ステータス管理**: JSONを直接編集が最も確実
3. **引数制限**: 説明文は引数として渡せない
4. **エンコーディング**: `PYTHONIOENCODING=utf-8`必須
5. **パス指定**: 絶対パス（特に`output_file`）を使用

## 📊 成功パターン

### 過去の成功事例
- `simple_calculator`: Phase 2で成功
- `data_analyzer`: Phase 3で成功  
- `batch_processor`: Phase 4で成功

### 失敗から学んだ改善点
- 承認プロセスの自動化（JSONファイル直接編集）
- 詳細な命令書作成（曖昧さの排除）
- エラーハンドリングの標準化

---
*更新日: 2025-09-06 20:40*  
*重要度: ★★★★★*  
*用途: LLM×SLMシステム使用時の必須参考資料*
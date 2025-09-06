# システム環境・実行方法 重要メモ (2025-09-06 21:50)

## 🔧 重要: グローバルPython環境実行の必要性

### 実行環境問題と解決方法
**問題**: venv環境とライブラリの不一致
- `ModuleNotFoundError: No module name 'loguru'`
- `ModuleNotFoundError: No module name 'requests'`

### ✅ 解決方法: グローバルPython環境での実行
**必須実行パターン**:
```bash
cd "C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming"
PYTHONIOENCODING=utf-8 /c/Python313/python.exe [スクリプト名]
```

### 実行成功事例
1. **Phase 2 電卓実行** (以前の成功):
   ```bash
   PYTHONIOENCODING=utf-8 /c/Python313/python.exe hybrid_pair.py execute [ID]
   ```

2. **Phase 3 data_analyzer実行** (本セッション成功):
   ```bash
   PYTHONIOENCODING=utf-8 /c/Python313/python.exe manual_data_analyzer_test.py
   PYTHONIOENCODING=utf-8 /c/Python313/python.exe test_data_analyzer.py
   ```

### 環境設定詳細
- **Pythonパス**: `/c/Python313/python.exe` (グローバル環境)
- **文字エンコード**: `PYTHONIOENCODING=utf-8` (日本語対応)
- **作業ディレクトリ**: プロジェクトルート必須

## 📋 今後の開発での必須事項

### 実行コマンド標準化
**テンプレート**:
```bash
cd "C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming"
PYTHONIOENCODING=utf-8 /c/Python313/python.exe [実行ファイル]
```

### 新規スクリプト作成時の注意
1. **依存関係**: グローバル環境でのライブラリ可用性確認
2. **インポートパス**: `sys.path.append(str(PROJECT_ROOT / "src"))` 必要
3. **実行テスト**: 必ずグローバル環境で動作確認

### トラブルシューティング手順
1. グローバル環境で実行 → 成功
2. venv環境で実行 → 失敗する可能性高
3. ライブラリ不足時 → `pip install [package]` でグローバル環境にインストール

---
*重要度: ★★★★★ - プロジェクト実行の根幹*
*記録日: 2025-09-06 21:50*
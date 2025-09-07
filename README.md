# 超シンプルハイブリッド実行システム

**3つの機能だけ：**
1. 命令書を受け取る（人間から直接）
2. SLMにコードを生成させる  
3. 指定場所にファイル保存

## 使用方法

### 1. 基本実行（対話モード）
```bash
python ultra_simple.py
```
- 命令書を入力（改行2回で終了）
- 保存パスを指定（例: C:/projects/my_app.py）
- 自動でコード生成・保存

### 2. プログラムから実行
```python
from quick_execute import quick_hybrid

# ワンライナーで実行
quick_hybrid(
    "電卓アプリを作って", 
    "C:/projects/calculator.py"
)
```

### 3. ClaudeCodeから実行
```python
# ClaudeCodeで以下を実行
exec(open('quick_execute.py').read())
quick_hybrid("要件をここに書く", "保存パス")
```

## 設定ファイル

`simple_config.json` が自動作成されます：

```json
{
  "deepseek_api": {
    "endpoint": "http://localhost:1234/v1/chat/completions",
    "model": "deepseek-coder-6.7b-instruct",
    "temperature": 0.2,
    "max_tokens": 2000
  }
}
```

## モデル選択

LM Studioで任意のモデルを選択するだけ。設定ファイルのmodel名は参考程度。

## 完全な実行例

```python
from ultra_simple import UltraSimpleHybrid

hybrid = UltraSimpleHybrid()
hybrid.execute_instruction(
    """
    家計簿アプリを作成してください：
    - 収入・支出の記録
    - 月別集計表示  
    - CSV出力機能
    - tkinterでGUI
    """, 
    "C:/projects/budget/household_app.py"
)
```

## システム要件

- Python 3.7+
- requests ライブラリ
- LM Studio + 任意のコーディングモデル

これだけです！
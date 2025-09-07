# 超シンプルハイブリッド実行システム

**3つの機能だけ：**
1. 命令書を受け取る（人間から直接）
2. SLMにコードを生成させる  
3. 指定場所にファイル保存

## 使用方法

### 1. 基本実行
```bash
python ultra_simple.py
```

### 2. プログラムから実行
```python
from quick_execute import quick_hybrid

# ワンライナーで実行
quick_hybrid(
    "電卓アプリを作って", 
    "calculator_app", 
    "calc.py"
)
```

### 3. ClaudeCodeから実行
```python
# ClaudeCodeで以下を実行
exec(open('quick_execute.py').read())
quick_hybrid("要件をここに書く", "プロジェクト名")
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
  },
  "output_settings": {
    "base_directory": "output",
    "create_project_folders": true
  }
}
```

## ファイル構造

```
output/
├── プロジェクト名1/
│   ├── ファイル1.py
│   └── ファイル2.py
├── プロジェクト名2/
│   └── ファイル.py
└── ...
```

## 前提条件

- LM Studio で DeepSeek-Coder が起動中
- ポート 1234 で API サーバーが動作中

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
    "household_budget",
    "budget_app.py"
)
```

## システム要件

- Python 3.7+
- requests ライブラリ
- LM Studio + DeepSeek-Coder

これだけです！
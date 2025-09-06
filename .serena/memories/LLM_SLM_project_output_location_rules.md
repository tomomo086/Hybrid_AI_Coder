# LLM-SLMシステム プロジェクト出力場所ルール

## 基本原則
**LLM-SLMハイブリッドシステムで生成したプログラムは、システムフォルダ外の適切な場所に配置する**

## 配置場所の階層

### 1. メイン開発フォルダ
**場所:** `C:\Users\tomon\dev\projects\`
**用途:** LLM-SLMシステムで生成した完成品プロジェクトの配置
**例:** `C:\Users\tomon\dev\projects\MyCalculatorApp\`

### 2. LLM-SLMシステムフォルダ（作業用のみ）
**場所:** `C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming\`
**用途:** 
- システム自体の管理・設定
- 一時的なコード生成作業
- 命令書・テンプレートの管理
**重要:** 完成品は必ずここから移動させる

### 3. デスクトップ（即使用・デモ用）
**場所:** `C:\Users\tomon\Desktop\`
**用途:** 
- ワンクリック起動が必要なアプリ
- デモ・プレゼンテーション用
- 即座に使用したいツール

## プロジェクト配置の標準ワークフロー

### ステップ1: システム内で開発
1. LLM-SLMシステムフォルダ内で開発作業
2. SLMによるコード生成
3. ClaudeCodeによる最適化・改良

### ステップ2: 適切な場所への移動
```bash
# 基本パターン
mkdir "C:\Users\tomon\dev\projects\{ProjectName}"
cp システム生成ファイル "C:\Users\tomon\dev\projects\{ProjectName}\"

# デスクトップ版が必要な場合
mkdir "C:\Users\tomon\Desktop\{ProjectName}"
cp 必要ファイル "C:\Users\tomon\Desktop\{ProjectName}\"
```

### ステップ3: システムフォルダのクリーンアップ
```bash
# 生成物を削除してシステムを清潔に保つ
rm システム内の配布済みファイル
```

## プロジェクトタイプ別配置ルール

### アプリケーション系
**配置先:** `C:\Users\tomon\dev\projects\{AppName}\`
**構成例:**
```
C:\Users\tomon\dev\projects\AdvancedCalculator\
├── main.py
├── run_app.bat
├── requirements.txt
├── README.md
└── config\
```

### ユーティリティ・ツール系
**配置先:** `C:\Users\tomon\dev\projects\{ToolName}\`
**デスクトップコピー:** 使用頻度が高い場合
**構成例:**
```
C:\Users\tomon\dev\projects\FileOrganizer\
├── file_organizer.py
├── utils\
└── tests\
```

### ライブラリ・モジュール系
**配置先:** `C:\Users\tomon\dev\projects\{LibraryName}\`
**構成例:**
```
C:\Users\tomon\dev\projects\MyUtilsLibrary\
├── my_utils\
│   ├── __init__.py
│   └── core.py
├── setup.py
└── tests\
```

### 学習・実験用コード
**配置先:** `C:\Users\tomon\dev\projects\experiments\{ExperimentName}\`
**特徴:** 軽量、単発用途

## 自動化スクリプトの提案

### プロジェクト移動スクリプト
```bash
# move_project.bat の例
@echo off
set PROJECT_NAME=%1
set SOURCE_DIR=C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming
set TARGET_DIR=C:\Users\tomon\dev\projects\%PROJECT_NAME%

mkdir "%TARGET_DIR%"
copy "%SOURCE_DIR%\*.py" "%TARGET_DIR%\"
copy "%SOURCE_DIR%\*.bat" "%TARGET_DIR%\"
copy "%SOURCE_DIR%\README.md" "%TARGET_DIR%\" 2>nul

echo プロジェクト %PROJECT_NAME% を %TARGET_DIR% に移動しました
```

### プロジェクト作成テンプレート
LLM-SLMシステムに以下のテンプレートを追加推奨:
- `standalone_application.json` - 独立アプリケーション用
- `desktop_tool.json` - デスクトップツール用  
- `utility_library.json` - ユーティリティライブラリ用

## ベストプラクティス

### 1. 命名規則
- **プロジェクト名:** PascalCase (例: `AdvancedCalculator`)
- **ファイル名:** snake_case (例: `advanced_calculator.py`)
- **フォルダ名:** snake_case または PascalCase

### 2. 必須ファイル
各プロジェクトには以下を必ず含める:
- `README.md` - プロジェクト説明
- `run_*.bat` - Windows実行用（該当する場合）
- `requirements.txt` - 依存関係（該当する場合）

### 3. システム管理
- LLM-SLMシステムフォルダは作業用のみ
- 完成品は必ず適切な場所に移動
- 定期的なシステムフォルダクリーンアップ

### 4. バックアップ考慮
- 重要なプロジェクトは複数の場所に保持
- git管理の検討（該当する場合）

## ClaudeCode用チェックリスト

LLM-SLMシステムでプロジェクト生成時は以下を確認:
- [ ] 適切な配置場所の決定
- [ ] プロジェクト構造の計画
- [ ] 移動用スクリプト/コマンドの準備
- [ ] システムフォルダからの移動実行
- [ ] 移動後のクリーンアップ
- [ ] 最終動作確認

この配置ルールにより、システムフォルダを清潔に保ちながら、生成したプロジェクトを適切な場所で管理できます。
# LLM-SLMシステム 自動プロジェクト配置スクリプト

## 自動化の目的
生成したプロジェクトを効率的に適切な場所に配置し、システムフォルダをクリーンに保つ

## 推奨自動化スクリプト

### 1. プロジェクト移動用バッチファイル

**ファイル名:** `deploy_project.bat`
**配置場所:** `C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming\`

```batch
@echo off
chcp 65001 >nul
title LLM-SLM プロジェクト配置ツール

echo LLM-SLM プロジェクト自動配置
echo ============================

if "%1"=="" (
    echo 使用方法: deploy_project.bat ProjectName [desktop]
    echo 例: deploy_project.bat MyCalculatorApp
    echo 例: deploy_project.bat MyTool desktop  ^(デスクトップにも配置^)
    pause
    exit /b 1
)

set PROJECT_NAME=%1
set DEPLOY_TO_DESKTOP=%2
set SOURCE_DIR=%~dp0
set TARGET_DIR=C:\Users\tomon\dev\projects\%PROJECT_NAME%
set DESKTOP_DIR=C:\Users\tomon\Desktop\%PROJECT_NAME%

echo プロジェクト名: %PROJECT_NAME%
echo 配置先: %TARGET_DIR%

REM メインディレクトリ作成
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

REM 主要ファイルのコピー
echo ファイルをコピー中...
for %%f in (*.py *.bat *.json *.md *.txt) do (
    if exist "%SOURCE_DIR%%%f" (
        copy "%SOURCE_DIR%%%f" "%TARGET_DIR%\" >nul 2>&1
        echo   %%f をコピーしました
    )
)

REM サブディレクトリのコピー（必要に応じて）
if exist "%SOURCE_DIR%config" (
    xcopy "%SOURCE_DIR%config" "%TARGET_DIR%\config\" /E /I /Q >nul
    echo   config フォルダをコピーしました
)

if exist "%SOURCE_DIR%utils" (
    xcopy "%SOURCE_DIR%utils" "%TARGET_DIR%\utils\" /E /I /Q >nul
    echo   utils フォルダをコピーしました
)

REM デスクトップ配置（オプション）
if /i "%DEPLOY_TO_DESKTOP%"=="desktop" (
    echo デスクトップにも配置中...
    if not exist "%DESKTOP_DIR%" mkdir "%DESKTOP_DIR%"
    
    REM 主要実行ファイルのみデスクトップに
    for %%f in (*.py run_*.bat) do (
        if exist "%SOURCE_DIR%%%f" (
            copy "%SOURCE_DIR%%%f" "%DESKTOP_DIR%\" >nul 2>&1
        )
    )
    
    REM README もコピー
    if exist "%SOURCE_DIR%README.md" (
        copy "%SOURCE_DIR%README.md" "%DESKTOP_DIR%\" >nul 2>&1
    )
    
    echo デスクトップ配置完了: %DESKTOP_DIR%
)

echo.
echo ✅ プロジェクト配置完了
echo 📁 メイン: %TARGET_DIR%
if /i "%DEPLOY_TO_DESKTOP%"=="desktop" (
    echo 🖥️  デスクトップ: %DESKTOP_DIR%
)

echo.
echo 次のステップ:
echo 1. 配置されたプロジェクトの動作確認
echo 2. システムフォルダのクリーンアップ（cleanup_system.bat）
echo.

pause
```

### 2. システムクリーンアップ用スクリプト

**ファイル名:** `cleanup_system.bat`
**配置場所:** `C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming\`

```batch
@echo off
chcp 65001 >nul
title LLM-SLM システムクリーンアップ

echo LLM-SLM システムクリーンアップ
echo ===============================
echo.
echo 以下のファイルを削除してシステムフォルダを整理します:
echo - 配置済みプロジェクトファイル（*.py, *.bat等）
echo - 一時的なテストファイル
echo.
echo 注意: システム本体ファイルは保護されます
echo.

set /p CONFIRM=実行しますか？ (y/N): 
if /i not "%CONFIRM%"=="y" (
    echo キャンセルしました
    pause
    exit /b 0
)

echo.
echo クリーンアップ中...

REM 配置対象ファイルの削除（システムファイル以外）
for %%f in (*.py *.bat) do (
    if not "%%f"=="hybrid_pair.py" (
        if not "%%f"=="run_hybrid_pair.bat" (
            if not "%%f"=="deploy_project.bat" (
                if not "%%f"=="cleanup_system.bat" (
                    if exist "%%f" (
                        del "%%f" >nul 2>&1
                        echo   %%f を削除しました
                    )
                )
            )
        )
    )
)

REM README.md の削除（必要に応じて）
if exist "project_README.md" (
    del "project_README.md" >nul 2>&1
    echo   project_README.md を削除しました
)

REM requirements.txt の削除（プロジェクト固有のもの）
if exist "project_requirements.txt" (
    del "project_requirements.txt" >nul 2>&1
    echo   project_requirements.txt を削除しました
)

echo.
echo ✅ クリーンアップ完了
echo システムフォルダが整理されました
echo.

pause
```

### 3. プロジェクト作成統合スクリプト

**ファイル名:** `create_and_deploy.bat`
**用途:** 命令書作成から配置まで一括実行

```batch
@echo off
chcp 65001 >nul
title LLM-SLM 統合プロジェクト作成

echo LLM-SLM 統合プロジェクト作成ツール
echo ================================

if "%1"=="" (
    echo 使用方法: create_and_deploy.bat ProjectName [Template] [desktop]
    echo 例: create_and_deploy.bat MyApp basic_function
    echo 例: create_and_deploy.bat MyTool simple_utility desktop
    pause
    exit /b 1
)

set PROJECT_NAME=%1
set TEMPLATE=%2
set DEPLOY_DESKTOP=%3

if "%TEMPLATE%"=="" set TEMPLATE=basic_function

echo プロジェクト名: %PROJECT_NAME%
echo テンプレート: %TEMPLATE%
echo.

REM ステップ1: 命令書作成
echo ステップ1: 命令書作成中...
C:/Python313/python.exe hybrid_pair.py create %PROJECT_NAME% --template %TEMPLATE% --no-interactive

if errorlevel 1 (
    echo ❌ 命令書作成に失敗しました
    pause
    exit /b 1
)

echo ✅ 命令書作成完了

REM ステップ2: 承認処理（自動）
echo ステップ2: 自動承認処理中...
REM ここで最新の命令書IDを取得して承認処理
REM （実装は命令書ID取得ロジックが必要）

echo ステップ3: コード生成をお待ちください...
echo 手動で承認とexecuteを実行してください
echo その後、deploy_project.bat を実行してください
echo.

pause
```

## 使用方法

### 基本的な使用パターン
```bash
# 1. プロジェクト開発完了後
deploy_project.bat MyCalculatorApp

# 2. デスクトップにも配置したい場合
deploy_project.bat MyTool desktop

# 3. システムクリーンアップ
cleanup_system.bat
```

### 推奨ワークフロー
1. LLM-SLMシステムでプロジェクト開発
2. `deploy_project.bat ProjectName [desktop]` で配置
3. 配置先で動作確認
4. `cleanup_system.bat` でシステム整理

## メリット

### 効率化
- 手動コピーの手間削減
- 一貫性のあるプロジェクト構造
- 自動化されたクリーンアップ

### 管理向上  
- システムフォルダの整理
- プロジェクトの体系的配置
- バックアップと配布の容易性

### エラー削減
- 手動ミスの防止
- 標準化された配置プロセス
- 確認機能付き

これらのスクリプトにより、LLM-SLMシステムで生成したプロジェクトを効率的に管理できます。
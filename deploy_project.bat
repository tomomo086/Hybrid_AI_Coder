@echo off
chcp 65001 >nul
title LLM-SLM プロジェクト配置ツール

echo.
echo LLM-SLM プロジェクト自動配置
echo ============================

if "%1"=="" (
    echo 使用方法: deploy_project.bat ProjectName [desktop]
    echo 例: deploy_project.bat MyCalculatorApp
    echo 例: deploy_project.bat MyTool desktop  ^(デスクトップにも配置^)
    echo.
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
        REM システムファイルはスキップ
        if not "%%f"=="hybrid_pair.py" (
            if not "%%f"=="run_hybrid_pair.bat" (
                if not "%%f"=="deploy_project.bat" (
                    if not "%%f"=="cleanup_system.bat" (
                        copy "%SOURCE_DIR%%%f" "%TARGET_DIR%\" >nul 2>&1
                        echo   %%f をコピーしました
                    )
                )
            )
        )
    )
)

REM デスクトップ配置（オプション）
if /i "%DEPLOY_TO_DESKTOP%"=="desktop" (
    echo デスクトップにも配置中...
    if not exist "%DESKTOP_DIR%" mkdir "%DESKTOP_DIR%"
    
    REM 主要実行ファイルのみデスクトップに
    for %%f in (*.py run*.bat) do (
        if exist "%SOURCE_DIR%%%f" (
            REM システムファイルはスキップ
            if not "%%f"=="hybrid_pair.py" (
                if not "%%f"=="run_hybrid_pair.bat" (
                    copy "%SOURCE_DIR%%%f" "%DESKTOP_DIR%\" >nul 2>&1
                )
            )
        )
    )
    
    REM README もコピー（システムREADME以外）
    if exist "%SOURCE_DIR%project_README.md" (
        copy "%SOURCE_DIR%project_README.md" "%DESKTOP_DIR%\README.md" >nul 2>&1
    )
    
    echo デスクトップ配置完了: %DESKTOP_DIR%
)

echo.
echo ✅ プロジェクト配置完了
echo 📁 メイン: %TARGET_DIR%
if /i "%DEPLOY_TO_DESKTOP%"=="desktop" (
    echo 🖥️ デスクトップ: %DESKTOP_DIR%
)

echo.
echo 次のステップ:
echo 1. 配置されたプロジェクトの動作確認
echo 2. システムフォルダのクリーンアップ（cleanup_system.bat）
echo.

pause
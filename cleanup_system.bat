@echo off
chcp 65001 >nul
title LLM-SLM システムクリーンアップ

echo.
echo LLM-SLM システムクリーンアップ
echo ===============================
echo.
echo 以下のファイルを削除してシステムフォルダを整理します:
echo - 配置済みプロジェクトファイル（*.py, *.bat等）
echo - 一時的なテストファイル
echo.
echo 注意: システム本体ファイルは保護されます
echo - hybrid_pair.py
echo - run_hybrid_pair.bat
echo - deploy_project.bat
echo - cleanup_system.bat
echo - requirements.txt
echo - README.md
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
    REM システムファイルを除外
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

REM プロジェクト固有ファイルの削除
if exist "project_README.md" (
    del "project_README.md" >nul 2>&1
    echo   project_README.md を削除しました
)

if exist "project_requirements.txt" (
    del "project_requirements.txt" >nul 2>&1
    echo   project_requirements.txt を削除しました
)

REM 一時ファイルの削除
for %%f in (test_*.py temp_*.py example_*.py) do (
    if exist "%%f" (
        del "%%f" >nul 2>&1
        echo   %%f を削除しました
    )
)

echo.
echo ✅ クリーンアップ完了
echo システムフォルダが整理されました
echo.
echo システム本体ファイルは保護されています:
dir /b hybrid_pair.py run_hybrid_pair.bat deploy_project.bat cleanup_system.bat 2>nul
echo.

pause
@echo off
chcp 65001 > nul

rem LLM×SLM ハイブリッドペアプログラミング システム 実行バッチファイル

echo 🤝 LLM×SLM ハイブリッドペアプログラミング システム
echo ==========================================

if "%1"=="" (
    echo.
    echo 使用例:
    echo   run_hybrid_pair.bat setup          システムセットアップ
    echo   run_hybrid_pair.bat test           接続テスト
    echo   run_hybrid_pair.bat create sample  命令書作成
    echo   run_hybrid_pair.bat list           命令書一覧
    echo   run_hybrid_pair.bat status         システム状況
    echo.
    echo 詳細ヘルプ:
    echo   run_hybrid_pair.bat --help
    echo.
    python hybrid_pair.py workflow
    goto :end
)

python hybrid_pair.py %*

:end
pause
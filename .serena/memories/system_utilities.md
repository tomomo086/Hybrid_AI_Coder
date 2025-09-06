# LLM×SLM ハイブリッドペアプログラミング - Windows システムユーティリティ

## Windows 固有のコマンド・ユーティリティ

### 基本ファイル操作

#### ディレクトリ操作
```cmd
# ディレクトリ移動
cd C:\Users\tomon\dev\projects\LLM_SLM_Hybrid_Pair_Programming
cd /d D:\projects\LLM_SLM_Hybrid_Pair_Programming    # ドライブ変更込み

# カレントディレクトリ確認
cd
echo %CD%

# ディレクトリ作成
mkdir data\new_folder
md logs\backup

# ディレクトリ削除（空の場合）
rmdir data\temp_folder
rd /s /q data\temp_folder    # 強制削除（内容込み）

# ディレクトリ一覧表示
dir                          # 基本一覧
dir /w                       # 横並び表示
dir /s                       # サブディレクトリ込み
dir /od                      # 日付順ソート
dir *.py                     # Python ファイルのみ
```

#### ファイル操作
```cmd
# ファイル表示
type config\config.json      # ファイル内容表示
more logs\latest.log         # ページング表示

# ファイルコピー
copy config\config.example.json config\config.json
xcopy src backup_src /E /I   # ディレクトリ構造込みコピー

# ファイル移動・リネーム
move old_file.py new_file.py
ren old_name.py new_name.py

# ファイル削除
del temp_file.txt
del /q /f *.tmp             # 強制削除（確認なし）

# ファイル検索
dir /s /b *.py              # Python ファイル検索
where python                # 実行ファイルの場所検索
```

### テキスト検索・処理

#### findstr コマンド（grep相当）
```cmd
# ファイル内文字列検索
findstr "TODO" src\*.py                    # TODO コメント検索
findstr /R "def.*:" src\*.py               # 関数定義検索（正規表現）
findstr /I "error" logs\*.log              # 大文字小文字区別なし
findstr /N "import" src\core\*.py          # 行番号付き表示
findstr /S "api_key" *.py                  # サブディレクトリ込み検索

# 複数条件検索
findstr /R "class.*:\|def.*:" src\*.py     # クラス・関数定義検索
findstr "ERROR WARN" logs\*.log            # ERROR または WARN 検索
```

#### 文字コード・改行コード対応
```cmd
# UTF-8 文字コード設定
chcp 65001

# ファイル文字コード変換（PowerShell）
powershell "Get-Content config.json -Encoding UTF8 | Set-Content config_utf8.json -Encoding UTF8"
```

### プロセス・システム管理

#### プロセス管理
```cmd
# プロセス一覧
tasklist                     # 全プロセス一覧
tasklist /FI "IMAGENAME eq python.exe"    # Python プロセスのみ

# プロセス終了
taskkill /F /PID 1234        # プロセスIDで終了
taskkill /F /IM python.exe   # イメージ名で終了

# ポート使用状況確認
netstat -an | findstr :1234  # ポート1234の使用状況
netstat -ano | findstr :8501 # Streamlit デフォルトポート確認
```

#### システム情報
```cmd
# システム情報表示
systeminfo                  # システム詳細情報
ver                         # Windows バージョン
echo %COMPUTERNAME%         # コンピューター名
echo %USERNAME%            # ユーザー名
```

### 環境変数・パス管理

#### 環境変数操作
```cmd
# 環境変数表示
echo %PATH%                 # PATH 環境変数
echo %USERPROFILE%          # ユーザーホームディレクトリ
set                         # 全環境変数表示

# 一時的な環境変数設定
set CLAUDE_API_KEY=your_key_here
set PYTHONPATH=%CD%;%PYTHONPATH%

# 永続的な環境変数設定（PowerShell Admin が必要）
setx CLAUDE_API_KEY "your_key_here"
```

#### パス関連
```cmd
# Python 実行パス確認
where python
python -c "import sys; print('\n'.join(sys.path))"

# プロジェクトルートの絶対パス取得
echo %CD%
for %I in (.) do echo %~fI
```

### ネットワーク・接続確認

#### LM Studio / API 接続確認
```cmd
# ポート接続テスト
telnet localhost 1234       # LM Studio ポート確認
netstat -an | findstr :1234 # ポート使用状況

# HTTP 接続テスト（PowerShell）
powershell "Invoke-RestMethod -Uri 'http://localhost:1234/v1/models' -Method Get"

# ping テスト
ping localhost
ping 8.8.8.8               # インターネット接続確認
```

#### curlコマンド（Windows 10 1803以降）
```cmd
# API エンドポイントテスト
curl -X GET http://localhost:1234/v1/models
curl -X POST http://localhost:1234/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"deepseek-coder\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}"
```

### ログ・デバッグユーティリティ

#### ログファイル監視
```cmd
# ログファイルの末尾監視（PowerShell）
powershell "Get-Content logs\latest.log -Wait -Tail 10"

# ログローテーション用日付
echo %DATE:~0,4%-%DATE:~5,2%-%DATE:~8,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
```

#### ファイル変更監視
```cmd
# ファイル更新日時確認
dir /T:W logs\*.log         # 書き込み時間順表示
forfiles /P logs /M *.log /C "cmd /c echo @path @fdate @ftime"
```

### バックアップ・アーカイブ

#### データバックアップ
```cmd
# ディレクトリバックアップ
xcopy data backup_data_%DATE:~0,4%%DATE:~5,2%%DATE:~8,2% /E /I /Y

# 設定ファイルバックアップ
copy config\config.json config\config.backup_%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%.json

# 圧縮アーカイブ作成（PowerShell）
powershell "Compress-Archive -Path data -DestinationPath backup_$(Get-Date -Format 'yyyyMMdd').zip"
```

### Git 操作（Windows）

#### Git Bash / Git CMD
```cmd
# Git 状況確認
git status
git log --oneline -10       # 直近10コミット
git branch -a               # 全ブランチ表示

# 変更確認
git diff
git diff --name-only        # ファイル名のみ
git diff --cached           # ステージング済み変更

# コミット・プッシュ
git add .
git commit -m "機能追加: [変更内容]"
git push origin main
```

### PowerShell 高度なコマンド

#### JSON 操作
```powershell
# JSON ファイル読み書き
$config = Get-Content config\config.json | ConvertFrom-Json
$config.llm_config.model
$config | ConvertTo-Json -Depth 4 | Set-Content config\config_modified.json
```

#### プロセス監視・制御
```powershell
# Python プロセス詳細
Get-Process | Where-Object {$_.ProcessName -eq "python"}
Get-Process -Name "python" | Stop-Process -Force

# ポート使用プロセス特定
Get-NetTCPConnection -LocalPort 1234 | ForEach-Object {Get-Process -Id $_.OwningProcess}
```

### 開発環境ユーティリティ

#### Python 環境管理
```cmd
# Python バージョン・環境確認
python --version
python -c "import sys; print(sys.executable)"
python -c "import site; print(site.getsitepackages())"

# パッケージ管理
pip list                    # インストール済みパッケージ
pip show requests          # パッケージ詳細
pip check                  # 依存関係整合性チェック
pip freeze > requirements_current.txt
```

#### 一括処理スクリプト
```cmd
@echo off
rem setup_dev_env.bat - 開発環境セットアップ

echo 🔧 LLM×SLM 開発環境セットアップ
echo ================================

echo ✅ Python バージョン確認
python --version

echo ✅ 依存関係インストール
pip install -r requirements.txt

echo ✅ 必要ディレクトリ作成
mkdir data\instructions 2>nul
mkdir data\generated_code 2>nul
mkdir data\reviews 2>nul
mkdir logs 2>nul

echo ✅ 設定ファイル作成
if not exist config\config.json (
    copy config\config.example.json config\config.json
    echo ⚠️  config\config.json のAPIキー設定を忘れずに！
)

echo 🎉 セットアップ完了！
pause
```

### トラブルシューティングユーティリティ

#### 権限・アクセス問題
```cmd
# 管理者権限での実行確認
net session >nul 2>&1 && echo 管理者権限あり || echo 管理者権限なし

# ファイル・ディレクトリのアクセス権確認
icacls config\config.json
icacls data /T              # 再帰的チェック
```

#### ネットワーク診断
```cmd
# DNS 確認
nslookup api.anthropic.com
nslookup localhost

# ファイアウォール設定確認（PowerShell Admin）
netsh advfirewall firewall show rule name="Python*"
netsh advfirewall firewall show rule dir=in | findstr 1234
```
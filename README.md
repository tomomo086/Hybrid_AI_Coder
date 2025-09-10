# 🤖 Hybrid_AI_Coder - ハイブリッドAI開発システム

![Platform: Python | LM Studio](https://img.shields.io/badge/Platform-Python%20%7C%20LM%20Studio-green.svg)
![Language: Python](https://img.shields.io/badge/Language-Python-orange.svg)
![AI: Claude4 | ClaudeCode | LM Studio](https://img.shields.io/badge/AI-Claude4%20%7C%20ClaudeCode%20%7C%20LM%20Studio-blue.svg)
![Method: Hybrid AI Development](https://img.shields.io/badge/Method-Hybrid%20AI%20Development-red.svg)
![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-purple.svg)

> LLMのコンテキスト節約を重視したハイブリッドAI開発システム

## 🎯 概要・設計意図

**3つの機能だけの究極シンプル設計**：
1. 命令書を受け取る（人間から直接）
2. SLMにコードを生成させる（LM Studio経由）
3. 指定場所にファイル保存（任意パス）

### 💡 LLMコンテキスト節約の仕組み
- **従来**: LLMがコード生成 → 大量のコンテキスト消費
- **このシステム**: SLMがコード生成 → LLMはコンテキスト節約
- **効果**: LLMは設計・レビューに集中、SLMは実装に特化

### 🔄 SLM随時交換による品質制御
- **DeepSeek-Coder**: 軽量高速、シンプルなコード
- **Qwen2.5-Coder**: 高品質、複雑なロジック対応
- **CodeLlama**: バランス型、汎用性高い
- **即座切り替え**: LM Studio側でモデル変更するだけ

## 📹 実際の開発事例

このシステムを使って実際にゲームを開発した事例をご覧いただけます：

[![Hybrid AI Coderで作った横スクロールアクションゲーム](https://img.youtube.com/vi/jBFzPxjboac/maxresdefault.jpg)](https://youtu.be/jBFzPxjboac)

**🎮 横スクロールアクションゲーム開発事例**
- **開発時間**: 約2時間程度
- **使用したSLM**: Qwen2.5-Coder
- **特徴**: シンプルな要求から完全なPygameベースの横スクロールアクションを自動生成
- **成果**: キャラクター操作・敵・障害物のあるゲームが短時間で完成

> 📺 **動画で見る**: [Hybrid AI Coderで横スクロールアクション作成 - YouTube](https://youtu.be/jBFzPxjboac)

このように、LLMでの要件定義からSLMでの実装まで、効率的な開発フローを実現しています。

### 📊 実際のコンテキスト節約効果

ClaudeCodeによる分析で、実際に**75.6%のトークン削減**を達成しました：

<details>
<summary>📈 詳細な節約効果分析（クリックで展開）</summary>

![コンテキスト節約効果分析1](images/スクリーンショット%202025-09-10%20154629.png)

![コンテキスト節約効果分析2](images/スクリーンショット%202025-09-10%20155013.png)

**分析結果まとめ：**
- **従来方式**: 約23,350トークン（全てLLMが処理）
- **ハイブリッド方式**: 約5,700トークン（SLM協働）
- **節約量**: 17,650トークン（75.6%削減）

**効果が高かった理由：**
1. 詳細な指示書による効率的なSLM活用
2. 段階的実装による冗長性排除
3. 的確な修正による最小限の読み取り
4. 再利用パターンによる類似修正の効率化

</details>

**現実的な効果予測**: デバッグ・修正作業も含めて**約50-60%の削減効果**が期待できます。

## 🚀 開発フロー

```
人間のアイデア → LLMとの対話 → 要件定義書作成 → 具体的命令書作成 → SLM実行 → 完成コード
```

### 詳細なプロセス

**1. アイデア出し・初期対話**
- **人間**: 「○○のアプリを作りたい」と要求
- **LLM（ClaudeCode/GeminiCLI）**: アイデアの深掘り、課題整理、方向性提案

**2. LLMとの反復対話による要件定義**
- 納得いくまで反復対話でブラッシュアップ
- 機能要件、技術仕様、UI/UX、エラーハンドリング等を詳細化

**3. SLM向け具体的命令書の作成**
- 要件定義書をSLMが理解できる具体的な命令に変換
- **重要**: 1ファイルレベルの詳細指定（ファイル構造、関数名、変数名まで明記）

**4. SLMでのコード生成**
- LM Studio（SLM）に送信してコード生成
- 指定場所に保存

**5. LLMによる修正・最適化**
- 生成後の修正・デバッグ・レビューを担当

## ⚡ 使用方法

### 必要な環境

**1. AI支援開発環境（いずれか必須）**
- **[ClaudeCode](https://claude.ai/code)** - Anthropic公式CLI（推奨）
- **[GeminiCLI](https://ai.google.dev/)** - Google製コマンドライン

**2. LM Studio設定（必須）**
1. [LM Studio](https://lmstudio.ai/) をダウンロード・起動
2. 推奨モデル（いずれか）を読み込み：
   - **DeepSeek-Coder-6.7B** (軽量・高速)
   - **Qwen2.5-Coder-14B** (高品質・重い)
   - **CodeLlama** (バランス型)
3. ローカルAPIサーバー起動 (http://localhost:1234)

**3. Python環境**
```bash
pip install requests  # 必要なライブラリはこれだけ
```

### 実行方法
1. **ClaudeCode/GeminiCLI経由**：プロンプトで命令書と保存先を指定
2. **対話モード**：`ultra_simple.py`を直接実行

## 📁 ファイル構成（4ファイルのみ）

```
Hybrid_AI_Coder/
├── ultra_simple.py          # メインシステム（150行）
├── quick_execute.py         # ワンライナー実行（50行）
├── simple_config.json       # SLM接続設定
└── README.md               # このファイル
```

### 設定ファイル
`simple_config.json` が自動作成されます：

```json
{
  "slm_api": {
    "endpoint": "http://localhost:1234/v1/chat/completions"
  }
}
```

## 🎯 システムの特徴

### 💾 検証済みコンテキスト節約効果

**実証済み節約効果: 50-75%（実際のプロジェクトで検証）**

**大幅節約を実現した要因**：
- **詳細な指示書**: SLMが正確に実装（一発成功率向上）
- **段階的実装**: 冗長な読み取りを排除
- **効率的修正**: 問題箇所のみピンポイントで対処

**節約効果の内訳**：
- **初回コード生成**: SLMが担当（約15,000トークン節約）
- **実装中の思考プロセス**: 大幅短縮（約8,000-12,000トークン節約）
- **効率的修正**: 指示書ベースの効率的修正

**現実的予測**: デバッグ込みでも**50-60%の節約効果**を実現

**重要**: 数値的節約に加え、**LLMを思考・判断に専念させる構造**により開発品質も大幅向上

### 🧠 商用LLM vs SLMの特性理解に基づく最適化

#### 商用LLM（Claude4、GPT-4等）の得意分野
- **抽象的思考**: 要件の曖昧性を自動補完
- **文脈理解**: 長い会話履歴から意図を推測
- **創造的提案**: 新しいアイデアや代替案の提案
- **総合的判断**: 複数要素を考慮した最適解の提示

#### SLM（DeepSeek、Qwen等）の特性
- **具体的指示への高精度**: 明確な命令に対する正確な実行
- **計算コスト効率**: ローカル実行でコスト削減
- **一貫性**: 同じ指示に対する安定した出力
- **専門特化**: コード生成に特化した高い性能

### 🎯 SLM命令書作成のコツ
**商用LLMとSLMの特性差を理解した具体的指示が精度向上の鍵**

- **技術仕様の明示**: 
  - ❌ 「きれいなコードで」→ ⭕ 「PEP8準拠、関数は30行以内、docstring必須」
  - ❌ 「エラー処理して」→ ⭕ 「FileNotFoundError時は新規作成、ValueError時は再入力促す」
- **実装詳細の指定**:
  - 使用ライブラリのバージョン指定
  - 変数名・関数名の命名規則
  - ファイル構造とディレクトリ配置
  - 日本語コメントの具体的内容

### 🎯 最適な役割分担
- **人間**: 創造性・要件定義・最終判断
- **LLM（ClaudeCode/GeminiCLI）**: 仕様整理・品質管理・レビュー（**コンテキスト節約**）
- **SLM（LM Studio）**: 高速・正確なコード実装

### その他の特徴
- **完全日本語対応**: 日本語での要件定義・コメント生成
- **シンプル設計**: 4ファイル、200行程度で全体把握が容易
- **即座に開始**: 複雑なセットアップ不要

## 🚦 システム要件

- **Python 3.7+**
- **requests ライブラリ**
- **LM Studio + 任意のコーディングモデル**
- **ClaudeCode**（推奨） または GeminiCLI

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。  
商用・非商用問わず自由にご利用ください。

## 📋 開発情報

| **開発者** | tomomo086 + Claude4 |
| **開発期間** | 2025年9月7日 |
| **バージョン** | 1.0.0 |
| **開発ツール** | Claude4, ClaudeCode, LM Studio |

---

## 🔗 関連リンク

- [tomomo086:Github](https://github.com/tomomo086)
- [@mirai_sousiyo39:X](https://x.com/mirai_sousiyo39)

---

**作成者**: [tomomo086(@mirai_sousiyo39) + Claude4]   
**最終更新**: 2025年9月7日

---

**人間の創造性 × AIの実装力 = 効率的な開発スタイル** 🚀

*このREADMEもClaude4、ClaudeCode、LM StudioによるAI支援で作成されています 🤖💻*
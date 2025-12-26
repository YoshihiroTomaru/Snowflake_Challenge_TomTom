# Cortex Agent 直接呼び出しクライアント

このディレクトリには、Snowflake Cortex Agent APIをPAT（Personal Access Token）認証で直接呼び出すためのシンプルなPythonスクリプトが含まれています。

## 特徴

- **PAT認証**: シンプルで設定が簡単
- **ストリーミングレスポンス対応**: Server-Sent Events (SSE) 形式のストリーミング応答に対応
- **直接API呼び出し**: Cortex Agentへの直接REST APIアクセス

## セットアップ手順

### 1. 依存ライブラリのインストール

```bash
cd cortex_agent_call
pip install -r requirements.txt
```

### 2. Personal Access Token (PAT) の作成

SnowsightのUIで簡単にPATを作成できます：

#### Snowsight UIでの作成手順

1. [Snowsight](https://app.snowflake.com/) にサインインします
2. ナビゲーションメニューで **Admin** » **Users & Roles** を選択します
3. PATを作成したいユーザー（自分自身）を選択します
4. **Programmatic access tokens** セクションで、**Generate new token** を選択します
5. **New programmatic access token** ダイアログで以下を入力：
   - **Name**: トークンの名前（例: `my_cortex_agent_token`）
   - **Comment**: トークンの説明（例: `Cortex Agent API access`）
   - **Expires in**: 有効期限（例: 90日）
   - **Role**: **Any of my roles** を選択（または特定のロールに制限）
6. **Generate** を選択します
7. **生成されたトークンをコピー**してください

**重要**: このダイアログを閉じた後は、トークンをコピーできません！必ず安全な場所に保存してください。

#### SQL コマンドでの作成（代替方法）

Snowflakeワークシートで以下のSQLを実行してPATを作成することもできます：

```sql
-- 現在のユーザーのPATを作成（90日有効）
ALTER USER CURRENT_USER() 
  ADD PROGRAMMATIC ACCESS TOKEN my_token
  EXPIRES_IN_DAYS = 90;

-- トークンの情報を確認
SHOW USER PROGRAMMATIC ACCESS TOKENS;
```

**注意**: SQL コマンドでは、トークンのシークレット（実際の文字列）は表示されません。トークンのシークレットを取得するには、Snowsight UIを使用してください。

### 3. `.env` ファイルの作成

`.env.example` をコピーして `.env` を作成し、以下の値を設定します：

```bash
cp .env.example .env
```

`.env` の内容：

```env
# Snowflake接続情報
SNOWFLAKE_ACCOUNT=YOUR_ACCOUNT_IDENTIFIER
SNOWFLAKE_DATABASE=YOUR_DATABASE
SNOWFLAKE_SCHEMA=YOUR_SCHEMA

# Cortex Agent名
AGENT_NAME=YOUR_AGENT_NAME

# Personal Access Token
SNOWFLAKE_PAT=YOUR_PAT_TOKEN_HERE
```

**設定例**：
```env
SNOWFLAKE_ACCOUNT=SJERDKE-TEST_TOMARU
SNOWFLAKE_DATABASE=MELIPS_HANDS_ON
SNOWFLAKE_SCHEMA=STAGING
AGENT_NAME=MELIPS_AGENT_SUB
SNOWFLAKE_PAT=ver:1-hint:123456789-ETMsD...（長い文字列）
```

## 実行方法

```bash
python agent_client.py
```

スクリプトを実行すると、質問を入力するよう求められます。終了するには `exit` と入力してください。

## 実行例

```
質問を入力してください (終了するにはexitと入力): 平均気温が高いトップ3部屋は？

デバッグ情報:
  元のアカウント: SJERDKE-TEST_TOMARU
  URL用アカウント: sjerdke-test-tomaru
  エージェント名: MELIPS_HANDS_ON.STAGING.MELIPS_AGENT_SUB

ストリーミングレスポンスを受信中...

{"delta":{"content":[{"type":"text","text":"Based on the"}]}}
{"delta":{"content":[{"type":"text","text":" data, the top 3 rooms"}]}}
...
```

## ファイル構成

- `agent_client.py`: メインスクリプト（PAT認証でCortex Agent APIを呼び出し）
- `requirements.txt`: 必要なPythonパッケージ
- `.env`: 環境変数設定ファイル（Git管理外）
- `.env.example`: 環境変数設定テンプレート
- `README.md`: このドキュメント

## PAT認証 vs キーペア認証 vs OAuth認証

| 認証方式 | メリット | デメリット | 用途 |
|---------|---------|-----------|------|
| **PAT** | 設定が簡単、すぐに始められる | トークンの有効期限管理が必要 | 開発・テスト |
| **キーペア** | 長期利用に適している、自動化しやすい | 初期設定が複雑 | 本番環境、自動化 |
| **OAuth** | SSOと連携可能、セキュアなブラウザ認証 | 統合設定が必要 | エンドユーザー向けアプリ |

## 注意事項

- **PATは機密情報です**: `.env` ファイルをGitにコミットしないでください
- **有効期限**: PATには有効期限があります（デフォルト90日）
- **権限**: PATは作成したユーザーの権限を継承します
- **セキュリティ**: 本番環境では、より安全なキーペア認証またはOAuth認証の使用を推奨します

## トラブルシューティング

### 401 Unauthorized エラー

- PATの有効期限が切れている可能性があります
- PATの値が正しくコピーされているか確認してください
- SnowflakeでPATを再作成してみてください

### 404 Not Found エラー

- エージェント名が正しいか確認してください
- データベース・スキーマ名が正しいか確認してください
- エージェントへのアクセス権限があるか確認してください

### ストリーミング応答が表示されない

- `agent_client.py` が `stream=True` でリクエストしていることを確認してください
- `iter_lines()` を使用してServer-Sent Eventsを処理していることを確認してください

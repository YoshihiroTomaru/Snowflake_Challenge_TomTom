# Snowflake MCP Server Setup Guide

このディレクトリには、Snowflake Managed MCP ServerをCortex Analystと連携させるために必要な設定ファイルが含まれています。

## 📁 ファイル構成

- `create_mcp_server.sql` - Snowflake側でMCPサーバーを作成するSQLスクリプト
- `environmental_model.yml` - Cortex Analystのセマンティックモデル定義
- `mcp.json.example` - VS CodeのMCP設定ファイルのサンプル

## 🔧 セットアップ手順

### 1. Snowflake側の設定

#### 1.1 セマンティックモデルのアップロード

1. Snowsight左メニューから **AI & ML** → **Analyst** を選択
2. 右上の **+ Create** ボタンをクリック
3. **Upload from YAML file** を選択
4. `environmental_model.yml` ファイルを選択してアップロード
5. アップロード設定で以下を選択：
   - **Database**: `MELIPS_HANDS_ON`（または対象のデータベース）
   - **Schema**: `STAGING`（または対象のスキーマ）
   - **Stage**: 適切なステージを選択
6. **Create** をクリック
7. **Semantic Models** タブに `environmental_analysis_model` が作成されていることを確認

#### 1.2 セマンティックビューの作成

セマンティックモデルをMCPサーバーで使用するには、セマンティックビューへの変換が必要です。

1. Snowsight左メニューから **AI & ML** → **Analyst** を選択
2. Cortex分析画面が開いたら、**Semantic Models** タブをクリック
3. `environmental_analysis_model` を見つけ、右側の三点リーダ（**...**）をクリック
4. **Convert to Semantic View**（セマンティックビューに変換）を選択
5. **Semantic Views** タブに切り替えて、対応するビューが作成されていることを確認

#### 1.3 MCPサーバーの作成

1. Snowsightで新しいワークシートを開く
2. `create_mcp_server.sql` の内容をコピー＆ペースト
3. 必要に応じて以下を調整：
   ```sql
   USE ROLE DATA_ENGINEER;           -- 使用するロール
   USE WAREHOUSE DATA_ENGINEER_WH;   -- 使用するウェアハウス
   USE DATABASE MELIPS_HANDS_ON;     -- 対象データベース
   USE SCHEMA STAGING;               -- 対象スキーマ
   ```
4. SQLを実行してMCPサーバー `ANALYST_MCP_SERVER` を作成

#### 1.4 Personal Access Token (PAT) の生成

1. Snowsight右上のユーザーメニューをクリック
2. **Account** → **Personal Access Tokens**
3. **+ Token** をクリック
4. トークン名を入力（例: `vscode-mcp-token`）
5. 生成されたトークンをコピー（**このトークンは二度と表示されません**）

### 2. VS Code側の設定

#### 2.1 MCP設定ファイルの作成

1. プロジェクトルートに `.vscode` ディレクトリが存在することを確認
2. `mcp.json.example` を `.vscode/mcp.json` にコピー
   ```powershell
   cp mcp_server_setup/mcp.json.example .vscode/mcp.json
   ```

3. `.vscode/mcp.json` を編集して以下のプレースホルダーを実際の値に置き換え：
   - `<YOUR_ACCOUNT>`: Snowflakeアカウント識別子（例: `sjerdke-test-tomaru`）
   - `<DATABASE>`: データベース名（例: `melips_hands_on`）
   - `<SCHEMA>`: スキーマ名（例: `staging`）
   - `<MCP_SERVER_NAME>`: MCPサーバー名（例: `analyst_mcp_server`）
   - `<YOUR_PERSONAL_ACCESS_TOKEN>`: 生成したPAT

#### 2.2 VS Codeの再起動

設定ファイルを更新したら、VS Codeを再起動してMCP接続を有効化します。

## 🧪 動作確認

VS Codeで以下のようなプロンプトを送信してCortex Analystが応答することを確認：

```
平均気温が一番高い部屋はどこですか？
```

```
CO2濃度が高いトップ5の部屋を教えてください
```

## 🔒 セキュリティ注意事項

⚠️ **重要**: Personal Access Tokenは機密情報です

- `.vscode/mcp.json` は `.gitignore` に含まれており、Gitにコミットされません
- トークンを他の人と共有しないでください
- トークンが漏洩した場合は、すぐにSnowsightで無効化してください

## 📝 トラブルシューティング

### MCPサーバーに接続できない

1. Snowflake側でMCPサーバーが正常に作成されているか確認
   ```sql
   SHOW MCP SERVERS IN SCHEMA STAGING;
   ```

2. PATが有効か確認（期限切れでないか）

3. `.vscode/mcp.json` のURL形式が正しいか確認
   - URL内のデータベース名・スキーマ名は**小文字**
   - アカウント識別子のアンダースコアは**ハイフン**に変換

### Cortex Analystがクエリに応答しない

1. セマンティックモデルが正しくアップロードされているか確認
2. テーブルへのアクセス権限があるか確認
3. ウェアハウスが起動しているか確認

## 📚 参考リンク

- [Snowflake MCP Documentation](https://docs.snowflake.com/en/developer-guide/model-context-protocol/overview)
- [Cortex Analyst Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)

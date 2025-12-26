# Snowflake API連携プロジェクト

このリポジトリは、Snowflakeとの連携に関する3つの主要なコンポーネントを含んでいます。

## 1. Pythonクライアント (`/python_client`)

`python_client`ディレクトリには、Pythonアプリケーションから直接Snowflake Cortex Analyst APIを呼び出すためのクライアントライブラリとサンプルスクリプトが含まれています。

**認証方式**：
- **キーペア認証（JWT）**: プログラムからの自動実行や、既存のアプリケーションへの組み込みに適しています
- **ブラウザOAuth認証**: Entra ID（Azure AD）などのSSOと連携したブラウザベース認証をサポート

詳細なセットアップ方法や使用法については、[`python_client/README.md`](./python_client/README.md) を参照してください。

## 2. Cortex Agent直接呼び出し (`/cortex_agent_call`)

`cortex_agent_call`ディレクトリには、Snowflake Cortex Agent APIをPAT（Personal Access Token）認証で直接呼び出すためのシンプルなスクリプトが含まれています。

**特徴**：
- PAT認証による簡単なセットアップ
- ストリーミングレスポンス対応
- Cortex Agent（MELIPS_AGENT_SUB）への直接クエリ実行

詳細については、[`cortex_agent_call/`](./cortex_agent_call/) ディレクトリを参照してください。

## 3. Snowflake Managed MCP Server連携 (`/mcp_server_setup`)

`mcp_server_setup`ディレクトリには、VS CodeでSnowflake Managed MCP ServerとGitHub CopilotのCortex Analystを連携させるための設定ファイルとドキュメントが含まれています。

MCPサーバーを使用することで、GitHub Copilot経由でSnowflakeのデータに自然言語でクエリを実行できます。

詳細な設定手順については、[`mcp_server_setup/README.md`](./mcp_server_setup/README.md) を参照してください。

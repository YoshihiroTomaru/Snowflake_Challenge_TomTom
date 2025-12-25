# Snowflake API連携プロジェクト

このリポジトリは、Snowflakeとの連携に関する2つの主要なコンポーネントを含んでいます。

## 1. Pythonクライアント (`/python_client`)

`python_client`ディレクトリには、Pythonアプリケーションから直接Snowflake Cortex Analyst APIを呼び出すためのクライアントライブラリとサンプルスクリプトが含まれています。

キーペア認証を使用し、プログラムからの自動実行や、既存のアプリケーションへの組み込みに適しています。

詳細なセットアップ方法や使用法については、[`python_client/README.md`](./python_client/README.md) を参照してください。

## 2. Snowflake Managed MCP Server連携 (`/mcp_server_setup`)

`mcp_server_setup`ディレクトリには、VS CodeでSnowflake Managed MCP ServerとGitHub CopilotのCortex Analystを連携させるための設定ファイルとドキュメントが含まれています。

MCPサーバーを使用することで、GitHub Copilot経由でSnowflakeのデータに自然言語でクエリを実行できます。

詳細な設定手順については、[`mcp_server_setup/README.md`](./mcp_server_setup/README.md) を参照してください。

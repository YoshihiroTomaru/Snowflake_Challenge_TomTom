# Snowflake API連携プロジェクト

このリポジトリは、Snowflakeとの連携に関する2つの主要なコンポーネントを含んでいます。

## 1. Pythonクライアント (`/python_client`)

`python_client`ディレクトリには、Pythonアプリケーションから直接Snowflake Cortex Analyst APIを呼び出すためのクライアントライブラリとサンプルスクリプトが含まれています。

キーペア認証を使用し、プログラムからの自動実行や、既存のアプリケーションへの組み込みに適しています。

詳細なセットアップ方法や使用法については、[`python_client/README.md`](./python_client/README.md) を参照してください。

## 2. AIエージェント連携 (MCPサーバー) (`/mcp_server_setup`)

`mcp_server_setup`ディレクトリには、ClineのようなAIエージェントがSnowflakeの機能を「ツール」として利用できるようにするための設定ファイルやドキュメントが含まれています。

こちらはSnowflakeが管理するマネージドMCPサーバーを利用し、AIエージェントとの対話的なデータ分析を実現します。

詳細な設定手順については、[`mcp_server_setup/README.md`](./mcp_server_setup/README.md) を参照してください（現在作成中です）。

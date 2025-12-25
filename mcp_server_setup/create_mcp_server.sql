-- =============================================================================
-- Snowflake Managed MCP Server for Cortex Analyst (Semantic View)
-- =============================================================================
-- このSQLは、指定されたセマンティックビューを公開するマネージドMCPサーバーを作成します。
-- このサーバーへの認証は、別途生成するPAT (Personal Access Token) を使用します。
--
-- 実行方法:
-- 1. Snowsightのワークシートにこのクエリを貼り付けます。
-- 2. 以下の `USE ROLE` を、このオブジェクトを所有させたいロールに設定します。
-- 3. このクエリ全体を実行します。
-- 4. SnowsightのUIから、このMCPサーバーにアクセスするユーザー用のPATを生成します。
-- =============================================================================

-- 1. ロール、データベース、スキーマの指定
USE ROLE DATA_ENGINEER;
USE WAREHOUSE DATA_ENGINEER_WH;
USE DATABASE MELIPS_HANDS_ON;
USE SCHEMA STAGING; -- MCPサーバーオブジェクトを作成するスキーマ

-- 2. MCPサーバーの作成
CREATE OR REPLACE MCP SERVER ANALYST_MCP_SERVER
FROM SPECIFICATION $$
tools:
  - name: "environmental_analyst"
    type: "CORTEX_ANALYST_MESSAGE"
    title: "Analyst for Indoor Environmental Data"
    description: "Ask questions in natural language about indoor environmental data like temperature, humidity, and CO2 levels."
    identifier: "MELIPS_HANDS_ON.STAGING.environmental_analysis_model"
  - name: "SQL_Execution_Tool"
    type: "SYSTEM_EXECUTE_SQL"
    description: "A tool to execute SQL queries against the connected Snowflake database."
    title: "SQL Execution Tool"
$$;

# Snowflake Cortex Analyst API クライアント

このスクリプトは、キーペア認証を使用してSnowflake Cortex Analyst REST APIに接続し、指定されたセマンティックビューに対して質問を送信することができます。

## セットアップ手順

### 1. リポジトリをクローン

まず、このリポジトリをローカルマシンにクローンします。

```bash
git clone https://github.com/YoshihiroTomaru/Snowflake_Challenge_TomTom.git
cd Snowflake_Challenge_TomTom
```

### 2. 仮想環境の作成（推奨）

依存関係を管理するために、仮想環境の使用を推奨します。

```bash
# 仮想環境を作成
python -m venv .venv

# 仮想環境を有効化
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3. 依存ライブラリのインストール

`requirements.txt` ファイルを使用して、必要なPythonライブラリをインストールします。

```bash
pip install -r requirements.txt
```

### 4. `.env` ファイルの作成

このプロジェクトでは、秘匿情報を管理するために `.env` ファイルを使用します。まず、`example.env` ファイルをコピーして `.env` という名前のファイルを作成します。

```bash
cp example.env .env
```

次に、作成した `.env` ファイルを開き、プレースホルダー (`YOUR_...`) をご自身のSnowflakeアカウント情報や秘密鍵の情報に置き換えてください。

**`.env` ファイルはGitにコミットしないでください。** `.gitignore` に `.env` が含まれていることを確認してください。

### 5. 秘密鍵の配置

ご自身の秘密鍵ファイル（例: `rsa_key.p8`）を、`.env` ファイル内の `PRIVATE_KEY_FILE` で指定したパスに配置してください。

## 実行方法

セットアップが完了したら、以下のコマンドでスクリプトを実行できます。

```bash
python snowflake_agent_client.py
```

スクリプトを実行すると、セマンティックビューへの質問を入力するよう求められます。終了するには `exit` と入力してください。

## 実行結果の例

スクリプトを実行し、「どんなデータが見れますか？」と質問した場合のAPIレスポンスの例です。

```json
{
  "message": {
    "role": "analyst",
    "content": [
      {
        "type": "text",
        "text": "This semantic data model contains environmental monitoring data including temperature, humidity, and carbon dioxide measurements collected over time from different locations. It also includes information about room characteristics such as area categories and sizes. You can analyze environmental trends, compare conditions across different locations and room types, and track changes in environmental metrics over time."
      },
      {
        "type": "suggestions",
        "suggestions": [
          "What is the average CO2 emissions level across all locations last month?",
          "What are the temperature readings for each area category?",
          "What is the total humidity percentage recorded year to date?"
        ]
      }
    ]
  },
  "request_id": "15ee04aa-58d2-4aa4-a6b6-3551c5f18760",
  "warnings": [],
  "semantic_model_selection": null,
  "response_metadata": {
    "model_names": [
      "claude-4-sonnet"
    ],
    "is_semantic_sql": false,
    "cortex_search_retrieval": [],
    "question_category": "ONBOARDING",
    "analyst_orchestration_path": "regular_sqlgen",
    "analyst_latency_ms": 4561.0
  }
}
```

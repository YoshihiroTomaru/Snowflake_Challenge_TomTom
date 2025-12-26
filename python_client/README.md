# Snowflake Cortex Analyst API クライアント

このスクリプトは、**キーペア認証**または**ブラウザOAuth認証**を使用してSnowflake Cortex Analyst REST APIに接続し、指定されたセマンティックモデルまたはセマンティックビューに対して質問を送信することができます。

## 認証方式

2つの認証方式をサポートしています：

1. **キーペア認証（JWT）** - 秘密鍵と公開鍵を使用（デフォルト、推奨）
2. **ブラウザOAuth認証** - ブラウザでSSOログインを使用（実験的機能）

## セマンティックモデルとセマンティックビューについて

Cortex Analystで分析を行うには、**セマンティックモデル**または**セマンティックビュー**のどちらかをクエリ対象として指定します。

-   **セマンティックビュー**: 単一のテーブルやビューに対するシンプルな分析に適しています。
-   **セマンティックモデル**: 複数のテーブル間の関係性を定義することで、より高度な分析を可能にします。**複数のテーブルにまたがるような複雑な質問に答えるには、セマンティックモデルの使用が必須です。**

このクライアントは、`.env` ファイルの設定を切り替えることで、両方の方法に対応しています。

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

### 4. キーペアの作成とSnowflakeへの登録

このクライアントはSnowflakeへの接続にキーペア認証を使用します。以下の手順で秘密鍵と公開鍵のペアを作成し、公開鍵をSnowflakeユーザーに登録してください。

**a. 秘密鍵と公開鍵を生成する**

PowerShell（Windows）やターミナル（macOS/Linux）などで以下の `openssl` コマンドを実行して、暗号化された秘密鍵（`rsa_key.p8`）と公開鍵（`rsa_key.pub`）を生成します。

```bash
# 暗号化された秘密鍵を生成（推奨）
openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 des3 -inform PEM -out rsa_key.p8

# 秘密鍵から公開鍵を生成
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

最初のコマンド実行時に、秘密鍵を保護するためのパスフレーズの入力を求められます。このパスフレーズは後で `.env` ファイルに設定するので、忘れないようにしてください。

**b. 公開鍵をSnowflakeに登録する**

まず、生成された公開鍵ファイル (`rsa_key.pub`) の内容から、ヘッダー (`-----BEGIN PUBLIC KEY-----`) とフッター (`-----END PUBLIC KEY-----`) **および、その間の改行コードをすべて取り除き**、1行の文字列にしたものをコピーします。

以下のコマンドを実行すると、整形済みのキーがターミナルに出力されるので便利です。

```bash
cat rsa_key.pub | grep -v -- '-----' | tr -d '\n'
```

次に、ブラウザでSnowflakeにログインし、ワークシートを開いて以下のSQLコマンドを実行して、コピーした公開鍵の文字列を対象のユーザーに登録します。

```sql
ALTER USER YOUR_SNOWFLAKE_USER SET RSA_PUBLIC_KEY='ここにコピーした1行の公開鍵文字列を貼り付け';
```

`YOUR_SNOWFLAKE_USER` には、Snowflake UIの左下に表示されるご自身のユーザー名（例: `MITSUBISHI_TARO`）を指定してください。

### 5. `.env` ファイルの作成

このプロジェクトでは、秘匿情報を管理するために `.env` ファイルを使用します。まず、`example.env` ファイルをコピーして `.env` という名前のファイルを作成します。

```bash
cp example.env .env
```

次に、作成した `.env` ファイルを開き、ご自身の環境に合わせて設定値を入力してください。

`.env` ファイルでは、クエリ対象として**セマンティックモデル**か**セマンティックビュー**のどちらか一方を選択します。`example.env` を参考に、使用しない方をコメントアウトしてください。

`SNOWFLAKE_USER` には、Snowflakeへのログインに使用するユーザー名を設定します。SSOを利用している場合は、SSOのログイン名となります。これは、`ALTER USER` コマンドで指定したユーザー名と異なる場合があります。

**`.env` ファイルはGitにコミットしないでください。** `.gitignore` に `.env` が含まれていることを確認してください。

### 6. 秘密鍵の配置

生成したご自身の秘密鍵ファイル（例: `rsa_key.p8`）を、`.env` ファイル内の `PRIVATE_KEY_FILE` で指定したパスに配置してください。

## 実行方法

セットアップが完了したら、以下のコマンドでスクリプトを実行できます。

```bash
python snowflake_agent_client.py
```

スクリプトを実行すると、質問を入力するよう求められます。終了するには `exit` と入力してください。

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

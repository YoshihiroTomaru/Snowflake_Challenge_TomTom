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

このプロジェクトでは、秘匿情報を管理するために `.env` ファイルを使用します。プロジェクトのルートディレクトリに `.env` という名前のファイルを作成し、以下の内容を記述してください。**このファイルはGitにコミットしないでください。**

```env
SNOWFLAKE_ACCOUNT="YOUR_SNOWFLAKE_ACCOUNT"
SNOWFLAKE_USER="YOUR_SNOWFLAKE_USER"
PRIVATE_KEY_FILE="./path/to/your/rsa_key.p8"
PRIVATE_KEY_PASSPHRASE="YOUR_PASSPHRASE"
SEMANTIC_VIEW_NAME="YOUR_SEMANTIC_VIEW_NAME"
SNOWFLAKE_DATABASE="YOUR_DATABASE"
SNOWFLAKE_SCHEMA="YOUR_SCHEMA"
```

上記のプレースホルダー (`YOUR_...`) を、ご自身のSnowflakeアカウント情報や秘密鍵の情報に置き換えてください。

### 5. 秘密鍵の配置

ご自身の秘密鍵ファイル（例: `rsa_key.p8`）を、`.env` ファイル内の `PRIVATE_KEY_FILE` で指定したパスに配置してください。

## 実行方法

セットアップが完了したら、以下のコマンドでスクリプトを実行できます。

```bash
python snowflake_agent_client.py
```

スクリプトを実行すると、セマンティックビューへの質問を入力するよう求められます。終了するには `exit` と入力してください。

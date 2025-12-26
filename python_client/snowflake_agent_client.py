import os

import requests
from dotenv import load_dotenv

from snowflake_api_client.auth import (generate_jwt,
                                       get_private_key_and_fingerprint)
from snowflake_api_client.oauth import get_oauth_token_browser
from snowflake_api_client.cortex import call_analyst_api

# .envファイルから環境変数を読み込む
load_dotenv()

# --- 環境変数から設定を読み込む ---
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
AUTH_METHOD = os.getenv('AUTH_METHOD', 'keypair')  # デフォルトはキーペア認証
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
PRIVATE_KEY_FILE = os.getenv('PRIVATE_KEY_FILE')
PRIVATE_KEY_PASSPHRASE = os.getenv('PRIVATE_KEY_PASSPHRASE')
OAUTH_REDIRECT_PORT = int(os.getenv('OAUTH_REDIRECT_PORT', '8080'))
OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')

# --- クエリ対象を読み込む ---
SEMANTIC_MODEL_STAGE = os.getenv('SEMANTIC_MODEL_STAGE')
SEMANTIC_MODEL_FILENAME = os.getenv('SEMANTIC_MODEL_FILENAME')
SEMANTIC_VIEW_NAME = os.getenv('SEMANTIC_VIEW_NAME')


def main():
    """
    認証トークンを生成し、ユーザーの質問をCortex Analyst REST APIに送信します。
    """
    try:
        # --- 設定の検証 ---
        if not all([SNOWFLAKE_ACCOUNT, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA]):
            print("エラー: 基本的な環境変数が.envファイルに設定されていません。")
            return

        model_path = None
        if SEMANTIC_MODEL_STAGE and SEMANTIC_MODEL_FILENAME:
            model_path = f"@{SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{SEMANTIC_MODEL_STAGE}/{SEMANTIC_MODEL_FILENAME}"

        if not (model_path or SEMANTIC_VIEW_NAME):
            print("エラー: .envファイルで、セマンティックモデル(STAGE/FILENAME) または セマンティックビュー(VIEW_NAME)のどちらかを設定してください。")
            return

        # --- 認証フェーズ ---
        jwt_token = None
        token_type = 'KEYPAIR_JWT'  # デフォルト
        
        if AUTH_METHOD == 'browser_oauth':
            print("=== ブラウザOAuth認証を使用します ===")
            if not OAUTH_CLIENT_ID:
                print("エラー: OAUTH_CLIENT_IDが.envファイルに設定されていません。")
                return
                
            access_token = get_oauth_token_browser(SNOWFLAKE_ACCOUNT, OAUTH_CLIENT_ID, OAUTH_REDIRECT_PORT)
            
            if access_token:
                print("\n✓ OAuth認証に成功しました。")
                # OAuthアクセストークンをJWTトークンとして使用
                jwt_token = access_token
                token_type = 'OAUTH'
            else:
                print("OAuth認証に失敗しました。")
                return
                
        else:  # keypair認証
            print("=== キーペア認証を使用します ===")
            if not all([SNOWFLAKE_USER, PRIVATE_KEY_FILE]):
                print("エラー: キーペア認証に必要な環境変数が設定されていません。")
                return
            print("認証トークンを生成しています...")
            private_key, public_key_fp = get_private_key_and_fingerprint(PRIVATE_KEY_FILE, PRIVATE_KEY_PASSPHRASE)
            jwt_token = generate_jwt(private_key, public_key_fp, SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER)
        
        print("認証トークンの生成に成功しました。")

        # --- 質問フェーズ ---
        target_name = model_path if model_path else SEMANTIC_VIEW_NAME
        print(f"'{target_name}' を使用して問い合わせます。")

        while True:
            question = input("\n質問を入力してください (終了するにはexitと入力): ")
            if question.lower() == 'exit':
                break

            result = call_analyst_api(
                jwt_token=jwt_token,
                snowflake_account=SNOWFLAKE_ACCOUNT,
                database=SNOWFLAKE_DATABASE,
                schema=SNOWFLAKE_SCHEMA,
                question=question,
                semantic_model_file_path=model_path,
                semantic_view=SEMANTIC_VIEW_NAME,
                token_type=token_type
            )

            print("\n--- APIからの回答 ---")
            if 'messages' in result and result['messages']:
                last_message = result['messages'][-1]
                if 'content' in last_message and last_message['content']:
                    print(last_message['content'][0].get('text', '回答テキストが見つかりません。'))
                else:
                    print(result)
            else:
                print(result)
            print("---------------------\n")

    except FileNotFoundError:
        print(f"エラー: 秘密鍵ファイル '{PRIVATE_KEY_FILE}' が見つかりません。パスが正しいか確認してください。")
    except requests.exceptions.HTTPError as e:
        print(f"APIリクエストエラー: {e.response.status_code}")
        print(f"レスポンス: {e.response.text}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    main()

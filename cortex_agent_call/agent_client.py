import os

import requests
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# --- 環境変数から設定を読み込む ---
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_PAT = os.getenv('SNOWFLAKE_PAT')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')
AGENT_NAME = os.getenv('AGENT_NAME')


def call_cortex_agent(pat_token, snowflake_account, database, schema, agent_name, question):
    """
    Cortex Agent APIを呼び出してエージェントに質問する
    """
    # アカウント識別子を整形
    # アンダースコアをハイフンに変換し、小文字に統一
    # 例: "SJERDKE-TEST_TOMARU" -> "sjerdke-test-tomaru"
    url_account_identifier = snowflake_account.replace('_', '-').lower()
    
    # エージェントのフルネーム
    full_agent_name = f"{database}.{schema}.{agent_name}"
    
    # Cortex Agent APIのエンドポイント (:runが必要)
    url = f"https://{url_account_identifier}.snowflakecomputing.com/api/v2/databases/{database}/schemas/{schema}/agents/{agent_name}:run"
    
    print(f"\nデバッグ情報:")
    print(f"  元のアカウント: {snowflake_account}")
    print(f"  URL用アカウント: {url_account_identifier}")
    print(f"  エージェント名: {full_agent_name}")
    
    headers = {
        'Authorization': f'Bearer {pat_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # リクエストボディ（ドキュメントに基づく）
    # 最初のリクエストではthread_idを指定しない
    data = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    }
    
    print(f"\nエージェント '{full_agent_name}' に問い合わせています...")
    print(f"質問: {question}")
    print(f"URL: {url}")
    
    response = requests.post(url, headers=headers, json=data, stream=True)
    
    print(f"ステータスコード: {response.status_code}")
    if response.status_code != 200:
        print(f"レスポンス内容: {response.text}")
    
    response.raise_for_status()
    
    # ストリーミングレスポンスを処理
    print("\n--- エージェントからのストリーミング応答 ---")
    final_response = []
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            # Server-Sent Events形式の処理
            if line_str.startswith('data: '):
                data_str = line_str[6:]  # "data: "を除去
                if data_str.strip():
                    print(data_str)
                    final_response.append(data_str)
            elif line_str.startswith('event: '):
                event_type = line_str[7:]  # "event: "を除去
                print(f"[{event_type}]", end=" ")
    
    print("\n---------------------")
    return {"streaming_response": final_response}


def main():
    """
    PAT認証を使用してCortex Agentに質問を送信します。
    """
    try:
        # --- 設定の検証 ---
        if not all([SNOWFLAKE_ACCOUNT, SNOWFLAKE_PAT, 
                    SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, AGENT_NAME]):
            print("エラー: 必要な環境変数が.envファイルに設定されていません。")
            return

        print("PAT認証を使用してエージェントに接続します...")

        # --- 質問フェーズ ---
        question = "平均湿度の高いトップ5を教えて"
        
        result = call_cortex_agent(
            pat_token=SNOWFLAKE_PAT,
            snowflake_account=SNOWFLAKE_ACCOUNT,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            agent_name=AGENT_NAME,
            question=question
        )

        # 結果は既にストリーミング処理で表示されているので、ここでは何もしない

    except FileNotFoundError as e:
        print(f"エラー: 秘密鍵ファイルが見つかりません: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"APIリクエストエラー: {e.response.status_code}")
        print(f"レスポンス: {e.response.text}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

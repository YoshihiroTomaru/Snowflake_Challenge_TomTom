import requests


def call_analyst_api(jwt_token, snowflake_account, database, schema, semantic_view, question):
    """
    JWTトークンと質問を使ってCortex Analyst APIを呼び出す。
    """
    url_account_identifier = snowflake_account.split('.')[0].replace('_', '-').lower()
    url = f"https://{url_account_identifier}.snowflakecomputing.com/api/v2/cortex/analyst/message"

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
        'X-Snowflake-Authorization-Token-Type': 'KEYPAIR_JWT'
    }

    full_semantic_view = f"{database}.{schema}.{semantic_view}"

    data = {
        "semantic_view": full_semantic_view,
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

    print(f"\n'{full_semantic_view}' に問い合わせています...")
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()

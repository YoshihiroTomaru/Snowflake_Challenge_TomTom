import requests


def call_analyst_api(jwt_token, snowflake_account, database, schema, question, semantic_model_file_path=None, semantic_view=None, token_type='KEYPAIR_JWT'):
    """
    JWTトークンと質問を使ってCortex Analyst APIを呼び出す。
    セマンティックモデルまたはセマンティックビューのどちらかを指定する。
    
    Args:
        token_type: 'KEYPAIR_JWT' または 'OAUTH'
    """
    url_account_identifier = snowflake_account.split('.')[0].replace('_', '-').lower()
    url = f"https://{url_account_identifier}.snowflakecomputing.com/api/v2/cortex/analyst/message"

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
        'X-Snowflake-Authorization-Token-Type': token_type
    }

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

    target = ""
    if semantic_model_file_path:
        data["semantic_model_file"] = semantic_model_file_path
        target = semantic_model_file_path
    elif semantic_view:
        full_semantic_view = f"{database}.{schema}.{semantic_view}"
        data["semantic_view"] = full_semantic_view
        target = full_semantic_view
    else:
        raise ValueError("Either semantic_model_file_path or semantic_view must be provided.")

    print(f"\n'{target}' に問い合わせています...")
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()

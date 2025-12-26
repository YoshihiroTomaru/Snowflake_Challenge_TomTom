import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import hashlib
import base64
import secrets
import requests
import os


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """OAuth認証コールバックを処理するHTTPハンドラー"""
    
    auth_code = None
    
    def do_GET(self):
        """GETリクエストを処理"""
        # クエリパラメータからcodeを取得
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        if 'code' in params:
            OAuthCallbackHandler.auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = """
                <html>
                <head><title>Authentication Successful</title></head>
                <body>
                    <h1>認証に成功しました！</h1>
                    <p>このウィンドウを閉じて、アプリケーションに戻ってください。</p>
                </body>
                </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = """
                <html>
                <head><title>Authentication Failed</title></head>
                <body>
                    <h1>認証に失敗しました</h1>
                    <p>エラーが発生しました。</p>
                </body>
                </html>
            """
            self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """ログメッセージを抑制"""
        pass


def generate_pkce_pair():
    """PKCE用のcode_verifierとcode_challengeを生成"""
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    return code_verifier, code_challenge


def get_oauth_token_browser(snowflake_account, client_id, redirect_port=8080):
    """
    ブラウザを使用してOAuth認証を行い、アクセストークンを取得します（PKCE対応）。
    
    Args:
        snowflake_account: Snowflakeアカウント識別子
        client_id: OAuth統合のクライアントID
        redirect_port: リダイレクトURIのポート番号
    
    Returns:
        アクセストークン（文字列）
    """
    redirect_uri = f"http://localhost:{redirect_port}/callback"
    
    # Snowflake OAuth認証URL
    account_url = snowflake_account.replace('_', '-').lower()
    
    # PKCE pair生成
    code_verifier, code_challenge = generate_pkce_pair()
    
    # OAuthパラメータ（PKCE対応）
    # Custom OAuth統合の場合、scopeは不要
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': secrets.token_hex(16),
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    
    auth_url = f"https://{account_url}.snowflakecomputing.com/oauth/authorize?" + urllib.parse.urlencode(auth_params)
    
    print(f"\n=== OAuth認証を開始します ===")
    print(f"ブラウザで認証ページが開きます...")
    print(f"認証後、自動的にリダイレクトされます。")
    print(f"リダイレクトURI: {redirect_uri}\n")
    
    # ローカルサーバーを起動してコールバックを待機
    OAuthCallbackHandler.auth_code = None
    server = HTTPServer(('localhost', redirect_port), OAuthCallbackHandler)
    
    # サーバーを別スレッドで起動
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.daemon = True
    server_thread.start()
    
    # ブラウザで認証URLを開く
    webbrowser.open(auth_url)
    
    # 認証コードを待機
    timeout = 300  # 5分
    start_time = time.time()
    
    while OAuthCallbackHandler.auth_code is None:
        if time.time() - start_time > timeout:
            print("認証がタイムアウトしました。")
            return None
        time.sleep(0.5)
    
    auth_code = OAuthCallbackHandler.auth_code
    print(f"\n認証コードを取得しました: {auth_code[:10]}...")
    
    # 認証コードをアクセストークンに交換（PKCE対応、client_secret不要）
    print("\nアクセストークンを取得中...")
    token_url = f"https://{account_url}.snowflakecomputing.com/oauth/token-request"
    
    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'code_verifier': code_verifier  # PUBLICクライアントはclient_secretの代わりにcode_verifierを使用
    }
    
    try:
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        
        access_token = token_response.json()['access_token']
        print(f"✓ アクセストークンを取得しました")
        return access_token
        
    except requests.exceptions.RequestException as e:
        print(f"\nトークン取得エラー: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"レスポンス: {e.response.text}")
        return None


def get_oauth_token_external_browser_fallback():
    """
    外部ブラウザ認証（Snowflakeの externalbrowser 認証タイプを使用）
    
    注意: これはSnowflake Python Connectorの機能を使用する代替案です。
    REST API直接使用の場合は、上記のOAuth実装が必要です。
    """
    try:
        import snowflake.connector
        
        print("\nSnowflake Python Connectorを使用した外部ブラウザ認証を試みます...")
        print("ブラウザが開き、Snowflakeの認証ページにリダイレクトされます。")
        
        # この方法では、Snowflake Connectorが自動的にブラウザ認証を処理します
        return "USE_SNOWFLAKE_CONNECTOR"
        
    except ImportError:
        print("エラー: snowflake-connector-python がインストールされていません。")
        print("インストールするには: pip install snowflake-connector-python")
        return None

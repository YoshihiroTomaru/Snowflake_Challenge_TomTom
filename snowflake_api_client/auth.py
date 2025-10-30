import base64
import hashlib
import time

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def get_private_key_and_fingerprint(p8_file, passphrase):
    """
    秘密鍵ファイルを読み込み、鍵オブジェクトと公開鍵のフィンガープリントを返します。
    """
    with open(p8_file, "rb") as key_file:
        p_key = serialization.load_pem_private_key(
            key_file.read(),
            password=passphrase.encode() if passphrase else None,
            backend=default_backend()
        )

    public_key = p_key.public_key()
    public_key_der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    sha256_hash = hashlib.sha256(public_key_der).digest()
    public_key_fp = 'SHA256:' + base64.b64encode(sha256_hash).decode('utf-8')
    return p_key, public_key_fp


def generate_jwt(private_key, public_key_fp, snowflake_account, snowflake_user):
    """
    Snowflake認証用のJWTを生成します。
    """
    qualified_username = f"{snowflake_account.upper()}.{snowflake_user.upper()}"

    payload = {
        'iss': f"{qualified_username}.{public_key_fp}",
        'sub': qualified_username,
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600
    }

    token = jwt.encode(
        payload,
        private_key,
        algorithm='RS256'
    )
    return token

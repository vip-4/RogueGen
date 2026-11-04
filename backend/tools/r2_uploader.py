"""
Cloudflare R2 (S3-compatible) 上传工具。

用于将生成的美术资源 / 游戏包上传到 R2，供前端或下载链接使用。
需要在 backend/.env 中配置：
  R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET, R2_PUBLIC_BASE
"""
from __future__ import annotations

import os
from pathlib import Path

try:
    import boto3
    from botocore.config import Config
    _BOTO_AVAILABLE = True
except Exception:  # pragma: no cover
    _BOTO_AVAILABLE = False


def _settings():
    return {
        "account_id": os.getenv("R2_ACCOUNT_ID", ""),
        "access_key": os.getenv("R2_ACCESS_KEY_ID", ""),
        "secret_key": os.getenv("R2_SECRET_ACCESS_KEY", ""),
        "bucket": os.getenv("R2_BUCKET", ""),
        "public_base": os.getenv("R2_PUBLIC_BASE", ""),
        "endpoint": os.getenv(
            "R2_ENDPOINT",
            f"https://{os.getenv('R2_ACCOUNT_ID','')}.r2.cloudflarestorage.com",
        ),
    }


def is_configured() -> bool:
    s = _settings()
    return _BOTO_AVAILABLE and bool(s["access_key"] and s["secret_key"] and s["bucket"])


def upload_file(local_path: str | Path, key: str) -> str | None:
    """
    上传本地文件到 R2，返回可访问的公开 URL（若配置了 R2_PUBLIC_BASE）。
    未配置或 boto3 不可用时返回 None。
    """
    if not is_configured():
        return None
    s = _settings()
    client = boto3.client(
        "s3",
        endpoint_url=s["endpoint"],
        aws_access_key_id=s["access_key"],
        aws_secret_access_key=s["secret_key"],
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )
    client.upload_file(str(local_path), s["bucket"], key)
    if s["public_base"]:
        return f"{s['public_base'].rstrip('/')}/{key}"
    return None


def upload_bytes(data: bytes, key: str, content_type: str = "application/octet-stream") -> str | None:
    if not is_configured():
        return None
    s = _settings()
    client = boto3.client(
        "s3",
        endpoint_url=s["endpoint"],
        aws_access_key_id=s["access_key"],
        aws_secret_access_key=s["secret_key"],
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )
    client.put_object(Bucket=s["bucket"], Key=key, Body=data, ContentType=content_type)
    if s["public_base"]:
        return f"{s['public_base'].rstrip('/')}/{key}"
    return None

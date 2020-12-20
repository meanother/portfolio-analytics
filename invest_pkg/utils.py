from typing import Any


def set_default_headers(data: Any, token: str) -> None:
    headers = data.get('headers', {})
    headers.setdefault('accept', 'application/json')
    headers.setdefault('Authorization', f'Bearer {token}')
    data['headers'] = headers

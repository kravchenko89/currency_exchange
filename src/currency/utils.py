import hashlib


def genetere_rate_cache_key(source: int, currency: int) -> str:
    key = (f'latest-rates-{source}-{currency}' * 100).encode()
    return hashlib.md5(key).hexdigest()
    # return f'latest-rates-{source}-{currency}'

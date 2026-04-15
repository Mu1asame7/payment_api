import hashlib


def verify_signature(data: dict, signature: str, secret_key: str) -> bool:

    filtered_data = {k: v for k, v in data.items() if k != "signature"}

    text = ""

    for key, value in sorted(filtered_data.items()):
        text += str(value)

    text += secret_key

    sha256_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    return signature == sha256_hash

import base64
import os
from pathlib import Path
import django

BASE_DIR = Path(__file__).resolve().parent.parent

path = Path(BASE_DIR, "service_account_key_original.json")
with open(path, "r") as file:
    content = file.read()
    content_bytes = content.encode("utf-8")
    content_b64 = base64.b64encode(content_bytes)
    print("content_b64:", content_b64)

path = Path(BASE_DIR, "service_account_key_b64.json")
with open(path, "w") as file:
    file.write(content_b64.decode("utf-8"))

import os
import ssl
import json
import urllib.request
from .content import validate_and_fix_content, is_content_valid
from .platform import is_valid_url

def load_content(src=None, path="widget.json", default_content=None):
    if src:
        if not is_valid_url(src):
            raise ValueError(f"Invalid URL: {src}")
        try:
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(src, context=context) as response:
                content = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            raise ValueError(f"Failed to fetch from URL: {e}")
        if not is_content_valid(content, default_content):
            raise ValueError("Invalid content from src")
        return content

    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default_content, f, indent=2, ensure_ascii=False)
        return default_content

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = json.load(f)
    except json.JSONDecodeError:
        content = {}
    content = validate_and_fix_content(content, default_content)
    return content
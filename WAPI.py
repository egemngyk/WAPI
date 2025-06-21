import sys
import os
import json
import platform
import importlib
from urllib.parse import urlparse
import urllib.request
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

def is_android():
    try:
        import android
        return True
    except ImportError:
        return False

def is_valid_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https") and result.netloc
    except:
        return False

def validate_and_fix_content(content, default_content):
    if not (isinstance(content.get('size'), list) and len(content['size']) == 2 and
            all(isinstance(x, (int, float)) and x > 0 for x in content['size'])):
        content['size'] = default_content['size']
    if not isinstance(content.get('html'), str):
        content['html'] = default_content['html']
    if not isinstance(content.get('css'), str):
        content['css'] = default_content['css']
    if not isinstance(content.get('js'), str):
        content['js'] = default_content['js']
    if not isinstance(content.get('movable'), bool):
        content['movable'] = default_content['movable']
    if not isinstance(content.get('transparent'), bool):
        content['transparent'] = default_content['transparent']
    opacity = content.get('opacity')
    if not (isinstance(opacity, (int, float)) and 0 < opacity <= 1):
        content['opacity'] = default_content['opacity']
    second_opacity = content.get('second_opacity')
    if not (isinstance(second_opacity, (int, float)) and 0 < second_opacity <= 1):
        content['second_opacity'] = default_content['second_opacity']
    block_size = content.get('block_size')
    if not (isinstance(block_size, int) and block_size > 0):
        content['block_size'] = default_content['block_size']
    padding = content.get('padding')
    if not (isinstance(padding, int) and padding >= 0):
        content['padding'] = default_content['padding']
    if not (isinstance(content.get('position'), list) and len(content['position']) == 2 and
            all(isinstance(x, (int, float)) and x >= 0 for x in content['position'])):
        content['position'] = default_content['position']
    return content

def is_content_valid(content, default):
    try:
        test = content.copy()
        _ = validate_and_fix_content(test, default)
        return True
    except:
        return False

QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

system = platform.system().lower()
match system:
    case 'windows':
        os_name = 'Windows'
    case 'darwin':
        os_name = 'Ios' if 'ios' in sys.platform else 'Macos'
    case 'linux':
        os_name = 'Android' if is_android() else 'Linux'
    case _:
        os_name = 'unknown'

if os_name == 'unknown':
    print("WAPI support is not available for this platform.")
    sys.exit(1)

WidgetClass = getattr(importlib.import_module('widgets'), os_name)

class Widget:
    def __init__(self, src=None, path=None):
        self.app = QApplication(sys.argv)
        self.widget = WidgetClass()
        default_content = {
            "size": [200, 200],
            "html": "",
            "css": "",
            "js": "",
            "movable": True,
            "transparent": False,
            "opacity": 1.0,
            "second_opacity": 0.5,
            "block_size": 15,
            "padding": 20,
            "position": [35, 35]
        }

        if src:
            if not is_valid_url(src):
                raise ValueError(f"Invalid URL format: {src}")
            try:
                with urllib.request.urlopen(src) as response:
                    content_from_src = json.loads(response.read().decode('utf-8'))
            except Exception as e:
                raise ValueError(f"Failed to fetch JSON from URL: {e}")
            if not is_content_valid(content_from_src, default_content):
                raise ValueError("Content from src is invalid and cannot be auto-fixed.")
            self.content = content_from_src
        else:
            if not path:
                path = "widget.json"
            if not path.lower().endswith(".json"):
                path += ".json"
            self.path = path

            if not os.path.exists(self.path):
                with open(self.path, 'w', encoding='utf-8') as f:
                    json.dump(default_content, f, indent=2, ensure_ascii=False)
                self.content = default_content
            else:
                with open(self.path, 'r', encoding='utf-8') as f:
                    try:
                        file_content = json.load(f)
                    except json.JSONDecodeError:
                        file_content = {}
                file_content = validate_and_fix_content(file_content, default_content)
                updated = False
                for key, value in default_content.items():
                    if key not in file_content:
                        file_content[key] = value
                        updated = True
                if updated:
                    with open(self.path, 'w', encoding='utf-8') as f:
                        json.dump(file_content, f, indent=2, ensure_ascii=False)
                self.content = file_content

        for key, value in self.content.items():
            setattr(self.widget, key, value)

    def start(self):
        self.widget.start()

    def stop(self):
        self.widget.stop()
        self.app.quit()
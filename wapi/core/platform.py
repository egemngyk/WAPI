import platform
import sys
import importlib
from urllib.parse import urlparse

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

def get_os():
    system = platform.system().lower()
    if system == "windows":
        return getattr(importlib.import_module('wapi.desktop.windows'), 'Windows')
    elif system == "darwin":
        if "ios" in sys.platform:
            return getattr(importlib.import_module('wapi.mobile.ios'), 'Ios')
        return getattr(importlib.import_module('wapi.desktop.macos'), 'Macos')
    elif system == "linux":
        if is_android():
            return getattr(importlib.import_module('wapi.mobile.android'), 'Android')
        return getattr(importlib.import_module('wapi.desktop.linux'), 'Linux')
    else:
        print("WAPI support is not available for this platform.")
        sys.exit(1)
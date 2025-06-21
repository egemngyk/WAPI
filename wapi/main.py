import sys
from PyQt6.QtWidgets import QApplication
from .core.platform import get_os
from .core.loader import load_content
from .core.content import validate_and_fix_content

DEFAULT_CONTENT = {
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

class Widget:
    def __init__(self, src=None, path=None):
        WidgetClass = get_os()
        self.app = QApplication(sys.argv)
        self.widget = WidgetClass()
        self.content = load_content(src, path or "widget.json", DEFAULT_CONTENT)

        for key, value in self.content.items():
            setattr(self.widget, key, value)

    def start(self):
        self.widget.start()

    def stop(self):
        self.widget.stop()
        self.app.quit()
from .base import PcWidget
from PyQt6.QtCore import Qt

class Linux(PcWidget):
    def __init__(self):
        super().__init__()
        self.setFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnBottomHint |
            Qt.WindowType.X11BypassWindowManagerHint
        )
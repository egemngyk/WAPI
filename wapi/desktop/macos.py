from .base import PcWidget
from PyQt6.QtCore import Qt

class Macos(PcWidget):
    def __init__(self):
        super().__init__()
        self.setFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnBottomHint
        )
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWebEngineWidgets import QWebEngineView

class PcWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.size = (500, 200)
        self.html = ""
        self.css = ""
        self.js = ""
        self.movable = True
        self.opacity = 1.0
        self.transparent = False
        self.second_opacity = 0.3
        self.block_size = 20
        self.padding = 10
        self.position = (0, 0)
        self.old_pos = None

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(*self.size)
        self.setMouseTracking(True)

        self.webview = QWebEngineView(self)
        self.webview.setGeometry(0, 0, *self.size)
        self.webview.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def setFlags(self, flags):
        self.setWindowFlags(flags)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
            self.setWindowOpacity(self.opacity)

    def mouseMoveEvent(self, event):
        if self.old_pos is not None and self.movable:
            current_pos = event.globalPosition().toPoint()
            delta = current_pos - self.old_pos

            move_x = (delta.x() // self.block_size) * self.block_size
            move_y = (delta.y() // self.block_size) * self.block_size

            if move_x != 0 or move_y != 0:
                new_x = self.x() + move_x
                new_y = self.y() + move_y

                desktop_rect = QtCore.QRect()
                for screen in QtWidgets.QApplication.screens():
                    desktop_rect = desktop_rect.united(screen.availableGeometry())

                widget_w = self.width()
                widget_h = self.height()

                new_x = max(desktop_rect.left() + self.padding,
                            min(new_x, desktop_rect.right() - widget_w - self.padding))
                new_y = max(desktop_rect.top() + self.padding,
                            min(new_y, desktop_rect.bottom() - widget_h - self.padding))

                self.move(new_x, new_y)
                self.old_pos = QtCore.QPoint(self.old_pos.x() + move_x, self.old_pos.y() + move_y)

            self.setWindowOpacity(self.second_opacity)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.old_pos = None
            self.setWindowOpacity(self.opacity)

    def _build_ui(self):
        html_with_css = f"""
        <html>
        <head>
            <style>{self.css}</style>
        </head>
        <body>
            {self.html}
        </body>
        </html>
        """
        self.webview.setHtml(html_with_css)
        self.webview.loadFinished.connect(lambda ok: self.webview.page().runJavaScript(self.js.strip()))
        self.move(*self.position)

    def closeEvent(self, event):
        event.ignore()

    def event(self, event):
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            if self.isMinimized():
                QtCore.QTimer.singleShot(0, self.showNormal)
        return super().event(event)

    def start(self):
        self.setFixedSize(*self.size)
        self.webview.setGeometry(0, 0, *self.size)
        self._build_ui()
        self.show()
        self.setWindowOpacity(self.opacity)
        if self.transparent:
            self.webview.setStyleSheet("background: transparent;")
            self.webview.page().setBackgroundColor(QtCore.Qt.GlobalColor.transparent)
        else:
            self.webview.setStyleSheet("background: white;")
            self.webview.page().setBackgroundColor(QtCore.Qt.GlobalColor.white)

    def stop(self):
        self.hide()
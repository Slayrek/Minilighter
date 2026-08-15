import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen

class OverlayWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool | 
            Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        # Determine total desktop size
        desktop = QApplication.desktop()
        self.setGeometry(desktop.geometry())
        
        self.start_point = None
        self.end_point = None
        self.selected_rect = None
        self.is_drawing = False
        self.is_finished = False
        
        self.fade_timer = QTimer(self)
        self.fade_timer.setSingleShot(True)
        self.fade_timer.timeout.connect(self.close)

        # Show full screen across all monitors
        self.showFullScreen()
        self.setCursor(Qt.CrossCursor)
        self.setFocus()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.is_finished:
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.is_drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing and not self.is_finished:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_drawing:
            self.end_point = event.pos()
            self.is_drawing = False
            self.is_finished = True
            self.update()
            
            # Start timer if behavior is fade
            if self.config.get('behavior', 'fade') == 'fade':
                timeout_ms = int(self.config.get('fade_timeout', 3.0) * 1000)
                self.fade_timer.start(timeout_ms)
                
            # If persist, we change the flags to allow clicks to pass through if needed.
            # But the user might want to click through the highlight.
            # To click through, we'd need to set Qt.WindowTransparentForInput, 
            # but then we can't catch Esc key. 
            # We'll just keep it catching inputs so Esc can close it, or we can use the global hotkey to close.
            # Actually, if they want it for demos, allowing clicks through is crucial.
            if self.config.get('behavior', 'fade') == 'persist':
                self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fill whole screen with dimmed color
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))
        
        # Calculate current rect
        current_rect = None
        if self.is_drawing and self.start_point and self.end_point:
            current_rect = QRect(self.start_point, self.end_point).normalized()
        elif self.is_finished and self.start_point and self.end_point:
            current_rect = QRect(self.start_point, self.end_point).normalized()
            
        if current_rect:
            # Clear the inside of the rect so it's fully transparent
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(current_rect, Qt.transparent)
            
            # Draw dashed border
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            pen = QPen(Qt.white, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(current_rect)

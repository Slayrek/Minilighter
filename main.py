import sys
import threading
import keyboard
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication

import config_mgr
from settings_ui import SettingsDialog
from overlay_ui import OverlayWidget

class AppController(QObject):
    show_overlay_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.config = config_mgr.load_config()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        self.overlay = None
        self.settings_dialog = None
        
        self.show_overlay_signal.connect(self.show_overlay)
        
        self.init_tray()
        self.register_hotkey()

    def create_icon(self):
        # Create a simple icon programmatically
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor("transparent"))
        painter = QPainter(pixmap)
        painter.setBrush(QColor(255, 200, 0))
        painter.drawRect(8, 8, 48, 48)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(16, 16, 32, 32)
        painter.end()
        return QIcon(pixmap)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self.create_icon(), self.app)
        self.tray_icon.setToolTip("Minilighter")
        
        menu = QMenu()
        
        settings_action = QAction("Settings", self.app)
        settings_action.triggered.connect(self.open_settings)
        menu.addAction(settings_action)
        
        quit_action = QAction("Quit", self.app)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def register_hotkey(self):
        shortcut = self.config.get('shortcut', 'alt+shift+h')
        try:
            keyboard.add_hotkey(shortcut, self.trigger_overlay)
        except Exception as e:
            print(f"Failed to register hotkey: {e}")

    def trigger_overlay(self):
        self.show_overlay_signal.emit()

    def show_overlay(self):
        # Close existing overlay if any
        if self.overlay:
            try:
                self.overlay.close()
            except Exception:
                pass
            self.overlay = None
            
        self.overlay = OverlayWidget(self.config)
        self.overlay.show()

    def open_settings(self):
        if not self.settings_dialog:
            self.settings_dialog = SettingsDialog()
            
        if self.settings_dialog.exec_():
            # Reload config and update hotkey
            keyboard.unhook_all_hotkeys()
            self.config = config_mgr.load_config()
            self.register_hotkey()
            
    def quit_app(self):
        keyboard.unhook_all_hotkeys()
        self.app.quit()
        
    def run(self):
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    controller = AppController()
    controller.run()

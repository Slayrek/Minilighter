import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDoubleSpinBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import config_mgr

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Minilighter Settings")
        self.setFixedSize(350, 200)
        self.config = config_mgr.load_config()
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Shortcut
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Shortcut:"))
        self.shortcut_input = QLineEdit()
        self.shortcut_input.setText(self.config.get('shortcut', 'alt+shift+h'))
        self.shortcut_input.setToolTip("e.g. alt+shift+h, ctrl+space")
        hbox1.addWidget(self.shortcut_input)
        layout.addLayout(hbox1)
        
        # Behavior
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Behavior:"))
        self.behavior_combo = QComboBox()
        self.behavior_combo.addItem("Fade out automatically", "fade")
        self.behavior_combo.addItem("Persist until Esc clicked", "persist")
        
        idx = self.behavior_combo.findData(self.config.get('behavior', 'fade'))
        if idx >= 0:
            self.behavior_combo.setCurrentIndex(idx)
        hbox2.addWidget(self.behavior_combo)
        layout.addLayout(hbox2)
        
        # Timeout
        hbox3 = QHBoxLayout()
        hbox3.addWidget(QLabel("Fade Timeout (sec):"))
        self.timeout_spin = QDoubleSpinBox()
        self.timeout_spin.setRange(0.5, 60.0)
        self.timeout_spin.setValue(self.config.get('fade_timeout', 3.0))
        hbox3.addWidget(self.timeout_spin)
        layout.addLayout(hbox3)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
    def save_settings(self):
        shortcut = self.shortcut_input.text().strip().lower()
        if not shortcut:
            QMessageBox.warning(self, "Error", "Shortcut cannot be empty.")
            return
            
        self.config['shortcut'] = shortcut
        self.config['behavior'] = self.behavior_combo.currentData()
        self.config['fade_timeout'] = self.timeout_spin.value()
        
        config_mgr.save_config(self.config)
        self.accept()

"""Satış ekranı"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from config.messages import MESSAGES

class SalesScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title = QLabel(MESSAGES['sales'])
        title.setFont(QFont('Arial', 18, QFont.Bold))
        layout.addWidget(title)
        
        label = QLabel('Satış modülü geliştiriliyor...')
        layout.addWidget(label)
        
        layout.addStretch()

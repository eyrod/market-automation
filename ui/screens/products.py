"""Ürün yönetimi ekranı"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from config.messages import MESSAGES

class ProductsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title = QLabel(MESSAGES['products'])
        title.setFont(QFont('Arial', 18, QFont.Bold))
        layout.addWidget(title)
        
        label = QLabel('Ürün yönetimi modülü geliştiriliyor...')
        layout.addWidget(label)
        
        layout.addStretch()

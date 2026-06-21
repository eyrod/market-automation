"""Kontrol Paneli ekranı"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from database.repositories import (
    SalesRepository, ProductRepository, CustomerRepository
)
from config.messages import MESSAGES
from datetime import datetime

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.sales_repo = SalesRepository()
        self.product_repo = ProductRepository()
        self.customer_repo = CustomerRepository()
        
        self.init_ui()
        self.load_data()
        
        # Veriler otomatik yenileme
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(30000)  # 30 saniyede bir
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Başlık
        title = QLabel(MESSAGES['dashboard'])
        title.setFont(QFont('Arial', 18, QFont.Bold))
        layout.addWidget(title)
        
        # Grid layout - İstatistikler
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Günlük satış
        self.daily_sales_card = self.create_stat_card(
            MESSAGES['daily_sales'],
            '₺0.00',
            '#4CAF50'
        )
        grid.addWidget(self.daily_sales_card, 0, 0)
        
        # Aylık satış
        self.monthly_sales_card = self.create_stat_card(
            MESSAGES['monthly_sales'],
            '₺0.00',
            '#2196F3'
        )
        grid.addWidget(self.monthly_sales_card, 0, 1)
        
        # Toplam ürün
        self.total_products_card = self.create_stat_card(
            MESSAGES['total_products'],
            '0',
            '#FF9800'
        )
        grid.addWidget(self.total_products_card, 0, 2)
        
        # Kasa durumu
        self.cash_register_card = self.create_stat_card(
            MESSAGES['cash_register'],
            '₺0.00',
            '#9C27B0'
        )
        grid.addWidget(self.cash_register_card, 0, 3)
        
        # Kritik stok ürünleri
        self.critical_stock_card = self.create_stat_card(
            MESSAGES['critical_stock'],
            '0 ürün',
            '#F44336'
        )
        grid.addWidget(self.critical_stock_card, 1, 0)
        
        # Bekleyen siparişler
        self.pending_orders_card = self.create_stat_card(
            MESSAGES['pending_orders'],
            '0 sipariş',
            '#00BCD4'
        )
        grid.addWidget(self.pending_orders_card, 1, 1)
        
        # Veresiye toplam
        self.credit_balance_card = self.create_stat_card(
            MESSAGES['credit_balance'],
            '₺0.00',
            '#8BC34A'
        )
        grid.addWidget(self.credit_balance_card, 1, 2)
        
        layout.addLayout(grid)
        layout.addStretch()
    
    def create_stat_card(self, title, value, color):
        """İstatistik kartı oluştur"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-left: 5px solid {color};
                border-radius: 4px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        
        # Başlık
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 12, QFont.Bold))
        title_label.setStyleSheet('color: #666;')
        layout.addWidget(title_label)
        
        # Değer
        value_label = QLabel(value)
        value_label.setFont(QFont('Arial', 24, QFont.Bold))
        value_label.setStyleSheet(f'color: {color};')
        layout.addWidget(value_label)
        
        # Referansları saklama
        frame.title_label = title_label
        frame.value_label = value_label
        
        return frame
    
    def load_data(self):
        """Verileri yükle"""
        try:
            # Günlük satış
            daily = self.sales_repo.get_daily_sales()
            self.daily_sales_card.value_label.setText(f'₺{daily:.2f}')
            
            # Aylık satış
            monthly = self.sales_repo.get_monthly_sales()
            self.monthly_sales_card.value_label.setText(f'₺{monthly:.2f}')
            
            # Toplam ürün
            products = self.product_repo.get_all()
            total_products = len(products) if products else 0
            self.total_products_card.value_label.setText(str(total_products))
            
            # Kritik stok
            critical = self.product_repo.get_critical_stock()
            critical_count = len(critical) if critical else 0
            self.critical_stock_card.value_label.setText(f'{critical_count} ürün')
            
            # Veresiye toplam
            credit_balance = self.customer_repo.get_credit_balance()
            self.credit_balance_card.value_label.setText(f'₺{credit_balance:.2f}')
            
        except Exception as e:
            print(f'Dashboard yükleme hatası: {e}')

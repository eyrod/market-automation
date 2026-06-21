"""Ana uygulama penceresi"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QMenuBar, QMenu, QStatusBar,
    QMessageBox, QDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from config.settings import APP_NAME, APP_VERSION, DEFAULT_THEME
from config.messages import MESSAGES
from ui.styles import get_theme
from ui.screens.dashboard import DashboardScreen
from ui.screens.sales import SalesScreen
from ui.screens.products import ProductsScreen
from ui.screens.customers import CustomersScreen
from ui.screens.credit_sales import CreditSalesScreen
from ui.screens.reports import ReportsScreen
from ui.screens.users import UsersScreen
from ui.screens.settings import SettingsScreen
import json
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.theme = DEFAULT_THEME
        self.settings_file = Path('app_settings.json')
        
        self.init_ui()
        self.load_settings()
        self.setStyleSheet(get_theme(self.theme))
    
    def init_ui(self):
        """UI'yi başlat"""
        self.setWindowTitle(f'{APP_NAME} v{APP_VERSION}')
        self.setGeometry(100, 100, 1200, 700)
        self.setMinimumSize(1024, 600)
        
        # Ana widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Ana layout
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sol panel - Menü
        self.create_menu_panel()
        
        # Sağ panel - İçerik
        self.stacked_widget = QStackedWidget()
        
        # Ekranları ekle
        self.dashboard_screen = DashboardScreen()
        self.sales_screen = SalesScreen()
        self.products_screen = ProductsScreen()
        self.customers_screen = CustomersScreen()
        self.credit_sales_screen = CreditSalesScreen()
        self.reports_screen = ReportsScreen()
        self.users_screen = UsersScreen()
        self.settings_screen = SettingsScreen()
        
        self.stacked_widget.addWidget(self.dashboard_screen)
        self.stacked_widget.addWidget(self.sales_screen)
        self.stacked_widget.addWidget(self.products_screen)
        self.stacked_widget.addWidget(self.customers_screen)
        self.stacked_widget.addWidget(self.credit_sales_screen)
        self.stacked_widget.addWidget(self.reports_screen)
        self.stacked_widget.addWidget(self.users_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        
        # Menu bar
        self.create_menu_bar()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Hazır')
        
        # Layout'a ekle
        main_layout.addWidget(self.stacked_widget)
    
    def create_menu_panel(self):
        """Sol menü panelini oluştur"""
        pass  # Toolbar veya side menu eklenebilir
    
    def create_menu_bar(self):
        """Menü barını oluştur"""
        menubar = self.menuBar()
        
        # Dosya menüsü
        file_menu = menubar.addMenu('Dosya')
        
        dashboard_action = file_menu.addAction('Kontrol Paneli')
        dashboard_action.triggered.connect(lambda: self.show_screen(0))
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('Çıkış')
        exit_action.triggered.connect(self.close)
        
        # Satış menüsü
        sales_menu = menubar.addMenu('Satış')
        
        new_sale_action = sales_menu.addAction('Yeni Satış')
        new_sale_action.triggered.connect(lambda: self.show_screen(1))
        
        # Ürün menüsü
        product_menu = menubar.addMenu('Ürünler')
        
        manage_products_action = product_menu.addAction('Ürün Yönetimi')
        manage_products_action.triggered.connect(lambda: self.show_screen(2))
        
        # Müşteri menüsü
        customer_menu = menubar.addMenu('Müşteriler')
        
        manage_customers_action = customer_menu.addAction('Müşteri Yönetimi')
        manage_customers_action.triggered.connect(lambda: self.show_screen(3))
        
        credit_sales_action = customer_menu.addAction('Veresiye')
        credit_sales_action.triggered.connect(lambda: self.show_screen(4))
        
        # Raporlar menüsü
        reports_menu = menubar.addMenu('Raporlar')
        
        reports_action = reports_menu.addAction('Satış Raporları')
        reports_action.triggered.connect(lambda: self.show_screen(5))
        
        # Ayarlar menüsü
        settings_menu = menubar.addMenu('Ayarlar')
        
        users_action = settings_menu.addAction('Personel')
        users_action.triggered.connect(lambda: self.show_screen(6))
        
        settings_action = settings_menu.addAction('Sistem Ayarları')
        settings_action.triggered.connect(lambda: self.show_screen(7))
    
    def show_screen(self, index):
        """Belirli ekranı göster"""
        self.stacked_widget.setCurrentIndex(index)
    
    def load_settings(self):
        """Ayarları yükle"""
        if self.settings_file.exists():
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                self.theme = settings.get('theme', DEFAULT_THEME)
    
    def save_settings(self):
        """Ayarları kaydet"""
        settings = {
            'theme': self.theme,
            'last_user': self.current_user.get('username') if self.current_user else None
        }
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    
    def closeEvent(self, event):
        """Uygulama kapatılırken"""
        self.save_settings()
        event.accept()

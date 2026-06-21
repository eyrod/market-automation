"""Ürün yönetimi ekranı - Kapsamlı ürün sistemi"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QSpinBox,
    QDoubleSpinBox, QComboBox, QMessageBox, QTabWidget, QFrame,
    QHeaderView, QDialog, QFormLayout, QFileDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor
from database.db_manager import get_db_manager
from database.repositories import ProductRepository, CustomerRepository
from config.messages import MESSAGES
import sqlite3

class ProductsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.product_repo = ProductRepository()
        self.db = get_db_manager()
        self.init_ui()
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Tab Widget
        tabs = QTabWidget()
        tabs.addTab(self.create_products_tab(), "Ürün Listesi")
        tabs.addTab(self.create_add_product_tab(), "Yeni Ürün Ekle")
        tabs.addTab(self.create_import_export_tab(), "İthalatçı/İhracatçı")
        tabs.addTab(self.create_categories_tab(), "Kategoriler")
        tabs.addTab(self.create_critical_stock_tab(), "Kritik Stok")
        
        layout.addWidget(tabs)
    
    def create_products_tab(self):
        """Ürün listesi sekmesi"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Arama
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Ara:"))
        self.product_search = QLineEdit()
        self.product_search.setPlaceholderText("Ürün adı veya barkod ara...")
        self.product_search.textChanged.connect(self.search_products)
        search_layout.addWidget(self.product_search)
        
        filter_combo = QComboBox()
        filter_combo.addItems(["Tüm Ürünler", "Aktif", "Pasif", "Düşük Stok"])
        filter_combo.currentIndexChanged.connect(self.apply_filter)
        search_layout.addWidget(filter_combo)
        
        layout.addLayout(search_layout)
        
        # Ürün tablosu
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(8)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Barkod", "Ürün Adı", "Kategori", "Fiyat", "Stok", "Durum", "İşlem"
        ])
        self.products_table.setColumnHidden(0, True)
        self.products_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        layout.addWidget(self.products_table)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Yenile")
        refresh_btn.clicked.connect(self.load_products)
        button_layout.addWidget(refresh_btn)
        
        delete_btn = QPushButton("Sil")
        delete_btn.setStyleSheet("background-color: #f44336; color: white;")
        delete_btn.clicked.connect(self.delete_product)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.load_products()
        return widget
    
    def create_add_product_tab(self):
        """Yeni ürün ekleme sekmesi"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        form_layout = QGridLayout()
        
        # Barkod
        form_layout.addWidget(QLabel("Barkod:"), 0, 0)
        self.barcode_input = QLineEdit()
        form_layout.addWidget(self.barcode_input, 0, 1)
        
        # Ürün Adı
        form_layout.addWidget(QLabel("Ürün Adı:"), 1, 0)
        self.product_name_input = QLineEdit()
        form_layout.addWidget(self.product_name_input, 1, 1)
        
        # Kategori
        form_layout.addWidget(QLabel("Kategori:"), 2, 0)
        self.category_combo = QComboBox()
        self.load_categories()
        form_layout.addWidget(self.category_combo, 2, 1)
        
        # Alış Fiyatı
        form_layout.addWidget(QLabel("Alış Fiyatı:"), 3, 0)
        self.purchase_price_input = QDoubleSpinBox()
        self.purchase_price_input.setMaximum(999999)
        form_layout.addWidget(self.purchase_price_input, 3, 1)
        
        # Satış Fiyatı
        form_layout.addWidget(QLabel("Satış Fiyatı:"), 4, 0)
        self.sale_price_input = QDoubleSpinBox()
        self.sale_price_input.setMaximum(999999)
        form_layout.addWidget(self.sale_price_input, 4, 1)
        
        # Stok
        form_layout.addWidget(QLabel("Stok:"), 5, 0)
        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(999999)
        form_layout.addWidget(self.stock_input, 5, 1)
        
        # Minimum Stok
        form_layout.addWidget(QLabel("Minimum Stok:"), 6, 0)
        self.min_stock_input = QSpinBox()
        self.min_stock_input.setValue(10)
        form_layout.addWidget(self.min_stock_input, 6, 1)
        
        # Birim
        form_layout.addWidget(QLabel("Birim:"), 7, 0)
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Adet", "Kg", "Litre", "Metre", "Paket"])
        form_layout.addWidget(self.unit_combo, 7, 1)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        # Ekle butonu
        add_btn = QPushButton("ÜRÜN EKLE")
        add_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        add_btn.clicked.connect(self.add_new_product)
        layout.addWidget(add_btn)
        
        return widget
    
    def create_import_export_tab(self):
        """İthalatçı/İhracatçı sekmesi"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("EXCEL İthalatçı/İhracatçı")
        title.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(title)
        
        # Bilgi
        info_text = QLabel(
            "Excel dosyasından ürünleri toplu olarak içe aktarabilir veya dışa aktarabilirsiniz.\n\n"
            "Gerekli sütunlar: Barkod, Ürün Adı, Kategori, Alış Fiyatı, Satış Fiyatı, Stok, Birim"
        )
        layout.addWidget(info_text)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        export_btn = QPushButton("EXCEL'E AKTAR")
        export_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        export_btn.clicked.connect(self.export_to_excel)
        button_layout.addWidget(export_btn)
        
        import_btn = QPushButton("EXCEL'DEN İÇE AKTAR")
        import_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 10px;")
        import_btn.clicked.connect(self.import_from_excel)
        button_layout.addWidget(import_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        return widget
    
    def create_categories_tab(self):
        """Kategoriler sekmesi"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Kategori tablosu
        self.categories_table = QTableWidget()
        self.categories_table.setColumnCount(3)
        self.categories_table.setHorizontalHeaderLabels(["ID", "Kategori Adı", "İşlem"])
        self.categories_table.setColumnHidden(0, True)
        self.categories_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.categories_table)
        
        # Yeni kategori
        new_cat_layout = QHBoxLayout()
        self.new_category_input = QLineEdit()
        self.new_category_input.setPlaceholderText("Yeni kategori adı...")
        new_cat_layout.addWidget(self.new_category_input)
        
        add_cat_btn = QPushButton("KATEGORİ EKLE")
        add_cat_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        add_cat_btn.clicked.connect(self.add_category)
        new_cat_layout.addWidget(add_cat_btn)
        
        layout.addLayout(new_cat_layout)
        
        self.load_categories_list()
        return widget
    
    def create_critical_stock_tab(self):
        """Kritik stok sekmesi"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("KRİTİK STOK ÜRÜNLER")
        title.setFont(QFont('Arial', 12, QFont.Bold))
        title.setStyleSheet("color: #d32f2f;")
        layout.addWidget(title)
        
        # Kritik stok tablosu
        self.critical_table = QTableWidget()
        self.critical_table.setColumnCount(5)
        self.critical_table.setHorizontalHeaderLabels([
            "ID", "Ürün Adı", "Stok", "Min. Stok", "İşlem"
        ])
        self.critical_table.setColumnHidden(0, True)
        self.critical_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.critical_table)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Yenile")
        refresh_btn.clicked.connect(self.load_critical_stock)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.load_critical_stock()
        return widget
    
    def load_products(self):
        """Ürünleri yükle"""
        self.products_table.setRowCount(0)
        products = self.product_repo.get_all()
        
        for row, product in enumerate(products):
            self.products_table.insertRow(row)
            
            self.products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            self.products_table.setItem(row, 1, QTableWidgetItem(product.get('barcode', '')))
            self.products_table.setItem(row, 2, QTableWidgetItem(product['name']))
            
            # Kategori
            category = self.get_category_name(product['category_id']) if product['category_id'] else 'N/A'
            self.products_table.setItem(row, 3, QTableWidgetItem(category))
            
            self.products_table.setItem(row, 4, QTableWidgetItem(f"₺{product['sale_price']:.2f}"))
            self.products_table.setItem(row, 5, QTableWidgetItem(str(product['stock'])))
            self.products_table.setItem(row, 6, QTableWidgetItem(product['status']))
            
            # Edit butonu
            edit_btn = QPushButton("Düzenle")
            edit_btn.clicked.connect(lambda checked, p_id=product['id']: self.edit_product(p_id))
            self.products_table.setCellWidget(row, 7, edit_btn)
    
    def search_products(self):
        """Ürünleri ara"""
        search_text = self.product_search.text().lower()
        self.products_table.setRowCount(0)
        
        products = self.product_repo.get_all()
        for product in products:
            if search_text in product['name'].lower() or search_text in str(product.get('barcode', '')):
                row = self.products_table.rowCount()
                self.products_table.insertRow(row)
                
                self.products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
                self.products_table.setItem(row, 1, QTableWidgetItem(product.get('barcode', '')))
                self.products_table.setItem(row, 2, QTableWidgetItem(product['name']))
                
                category = self.get_category_name(product['category_id']) if product['category_id'] else 'N/A'
                self.products_table.setItem(row, 3, QTableWidgetItem(category))
                
                self.products_table.setItem(row, 4, QTableWidgetItem(f"₺{product['sale_price']:.2f}"))
                self.products_table.setItem(row, 5, QTableWidgetItem(str(product['stock'])))
                self.products_table.setItem(row, 6, QTableWidgetItem(product['status']))
                
                edit_btn = QPushButton("Düzenle")
                edit_btn.clicked.connect(lambda checked, p_id=product['id']: self.edit_product(p_id))
                self.products_table.setCellWidget(row, 7, edit_btn)
    
    def apply_filter(self, index):
        """Filtre uygula"""
        # Filtre uygulaması
        self.load_products()
    
    def add_new_product(self):
        """Yeni ürün ekle"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO products 
                (barcode, name, category_id, purchase_price, sale_price, stock, min_stock, unit, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.barcode_input.text(),
                self.product_name_input.text(),
                self.category_combo.currentData() or None,
                self.purchase_price_input.value(),
                self.sale_price_input.value(),
                self.stock_input.value(),
                self.min_stock_input.value(),
                self.unit_combo.currentText(),
                'aktif'
            ))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Başarı", "Ürün başarıyla eklendi!")
            
            # Formu temizle
            self.barcode_input.clear()
            self.product_name_input.clear()
            self.purchase_price_input.setValue(0)
            self.sale_price_input.setValue(0)
            self.stock_input.setValue(0)
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ürün eklenirken hata oluştu: {str(e)}")
    
    def edit_product(self, product_id):
        """Ürünü düzenle"""
        # Düzenleme diyalog açılacak
        QMessageBox.information(self, "Bilgi", f"Ürün {product_id} düzenleniyor...")
    
    def delete_product(self):
        """Ürünü sil"""
        selected_items = self.products_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir ürün seçiniz!")
            return
        
        product_id = int(self.products_table.item(selected_items[0].row(), 0).text())
        
        reply = QMessageBox.question(self, "Onay", "Ürünü silmek istediğinize emin misiniz?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('UPDATE products SET status = ? WHERE id = ?', ('pasif', product_id))
                
                conn.commit()
                conn.close()
                
                QMessageBox.information(self, "Başarı", "Ürün silindi!")
                self.load_products()
                
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Ürün silinirken hata oluştu: {str(e)}")
    
    def load_categories(self):
        """Kategorileri yükle"""
        self.category_combo.clear()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM categories')
        
        for category in cursor.fetchall():
            self.category_combo.addItem(category['name'], category['id'])
        
        conn.close()
    
    def load_categories_list(self):
        """Kategorileri tabloya yükle"""
        self.categories_table.setRowCount(0)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM categories')
        
        for row, category in enumerate(cursor.fetchall()):
            self.categories_table.insertRow(row)
            self.categories_table.setItem(row, 0, QTableWidgetItem(str(category['id'])))
            self.categories_table.setItem(row, 1, QTableWidgetItem(category['name']))
            
            delete_btn = QPushButton("Sil")
            delete_btn.setStyleSheet("background-color: #f44336; color: white;")
            delete_btn.clicked.connect(lambda checked, c_id=category['id']: self.delete_category(c_id))
            self.categories_table.setCellWidget(row, 2, delete_btn)
        
        conn.close()
    
    def add_category(self):
        """Kategori ekle"""
        category_name = self.new_category_input.text().strip()
        
        if not category_name:
            QMessageBox.warning(self, "Uyarı", "Kategori adı boş olamaz!")
            return
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
            
            conn.commit()
            conn.close()
            
            self.new_category_input.clear()
            self.load_categories()
            self.load_categories_list()
            
            QMessageBox.information(self, "Başarı", "Kategori eklendi!")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kategori eklenirken hata oluştu: {str(e)}")
    
    def delete_category(self, category_id):
        """Kategori sil"""
        reply = QMessageBox.question(self, "Onay", "Kategoriyi silmek istediğinize emin misiniz?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
                
                conn.commit()
                conn.close()
                
                self.load_categories()
                self.load_categories_list()
                
                QMessageBox.information(self, "Başarı", "Kategori silindi!")
                
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kategori silinirken hata oluştu: {str(e)}")
    
    def load_critical_stock(self):
        """Kritik stok ürünlerini yükle"""
        self.critical_table.setRowCount(0)
        
        critical_products = self.product_repo.get_critical_stock()
        
        for row, product in enumerate(critical_products):
            self.critical_table.insertRow(row)
            
            self.critical_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            self.critical_table.setItem(row, 1, QTableWidgetItem(product['name']))
            self.critical_table.setItem(row, 2, QTableWidgetItem(str(product['stock'])))
            self.critical_table.setItem(row, 3, QTableWidgetItem(str(product['min_stock'])))
            
            # Stok ekle butonu
            add_stock_btn = QPushButton("Stok Ekle")
            add_stock_btn.setStyleSheet("background-color: #4CAF50; color: white;")
            add_stock_btn.clicked.connect(lambda checked, p_id=product['id']: self.add_stock(p_id))
            self.critical_table.setCellWidget(row, 4, add_stock_btn)
    
    def add_stock(self, product_id):
        """Stok ekle"""
        from PyQt5.QtWidgets import QInputDialog
        
        quantity, ok = QInputDialog.getInt(self, "Stok Ekle", "Eklenecek miktar:", 1, 1, 10000)
        
        if ok:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('UPDATE products SET stock = stock + ? WHERE id = ?', (quantity, product_id))
                
                conn.commit()
                conn.close()
                
                self.load_critical_stock()
                QMessageBox.information(self, "Başarı", f"{quantity} adet stok eklendi!")
                
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Stok eklenirken hata oluştu: {str(e)}")
    
    def export_to_excel(self):
        """Excel'e aktar"""
        QMessageBox.information(self, "Bilgi", "Excel'e aktarma işlemi başlıyor...")
    
    def import_from_excel(self):
        """Excel'den içe aktar"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Excel Dosyası Seç", "", "Excel Files (*.xlsx)")
        
        if file_path:
            QMessageBox.information(self, "Bilgi", f"Dosya seçildi: {file_path}")
    
    def get_category_name(self, category_id):
        """Kategori adını getir"""
        if not category_id:
            return "N/A"
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM categories WHERE id = ?', (category_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result['name'] if result else 'N/A'

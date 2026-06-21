"""Veritabanı işlemleri için repository sınıfları"""
from database.db_manager import get_db_manager
from datetime import datetime, timedelta

class BaseRepository:
    """Temel repository sınıfı"""
    def __init__(self):
        self.db = get_db_manager()

class ProductRepository(BaseRepository):
    """Ürün işlemleri"""
    
    def get_all(self):
        """Tüm ürünleri getir"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE status = "aktif"')
        products = cursor.fetchall()
        conn.close()
        return products
    
    def get_by_barcode(self, barcode):
        """Barkoda göre ürün getir"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE barcode = ?', (barcode,))
        product = cursor.fetchone()
        conn.close()
        return product
    
    def get_critical_stock(self):
        """Kritik stok ürünlerini getir"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM products 
            WHERE stock <= min_stock AND status = "aktif"
            ORDER BY stock ASC
        ''')
        products = cursor.fetchall()
        conn.close()
        return products
    
    def add_product(self, data):
        """Yeni ürün ekle"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products 
            (barcode, name, category_id, purchase_price, sale_price, stock, min_stock, unit, supplier_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('barcode'),
            data.get('name'),
            data.get('category_id'),
            data.get('purchase_price'),
            data.get('sale_price'),
            data.get('stock', 0),
            data.get('min_stock', 10),
            data.get('unit', 'adet'),
            data.get('supplier_id')
        ))
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        return product_id

class SalesRepository(BaseRepository):
    """Satış işlemleri"""
    
    def get_daily_sales(self):
        """Günlük satışları getir"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(total_amount) as total FROM sales 
            WHERE DATE(sale_date) = DATE('now')
        ''')
        result = cursor.fetchone()
        conn.close()
        return result['total'] or 0
    
    def get_monthly_sales(self):
        """Aylık satışları getir"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(total_amount) as total FROM sales 
            WHERE strftime('%Y-%m', sale_date) = strftime('%Y-%m', 'now')
        ''')
        result = cursor.fetchone()
        conn.close()
        return result['total'] or 0

class CustomerRepository(BaseRepository):
    """Müşteri işlemleri"""
    
    def get_all(self):
        """Tüm müşterileri getir"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE status = "aktif"')
        customers = cursor.fetchall()
        conn.close()
        return customers
    
    def get_credit_balance(self):
        """Toplam veresiye bakiyesi getir"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(credit_balance) as total FROM customers
        ''')
        result = cursor.fetchone()
        conn.close()
        return result['total'] or 0

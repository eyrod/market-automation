"""Veritabanı yönetimi"""
import sqlite3
from pathlib import Path
from config.settings import DATABASE_PATH, DATABASE_BACKUP_PATH
import shutil
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.backup_path = DATABASE_BACKUP_PATH
        self.create_directories()
        self.init_database()
    
    def create_directories(self):
        """Gerekli dizinleri oluştur"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.backup_path.mkdir(parents=True, exist_ok=True)
    
    def get_connection(self):
        """Veritabanı bağlantısı al"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Veritabanını başlat ve tabloları oluştur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Kullanıcılar tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'kasiyer',
                email TEXT,
                phone TEXT,
                status TEXT DEFAULT 'aktif',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Kategoriler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ürünler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE,
                name TEXT NOT NULL,
                category_id INTEGER,
                purchase_price REAL NOT NULL,
                sale_price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                min_stock INTEGER DEFAULT 10,
                unit TEXT DEFAULT 'adet',
                supplier_id INTEGER,
                status TEXT DEFAULT 'aktif',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
            )
        ''')
        
        # Müşteriler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                credit_limit REAL DEFAULT 0,
                credit_balance REAL DEFAULT 0,
                status TEXT DEFAULT 'aktif',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Satışlar tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                customer_id INTEGER,
                total_amount REAL NOT NULL,
                payment_method TEXT,
                discount REAL DEFAULT 0,
                notes TEXT,
                status TEXT DEFAULT 'tamamlandi',
                receipt_number TEXT UNIQUE,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Satış Detayları tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        # Veresiye tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credit_sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                paid_amount REAL DEFAULT 0,
                remaining_amount REAL NOT NULL,
                due_date DATE,
                status TEXT DEFAULT 'beklemede',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Tedarikçiler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                tax_id TEXT,
                account_balance REAL DEFAULT 0,
                status TEXT DEFAULT 'aktif',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Kasa İşlemleri tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cash_register (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opening_date TIMESTAMP,
                closing_date TIMESTAMP,
                opening_amount REAL DEFAULT 0,
                closing_amount REAL DEFAULT 0,
                total_sales REAL DEFAULT 0,
                total_cash REAL DEFAULT 0,
                total_card REAL DEFAULT 0,
                user_id INTEGER,
                status TEXT DEFAULT 'acik',
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Trendyol GO Siparişleri tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trendyol_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT UNIQUE,
                customer_name TEXT,
                total_amount REAL,
                status TEXT DEFAULT 'beklemede',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Admin kullanıcısını oluştur (varsayılan)
        self.create_default_admin()
    
    def create_default_admin(self):
        """Varsayılan admin kullanıcısını oluştur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users WHERE username='admin'")
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO users (username, password, full_name, role, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', 'admin123', 'Sistem Yöneticisi', 'admin', 'aktif'))
                conn.commit()
        except:
            pass
        finally:
            conn.close()
    
    def backup_database(self):
        """Veritabanını yedekle"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_path / f'market_{timestamp}.db'
        shutil.copy2(str(self.db_path), str(backup_file))
        return backup_file
    
    def restore_database(self, backup_file):
        """Veritabanını geri yükle"""
        shutil.copy2(str(backup_file), str(self.db_path))

# Singleton instance
_db_manager = None

def get_db_manager():
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager

"""Uygulama ayarları"""
import os
from pathlib import Path

# Proje kök dizini
BASE_DIR = Path(__file__).resolve().parent.parent

# Veritabanı
DATABASE_PATH = BASE_DIR / 'data' / 'market.db'
DATABASE_BACKUP_PATH = BASE_DIR / 'backups'

# Raporlar
REPORTS_PATH = BASE_DIR / 'reports'

# Tema ayarları
THEME_LIGHT = 'light'
THEME_DARK = 'dark'
DEFAULT_THEME = THEME_LIGHT

# Dil
LANGUAGE = 'tr'  # Türkçe

# Uygulama bilgileri
APP_NAME = 'Market Otomasyon Sistemi'
APP_VERSION = '1.0.0'
APP_AUTHOR = 'Profesyonel Market Çözümleri'

# Kasa ayarları
CASH_REGISTER_NAME = 'Kasa 1'

# Stok uyarı limiteri
CRITICAL_STOCK_LIMIT = 10

# Veritabanı ayarları
DB_TYPE = 'sqlite'  # sqlite veya mysql
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'market_db'
DB_USER = 'root'
DB_PASSWORD = ''

# Yazıcı ayarları
PRINTER_ENABLED = True
PRINTER_NAME = 'Varsayılan Yazıcı'

# Trendyol GO
TREADYOL_GO_ENABLED = False
TREADYOL_GO_API_KEY = ''
TREADYOL_GO_API_URL = 'https://api.trendyol.com'

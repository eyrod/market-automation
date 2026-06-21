#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Market Otomasyon Sistemi
Professyionel market ve bakkallar için satış ve yönetim sistemi
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from database.db_manager import get_db_manager

def main():
    """Ana fonksiyon"""
    # Veritabanını başlat
    db = get_db_manager()
    
    # PyQt5 uygulamasını oluştur
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Ana pencereyi oluştur
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

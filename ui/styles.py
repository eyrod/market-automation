"""Tema ve stil tanımları"""

LIGHT_THEME = """
QMainWindow {background-color: #f5f5f5;}
QWidget {background-color: #f5f5f5; color: #333;}
QMenuBar {background-color: #fff; border-bottom: 1px solid #ddd;}
QMenuBar::item:selected {background-color: #e8f4f8;}
QMenu {background-color: #fff; color: #333;}
QMenu::item:selected {background-color: #e8f4f8;}
QPushButton {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}
QPushButton:hover {background-color: #0056b3;}
QPushButton:pressed {background-color: #003d82;}
QLineEdit, QTextEdit, QComboBox {
    background-color: white;
    color: #333;
    border: 1px solid #ddd;
    padding: 6px;
    border-radius: 4px;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 2px solid #007bff;
}
QTableWidget {
    background-color: white;
    color: #333;
    gridline-color: #ddd;
    border: 1px solid #ddd;
}
QTableWidget::item {padding: 5px;}
QHeaderView::section {
    background-color: #f8f9fa;
    color: #333;
    padding: 5px;
    border: 1px solid #ddd;
}
QLabel {color: #333;}
"""

DARK_THEME = """
QMainWindow {background-color: #2b2b2b;}
QWidget {background-color: #2b2b2b; color: #fff;}
QMenuBar {background-color: #1e1e1e; border-bottom: 1px solid #444;}
QMenuBar::item:selected {background-color: #444;}
QMenu {background-color: #1e1e1e; color: #fff;}
QMenu::item:selected {background-color: #444;}
QPushButton {
    background-color: #0d47a1;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}
QPushButton:hover {background-color: #1565c0;}
QPushButton:pressed {background-color: #0d47a1;}
QLineEdit, QTextEdit, QComboBox {
    background-color: #3a3a3a;
    color: #fff;
    border: 1px solid #555;
    padding: 6px;
    border-radius: 4px;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 2px solid #0d47a1;
}
QTableWidget {
    background-color: #3a3a3a;
    color: #fff;
    gridline-color: #555;
    border: 1px solid #555;
}
QTableWidget::item {padding: 5px;}
QHeaderView::section {
    background-color: #2b2b2b;
    color: #fff;
    padding: 5px;
    border: 1px solid #555;
}
QLabel {color: #fff;}
"""

def get_theme(theme_name):
    """Tema döndür"""
    if theme_name == 'dark':
        return DARK_THEME
    return LIGHT_THEME

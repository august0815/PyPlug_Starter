#test_plugin.py
from PyQt5.QtWidgets import QAction, QMessageBox, QMenu

class TestPlugin:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_label = "Gruss"

    def add_to_menu(self):
        # Menüleiste erweitern
        menubar = self.main_window.menuBar()
        greet_action = QAction(self.menu_label, self.main_window)
        greet_action.triggered.connect(self.show_greeting)
        menubar.addAction(greet_action)

    def remove_from_menu(self):
        # Menüeintrag entfernen
        menubar = self.main_window.menuBar()
        for action in menubar.actions():
            if action.text() == self.menu_label:
                menubar.removeAction(action)
                break

    def show_greeting(self):
        QMessageBox.information(self.main_window, "Gruss", "Gruß an dich!")

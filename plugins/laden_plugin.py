#laden_plugin.py
from PyQt5.QtWidgets import QAction, QMenu, QWidget, QVBoxLayout, QLabel, QPushButton

class LadenPlugin:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_label = "Laden"

    def add_to_menu(self):
        menubar = self.main_window.menuBar()
        # Suche nach dem Menü "Datei" anhand des Objekt-Namens
        datei_menu = menubar.findChild(QMenu, "menuDatei")
        if datei_menu:
            # Füge den Menüeintrag "Laden" hinzu
            self.laden_action = QAction(self.menu_label, self.main_window)
            self.laden_action.triggered.connect(self.show_popup)
            datei_menu.addAction(self.laden_action)
        else:
            print("Menü 'Datei' nicht gefunden.")

    def remove_from_menu(self):
        menubar = self.main_window.menuBar()
        datei_menu = menubar.findChild(QMenu, "menuDatei")
        if datei_menu:
            for action in datei_menu.actions():
                if action.text() == self.menu_label:
                    datei_menu.removeAction(action)
                    break

    def show_popup(self):
        # Erstelle ein Popup-Fenster mit der Nachricht und einem Close-Button.
        self.popup = QWidget()
        self.popup.setWindowTitle("Laden Popup")
        layout = QVBoxLayout(self.popup)
        label = QLabel("Gruß von Laden", self.popup)
        layout.addWidget(label)
        close_button = QPushButton("Close", self.popup)
        close_button.clicked.connect(self.popup.close)
        layout.addWidget(close_button)
        self.popup.setLayout(layout)
        self.popup.show()

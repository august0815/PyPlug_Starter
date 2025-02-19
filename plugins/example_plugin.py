#example_plugin.py
from PyQt5.QtWidgets import QAction, QMessageBox, QMenu

class ExamplePlugin:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_label = "Hallo sagen"

    def add_to_menu(self):
        menubar = self.main_window.menuBar()
        # Suche nach einem QMenu mit dem Objekt-Namen "Ansicht"
        display_menu = menubar.findChild(QMenu, "menueAnsicht")
        # Falls nicht vorhanden, erstelle das Menü und setze den Objekt-Namen
        if not display_menu:
            display_menu = menubar.addMenu("Ansicht")
            display_menu.setObjectName("Ansicht")
        say_hello_action = QAction(self.menu_label, self.main_window)
        say_hello_action.triggered.connect(self.say_hello)
        display_menu.addAction(say_hello_action)

    def remove_from_menu(self):
        menubar = self.main_window.menuBar()
        display_menu = menubar.findChild(QMenu, "Ansicht")
        if display_menu:
            for action in display_menu.actions():
                if action.text() == self.menu_label:
                    display_menu.removeAction(action)
                    break

    def say_hello(self):
        QMessageBox.information(self.main_window, "Hallo", "Hallo!")

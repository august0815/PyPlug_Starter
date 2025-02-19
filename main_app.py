#main_app.py
import sys
import importlib
import os
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QAction, QMessageBox, QLineEdit,
    QVBoxLayout, QLabel, QWidget, QPushButton, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import QSettings, QByteArray, QFile, Qt
from PyQt5.QtGui import QFont
from PyQt5 import uic

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Plugin-Verzeichnis ermitteln und in den Python-Pfad aufnehmen
        self.plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")
        if self.plugin_dir not in sys.path:
            sys.path.insert(0, self.plugin_dir)

        # UI-Initialisierung aus der .ui-Datei
        self.ui = uic.loadUi("ui.ui", self)

        # Plugin-Manager initialisieren (wird später erstellt)
        self.plugin_manager = None

        # Menü erstellen
        menubar = self.menuBar()
        self.display_menu = menubar.addMenu("Anzeigen")
        self.display_menu.setObjectName("Ansicht")
        help_menu = menubar.addMenu("Hilfe")

        # Plugin-Verwaltung (enthält aktuell geladene Plugins)
        self.plugins = {}

        # Plugin-Verwaltungsaktion
        manage_plugins_action = QAction("Plugin verwalten", self)
        help_menu.addAction(manage_plugins_action)
        manage_plugins_action.triggered.connect(self.manage_plugins)

        # Einstellungen laden, falls vorhanden
        self.loadSettings()

    def on_plugin_manager_destroyed(self, obj=None):
        self.plugin_manager = None

    def load_plugin(self, plugin_base_name):
        plugin_name = f"{plugin_base_name}_plugin"
        class_name = f"{plugin_base_name.capitalize()}Plugin"
        print(f"Loading plugin: {plugin_name}, class: {class_name}")  # Debug-Ausgabe
        try:
            plugin_module = importlib.import_module(plugin_name)
            plugin_class = getattr(plugin_module, class_name)
            plugin_instance = plugin_class(self)
            self.plugins[plugin_base_name] = plugin_instance
            plugin_instance.add_to_menu()
            if self.plugin_manager:
                self.plugin_manager.layout.addWidget(QLabel(f"Plugin '{plugin_name}' erfolgreich geladen."))
        except ModuleNotFoundError:
            QMessageBox.critical(self, "Fehler", f"Plugin '{plugin_name}' konnte nicht gefunden werden.")
            if self.plugin_manager:
                self.plugin_manager.layout.addWidget(QLabel(f"Fehler: Plugin '{plugin_name}' konnte nicht gefunden werden."))
        except AttributeError:
            QMessageBox.critical(self, "Fehler", f"Klasse '{class_name}' nicht im Plugin '{plugin_name}' gefunden.")
            if self.plugin_manager:
                self.plugin_manager.layout.addWidget(QLabel(f"Fehler: Klasse '{class_name}' nicht im Plugin '{plugin_name}' gefunden."))

    def unload_plugin(self, plugin_base_name):
        plugin_name = f"{plugin_base_name}_plugin"
        if plugin_base_name in self.plugins:
            plugin_instance = self.plugins.pop(plugin_base_name)
            plugin_instance.remove_from_menu()
            if self.plugin_manager:
                self.plugin_manager.layout.addWidget(QLabel(f"Plugin '{plugin_name}' erfolgreich entfernt."))
        else:
            QMessageBox.critical(self, "Fehler", f"Plugin '{plugin_name}' ist nicht geladen.")
            if self.plugin_manager:
                self.plugin_manager.layout.addWidget(QLabel(f"Fehler: Plugin '{plugin_name}' ist nicht geladen."))

    def load_plugin_and_close(self, plugin_base_name):
        self.load_plugin(plugin_base_name)
        if self.plugin_manager is not None:
            self.plugin_manager.close()

    def unload_plugin_and_close(self, plugin_base_name):
        self.unload_plugin(plugin_base_name)
        if self.plugin_manager is not None:
            self.plugin_manager.close()

    def manage_plugins(self):
        if self.plugin_manager is not None:
            try:
                if not self.plugin_manager.isVisible():
                    self.plugin_manager = None
            except RuntimeError:
                self.plugin_manager = None

        if self.plugin_manager is None:
            self.plugin_manager = QWidget()
            self.plugin_manager.setAttribute(Qt.WA_DeleteOnClose)
            self.plugin_manager.setWindowTitle("Plugin verwalten")
            self.plugin_manager.layout = QVBoxLayout(self.plugin_manager)
            self.plugin_manager.setLayout(self.plugin_manager.layout)
            self.plugin_manager.destroyed.connect(self.on_plugin_manager_destroyed)

        layout = self.plugin_manager.layout
        while layout.count():
            item = layout.takeAt(0)
            widget_item = item.widget()
            if widget_item is not None:
                widget_item.deleteLater()

        layout.addWidget(QLabel("Verfügbare Plugins:"))

        self.available_plugins_list = QListWidget()
        if os.path.isdir(self.plugin_dir):
            for filename in os.listdir(self.plugin_dir):
                if filename.endswith("_plugin.py"):
                    base_name = filename[:-len("_plugin.py")]
                    item = QListWidgetItem(base_name)
                    if base_name in self.plugins:
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)
                    self.available_plugins_list.addItem(item)
        layout.addWidget(self.available_plugins_list)

        layout.addWidget(QLabel("Plugin-Name:"))
        self.plugin_name_entry = QLineEdit()
        layout.addWidget(self.plugin_name_entry)

        self.available_plugins_list.itemSelectionChanged.connect(self.update_plugin_name_from_selection)

        load_button = QPushButton("Laden")
        load_button.clicked.connect(lambda: self.load_plugin_and_close(self.plugin_name_entry.text()))
        layout.addWidget(load_button)

        unload_button = QPushButton("Entfernen")
        unload_button.clicked.connect(lambda: self.unload_plugin_and_close(self.plugin_name_entry.text()))
        layout.addWidget(unload_button)

        self.plugin_manager.show()
        self.plugin_manager.raise_()
        self.plugin_manager.activateWindow()

    def update_plugin_name_from_selection(self):
        selected_items = self.available_plugins_list.selectedItems()
        if selected_items:
            self.plugin_name_entry.setText(selected_items[0].text())

    def closeEvent(self, event):
        self.saveSettings()
        event.accept()

    def loadSettings(self):
        if QFile.exists("config.conf"):
            settings = QSettings("config.conf", QSettings.IniFormat)
            geometry = settings.value("window/geometry", QByteArray())
            if geometry:
                self.restoreGeometry(geometry)
            state = settings.value("window/state", QByteArray())
            if state:
                self.restoreState(state)

            plugin_count = settings.beginReadArray("plugins")
            for i in range(plugin_count):
                settings.setArrayIndex(i)
                plugin_base_name = settings.value("name")
                self.load_plugin(plugin_base_name)
            settings.endArray()

            defaultSizes = [self.width() * 0.1, self.width() * 0.9]
            splitterSizes = settings.value("splitter/sizes", defaultSizes)
            splitterSizes = [int(size) for size in splitterSizes]
            self.ui.splitter.setSizes(splitterSizes)
        else:
            print("Keine Konfigurationsdatei gefunden. Starte mit Standard-UI.")
            self.load_plugin("example")

    def saveSettings(self):
        settings = QSettings("config.conf", QSettings.IniFormat)
        settings.setValue("window/geometry", self.saveGeometry())
        settings.setValue("window/state", self.saveState())

        settings.beginWriteArray("plugins")
        for i, plugin_base_name in enumerate(self.plugins):
            settings.setArrayIndex(i)
            settings.setValue("name", plugin_base_name)
        settings.endArray()

        settings.setValue("splitter/sizes", self.ui.splitter.sizes())
        settings.sync()

        if settings.status() != QSettings.NoError:
            self.statusBar().showMessage("Fehler beim Speichern der Einstellungen!", 5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

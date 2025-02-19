# Plugin Template for PyQt5 Applications

Dieses Repository enthält ein Grundgerüst für eine Python-Anwendung, die mithilfe von PyQt5 eine modulare Plugin-Struktur implementiert. Die Anwendung ermöglicht es, zur Laufzeit Plugins zu laden und zu entfernen, und bietet eine einfache Plugin-Verwaltung über ein eigenes Fenster.

## Inhalt

- [Überblick](#überblick)
- [Dateistruktur](#dateistruktur)
- [Funktionsweise der Hauptanwendung](#funktionsweise-der-hauptanwendung)
- [Plugin-Konzept und Namenskonvention](#plugin-konzept-und-namenskonvention)
- [Plugins im Detail](#plugins-im-detail)
- [Verwendung der Anwendung](#verwendung-der-anwendung)
- [Eigene Plugins erstellen und erweitern](#eigene-plugins-erstellen-und-erweitern)
- [Beispiel: ExtendPlugin](#beispiel-extendplugin)
- [Lizenz und Hinweise](#lizenz-und-hinweise)

## Überblick

Das System basiert auf einer PyQt5-Anwendung, die:
- Eine Benutzeroberfläche (UI) aus einer Qt Designer-Datei (`ui.ui`) lädt.
- Ein Hauptmenü mit mehreren Bereichen (z. B. "Ansicht", "Datei", "Hilfe") bereitstellt.
- Plugins dynamisch aus einem speziellen Verzeichnis (`plugins`) importiert und in die Anwendung eingebunden werden.
- Über ein Plugin-Verwaltungsfenster (unter "Hilfe") die Möglichkeit bietet, Plugins zu laden und zu entfernen.
- Einstellungen wie Fenstergeometrie, Menüzustand und geladene Plugins in einer Konfigurationsdatei (`config.conf`) speichert.

## Dateistruktur

- **main_app.py**  
  Hauptanwendung, die das Hauptfenster, die Plugin-Verwaltung und das Laden/Entfernen von Plugins implementiert.

- **ui.ui**  
  Eine Qt Designer-Datei, die das Layout und die Widgets der Benutzeroberfläche definiert.

- **plugins/**  
  Dieser Ordner enthält alle Plugin-Dateien. Jede Plugin-Datei muss dem Namensmuster `{plugin_base_name}_plugin.py` entsprechen.

  Beispiel-Plugins:
  - **example_plugin.py**  
    Fügt einen Menüeintrag "Hallo sagen" im Menü "Ansicht" hinzu.
  - **laden_plugin.py**  
    Fügt einen Menüeintrag "Laden" im Menü "Datei" hinzu und öffnet ein Popup.
  - **test_plugin.py**  
    Fügt einen Menüeintrag "Gruss" direkt in die Menüleiste ein.
  - **extend_plugin.py** (Beispiel unten)  
    Fügt einen Menüeintrag "Beenden und Speichern" im Menü "Datei" hinzu, speichert Daten und beendet die Anwendung.

## Funktionsweise der Hauptanwendung

- **Dynamisches Laden von Plugins:**  
  Beim Start wird das Verzeichnis `plugins` zum Python-Pfad hinzugefügt. Plugins werden anhand ihres Dateinamens und Klassennamens (z. B. `ExamplePlugin` aus `example_plugin.py`) dynamisch importiert und mittels ihrer `add_to_menu()`-Methode in die Anwendung eingebunden.

- **Plugin-Verwaltung:**  
  Über den Menüpunkt „Plugin verwalten“ im „Hilfe“-Menü wird ein Verwaltungsfenster geöffnet. Hier kannst Du:
  - Eine Liste aller im `plugins`-Ordner verfügbaren Plugins einsehen.
  - Ein Plugin auswählen oder per Texteingabe angeben.
  - Plugins laden oder entfernen, was unmittelbar in der Menüleiste sichtbar wird.

- **Einstellungen speichern und laden:**  
  Über `QSettings` werden Fensterzustand, Menükonfiguration und geladene Plugins in einer Datei (`config.conf`) persistiert. Dadurch wird der zuletzt benutzte Zustand beim Neustart der Anwendung wiederhergestellt.

## Plugin-Konzept und Namenskonvention

Damit ein Plugin korrekt eingebunden werden kann, müssen folgende Anforderungen erfüllt sein:

1. **Dateiname:**  
   Das Plugin muss im Ordner `plugins` liegen und dem Muster `{plugin_base_name}_plugin.py` folgen.  
   Beispiel: `example_plugin.py` für das Plugin „example“.

2. **Klassenname:**  
   Innerhalb der Datei muss eine Klasse mit dem Namen `{PluginBaseName}Plugin` definiert sein.  
   Beispiel: Für `example_plugin.py` lautet der Klassenname `ExamplePlugin`.

3. **Erforderliche Methoden:**  
   - `add_to_menu()`: Diese Methode fügt Menüeinträge oder weitere UI-Komponenten zur Hauptanwendung hinzu.
   - `remove_from_menu()`: Diese Methode entfernt alle durch das Plugin hinzugefügten UI-Elemente wieder.

## Plugins im Detail

- **ExamplePlugin (example_plugin.py):**  
  Fügt einen Menüeintrag „Hallo sagen“ zum Menü „Ansicht“ hinzu. Beim Auslösen zeigt es ein Informations-Popup mit der Nachricht „Hallo!“ an.

- **LadenPlugin (laden_plugin.py):**  
  Sucht das Menü „Datei“ anhand des Objekt-Namens „menuDatei“ und fügt einen Menüeintrag „Laden“ hinzu. Beim Klick wird ein Popup mit einer Grußnachricht geöffnet.

- **TestPlugin (test_plugin.py):**  
  Fügt einen einfachen Menüeintrag „Gruss“ direkt in die Menüleiste ein, der beim Auslösen ein Popup mit der Nachricht „Gruß an dich!“ anzeigt.

## Verwendung der Anwendung

1. **Installation und Voraussetzungen:**  
   - Python (empfohlen: 3.x) muss installiert sein.
   - PyQt5 installieren:  
     ```bash
     pip install PyQt5
     ```

2. **Starten der Anwendung:**  
   Führe in der Kommandozeile aus:
   ```bash
   python main_app.py

Beim ersten Start wird standardmäßig das example_plugin geladen, sofern keine Konfigurationsdatei vorhanden ist.

    Plugins verwalten:
        Gehe im Menü auf „Hilfe“ und wähle „Plugin verwalten“.
        Im erscheinenden Fenster siehst Du alle im Ordner plugins verfügbaren Plugins.
        Wähle ein Plugin aus oder gib den Plugin-Namen manuell ein.
        Mit den Buttons „Laden“ und „Entfernen“ kannst Du das jeweilige Plugin aktivieren oder deaktivieren.

    Einstellungen:
    Beim Schließen der Anwendung werden die Fenstergeometrie, der Zustand der Menüs und die geladenen Plugins in config.conf gespeichert und beim nächsten Start wiederhergestellt.

Eigene Plugins erstellen und erweitern

Um die Funktionalität der Anwendung zu erweitern, kannst Du eigene Plugins erstellen:

    Neues Plugin erstellen:
    Erstelle im Ordner plugins eine neue Python-Datei, z. B. mein_plugin.py.

    Namenskonvention beachten:
    Der Dateiname muss {plugin_base_name}_plugin.py lauten und die enthaltene Klasse muss MeinPlugin heißen (erste Buchstabe groß, Suffix „Plugin“).

    Erforderliche Methoden implementieren:
    Implementiere in Deiner Klasse mindestens:
        add_to_menu(): Fügt Dein Plugin-spezifisches UI-Element (z. B. einen Menüeintrag) hinzu.
        remove_from_menu(): Entfernt das hinzugefügte UI-Element wieder.

    Integration:
    Beim nächsten Start der Anwendung oder über die Plugin-Verwaltung erscheint Dein Plugin in der Liste der verfügbaren Plugins. Lade es, um die neuen Funktionen zu nutzen.

Beispiel: ExtendPlugin

Hier folgt ein Beispiel, wie Du ein Plugin namens ExtendPlugin erstellen kannst, das im Menü „Datei“ einen Menüeintrag „Beenden und Speichern“ hinzufügt. Beim Auslösen des Eintrags wird:

    Die Methode saveSettings() des Hauptfensters aufgerufen, um alle Daten zu speichern.
    Ein Popup mit der Nachricht „Danke für das Benutzen“ angezeigt.
    Die Anwendung beendet.

Speichere den folgenden Code in der Datei extend_plugin.py im Ordner plugins:

from PyQt5.QtWidgets import QAction, QMessageBox, QMenu

class ExtendPlugin:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_label = "Beenden und Speichern"

    def add_to_menu(self):
        menubar = self.main_window.menuBar()
        # Suche nach dem "Datei"-Menü anhand des Objekt-Namens
        datei_menu = menubar.findChild(QMenu, "menuDatei")
        if datei_menu:
            self.extend_action = QAction(self.menu_label, self.main_window)
            self.extend_action.triggered.connect(self.exit_program)
            datei_menu.addAction(self.extend_action)
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

    def exit_program(self):
        # Speichere alle Einstellungen/Daten
        try:
            self.main_window.saveSettings()
        except Exception as e:
            print("Fehler beim Speichern:", e)
        # Zeige Popup mit der Nachricht
        QMessageBox.information(self.main_window, "Beenden", "Danke für das Benutzen")
        # Schließe das Programm
        self.main_window.close()

Lizenz und Hinweise

Bitte beachte, dass diese Vorlage unter eigenem Ermessen verwendet werden kann. Eine abschließende Prüfung der Namensgebung (insbesondere in Bezug auf Markenschutz und bereits bestehende Projekte) sowie eine gründliche Testphase der Plugins ist ratsam.

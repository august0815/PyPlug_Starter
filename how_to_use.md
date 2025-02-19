Hier folgt eine ausführliche Anleitung, die erklärt, wie das Plugin-Grundgerüst funktioniert, wie die einzelnen Dateien zusammenwirken und wie Du das Programm nutzen sowie um eigene Plugins erweitern kannst.

---

## 1. Überblick und Dateistruktur

Das System besteht im Wesentlichen aus folgenden Dateien:

- **main_app.py**  
  Enthält die Hauptanwendung, die ein Hauptfenster mit einer über ein .ui-File geladenen Benutzeroberfläche erstellt. Sie implementiert das Laden und Entfernen von Plugins, speichert die Anwendungs-Einstellungen und bietet über ein extra Fenster eine einfache Plugin-Verwaltung .

- **ui.ui**  
  Eine Qt Designer-Datei, die das Layout und die Widgets der Hauptanwendung definiert. Sie enthält beispielsweise einen Splitter, dessen Größe gespeichert und wiederhergestellt wird.

- **example_plugin.py**  
  Ein Beispiel-Plugin, das einen Menüeintrag „Hallo sagen“ in einem Menü (hier „Ansicht“) einfügt. Beim Auslösen wird eine Nachricht mit „Hallo!“ angezeigt .

- **laden_plugin.py**  
  Ein weiteres Plugin, das einen Menüpunkt „Laden“ im Menü „Datei“ (identifiziert über den Objektnamen „menuDatei“) hinzufügt. Dieser Menüpunkt öffnet ein Popup-Fenster mit einer Begrüßung .

- **test_plugin.py**  
  Ein drittes Plugin, das einen direkten Menüeintrag mit der Beschriftung „Gruss“ zur Menüleiste hinzufügt. Wird dieser Eintrag aktiviert, erscheint ein Dialog mit einer Grußbotschaft .

---

## 2. Funktionsweise der Hauptanwendung (main_app.py)

Beim Start der Anwendung wird das Hauptfenster aus der UI-Datei geladen. Folgende Punkte sind dabei zentral:

- **Plugin-Verzeichnis und dynamisches Laden:**  
  Das Verzeichnis `plugins` (relativ zum Hauptapplikationsordner) wird in den Python-Pfad eingefügt. Dort werden alle Dateien gesucht, deren Name auf „_plugin.py“ endet.  
  In der Funktion `load_plugin()` wird der Plugin-Name aus dem Dateinamen abgeleitet. Es wird versucht, das Modul zu importieren und eine Klasse zu instanziieren, die den Namen `PluginBaseNamePlugin` trägt. Anschließend wird die Methode `add_to_menu()` des Plugins aufgerufen, sodass das Plugin seine Funktionalität (z. B. einen neuen Menüeintrag) in die Anwendung integriert.

- **Plugin-Verwaltung:**  
  Über den Menüpunkt „Plugin verwalten“ (unter „Hilfe“) öffnet sich ein separates Fenster, das in `manage_plugins()` erstellt wird. Hier findest Du:
  - Eine Liste aller im `plugins`-Verzeichnis vorhandenen Plugins.
  - Ein Eingabefeld, das den Namen des ausgewählten Plugins übernimmt.
  - Zwei Buttons: „Laden“ (um ein Plugin zu aktivieren) und „Entfernen“ (um ein Plugin wieder zu deaktivieren).
  
  So kannst Du zur Laufzeit Plugins hinzufügen oder entfernen.

- **Einstellungen speichern und laden:**  
  Mithilfe von `QSettings` wird die Fenstergeometrie, der Zustand der Menüs und auch die aktuell geladenen Plugins in einer Konfigurationsdatei (`config.conf`) gespeichert. So wird beim nächsten Start der zuletzt verwendete Zustand wiederhergestellt.

---

## 3. Plugin-Struktur und Namenskonvention

Damit ein Plugin korrekt in das System eingebunden werden kann, muss es einige Anforderungen erfüllen:

- **Dateiname:**  
  Das Plugin muss in einer Datei liegen, deren Name dem Muster `{plugin_base_name}_plugin.py` entspricht.  
  Beispiel: Für das Plugin „example“ lautet der Dateiname `example_plugin.py`.

- **Klassenname:**  
  Innerhalb der Datei muss eine Klasse mit dem Namen `{PluginBaseName}Plugin` definiert sein – also mit erstem Großbuchstaben und dem Suffix „Plugin“.  
  Beispiel: Für `example_plugin.py` muss die Klasse `ExamplePlugin` heißen.

- **Erforderliche Methoden:**  
  Jedes Plugin sollte mindestens zwei Methoden enthalten:
  - `add_to_menu()`: Wird beim Laden des Plugins aufgerufen und fügt das Plugin einen oder mehrere Menüeinträge hinzu.
  - `remove_from_menu()`: Ermöglicht das Entfernen des Plugin-bezogenen Menüeintrags wieder aus der Anwendung.
  
  Optional können weitere Funktionen (z. B. Ereignisbehandlung, Fensteröffnen) definiert werden.

---

## 4. Details zu den Beispiel-Plugins

- **ExamplePlugin (example_plugin.py):**  
  Dieses Plugin sucht in der Menüleiste nach einem Menü mit dem Namen „Ansicht“. Wird keines gefunden, wird es neu erstellt. Der Menüeintrag „Hallo sagen“ wird hinzugefügt, und bei Klick erscheint ein Dialog mit „Hallo!“.

- **LadenPlugin (laden_plugin.py):**  
  Hier wird gezielt das Menü „Datei“ (über den Objektnamen „menuDatei“) angesprochen. Wird der Menüpunkt „Laden“ aktiviert, öffnet sich ein kleines Popup-Fenster mit einer Begrüßung und einem Button zum Schließen.

- **TestPlugin (test_plugin.py):**  
  Fügt einen direkten Menüeintrag „Gruss“ in die Hauptmenüleiste ein. Beim Auslösen wird ein Dialog mit der Nachricht „Gruß an dich!“ angezeigt.

---

## 5. So nutzt Du das Programm

1. **Installation und Voraussetzungen:**  
   - Stelle sicher, dass Python (z. B. 3.x) installiert ist.
   - Installiere PyQt5, z. B. über `pip install PyQt5`.

2. **Start der Anwendung:**  
   - Starte die Anwendung mit:  
     `python main_app.py`  
   - Beim ersten Start wird standardmäßig das `example_plugin` geladen, sofern keine `config.conf` existiert.

3. **Plugins verwalten:**  
   - Klicke in der Menüleiste auf „Hilfe“ und wähle dort „Plugin verwalten“.
   - Im erscheinenden Fenster siehst Du eine Liste aller Plugins, die im `plugins`-Verzeichnis vorhanden sind.
   - Wähle einen Plugin-Namen aus oder gib ihn manuell in das Textfeld ein.
   - Klicke auf „Laden“, um das Plugin zu aktivieren, oder auf „Entfernen“, um es wieder zu deaktivieren.
   - Die Aktionen der Plugins (z. B. neue Menüeinträge) erscheinen unmittelbar in der Hauptmenüleiste.

4. **Automatisches Speichern:**  
   - Beim Schließen der Anwendung werden Fensterzustand, Geometrie und die Liste der geladenen Plugins in der `config.conf` gesichert.  
   - Beim nächsten Start werden diese Einstellungen automatisch wiederhergestellt.

---

## 6. Eigene Plugins erstellen und erweitern

Um das Programm zu erweitern, kannst Du eigene Plugins hinzufügen. So gehst Du vor:

1. **Neues Plugin erstellen:**  
   - Lege im Ordner `plugins` eine neue Python-Datei an, z. B. `mein_plugin.py`.

2. **Namenskonvention beachten:**  
   - Der Klassenname muss in diesem Fall `MeinPlugin` lauten.

3. **Methoden implementieren:**  
   - Implementiere in Deiner Klasse mindestens die Methoden `add_to_menu()` und `remove_from_menu()`.  
   - In `add_to_menu()` fügst Du beispielsweise einen neuen Menüeintrag hinzu oder öffnest ein neues Fenster.  
   - In `remove_from_menu()` sorgst Du dafür, dass der von Dir hinzugefügte Menüeintrag wieder entfernt wird, wenn das Plugin deaktiviert wird.

4. **Integration in das System:**  
   - Starte die Anwendung. Dein neues Plugin sollte nun in der Plugin-Verwaltung als verfügbar erscheinen.
   - Lade es über die Verwaltung oder füge es in die Konfiguration ein, sodass es automatisch geladen wird.

5. **Fehlerbehandlung:**  
   - Achte darauf, dass Dein Plugin keine schwerwiegenden Fehler wirft, da sonst die dynamische Einbindung scheitern kann. Die Anwendung informiert Dich in diesem Fall über Fehlermeldungen (z. B. fehlendes Modul oder Attribut).

---

## 7. Zusammenfassung

- **Grundfunktionalität:**  
  Die Hauptanwendung lädt beim Start eine UI, richtet Menüs ein und bietet ein Plugin-Verwaltungsfenster.  
- **Plugins:**  
  Werden dynamisch aus dem Ordner `plugins` geladen und müssen einer festen Namens- und Strukturkonvention folgen.  
- **Erweiterung:**  
  Du kannst eigene Plugins erstellen, indem Du neue Dateien im `plugins`-Ordner ablegst, die die Methoden `add_to_menu()` und `remove_from_menu()` implementieren.  
- **Speicherung:**  
  Einstellungen und geladene Plugins werden in `config.conf` gespeichert, sodass beim Neustart der letzte Zustand wiederhergestellt wird.

Diese modulare Struktur erlaubt es Dir, das Programm schrittweise zu erweitern und eigene Funktionalitäten hinzuzufügen – sei es durch neue Menüeinträge, Dialoge oder komplexere Interaktionen.

Viel Erfolg beim Anpassen und Erweitern Deines Plugin-basierten Programms!

# HAWK SOSE2020 
Repository für das Wall-A-001-Projekt.

Dieses Projekt basiert auf dem gym-miniworld Project von maximecb : https://github.com/maximecb/gym-miniworld
Es wurde auf die Bedürfnisse für die Verwendung des Wall-A Projekte im Fach Software Engineering angepasst.

Um gym-miniworld zu verwenden ist die OpenAI Gym Umgebung notwendig, außerdem wird zur Installation Git benötigt.
Die Installation wird unter Verwendung des Anaconda Navigators beschrieben.

## Installation OpenAI Gym:
Im Ordner "site-packages" der Pythonumgebung (Pfad: ...\anaconda3\envs\[Env-Name]\Lib\site-packages) muss das OpenAI Gym eingefügt werden.
Hierzu müssen in dem entsprechendem Ordner folgende Befehle ausgeführt werden:
```
git clone https://github.com/openai/gym
cd gym
pip install -e .
```

## Installation des Wall-A Projekts:
Innerhalb des OpenAI Gym Ordners muss nun in das Verzeichnis envs (Pfad: ...\anaconda3\envs\[Env-Name]\gym\gym\envs) navigiert werden.
Hier wird nun das Wall-A Projekt Repository erstellt:
```
git clone https://github.com/Wall-A-001/Hawk20.git
cd gym-miniworld
pip install -e .
```

## ALternative Installation
Falls die direkte Installation des Projektrepositories nicht funktioniert hat, kann alternativ zunächst das originale
miniworld Environment installiert werden:
```
git clone https://github.com/maximecb/gym-miniworld.git
cd gym-miniworld
pip install -e .
```

Anschließend müssen die Dateien mit dennen aus dem Wall-A Projekt überschrieben werden.

## Funktionsprüfung    
Nun sollte das Wall-A Projekt installiert und funktionsfähig sein.

Um die Installation zu prüfen, kann im Ordner Env\Hawk20 das Programm 
```
python manual_control.py
```
ausgeführt werden. Hier sollte sich eine Fenster öffnen, in welchem ein Labyrinth aus der Vogelperspektive zu sehen ist.
Die Spielfigur (rotes Dreieck) kann mit Hilfe der Pfeiltasten zu den roten Quadraten navigiert werden.
Steht die Spielfigur vor einem Quadrat kann dieses mit der "p" Taste aufgehoben werden.
Ziel des Spiels ist es alle Kisten im Level aufzuheben.

Eine Anleitung zur Nutzung des KI Lernalgorithmus folgt in Kürze.

Stand: 25.06.2020

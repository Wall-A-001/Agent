# HAWK SOSE2020.
Repository für das Wall-A-001-Projekt
Dieses Projekt basiert auf dem gym-miniworld Projekt von maximecb : https://github.com/maximecb/gym-miniworld
Es wurde auf die Bedürfnisse für die Verwendung des Wall-A Projekts im Fach Software Engineering angepasst.
Um gym-miniworld zu verwenden, ist die OpenAI Gym Umgebung notwendig. Außerdem wird zur Installation Git benötigt.
Die Installation wird unter Verwendung des Anaconda Navigators beschrieben.

## Voraussetzungen für Installation
Die verwendete Software besitzt eine Reihe von Abhängigkeiten gegenüber anderen Python-Modulen und Paketen. Diese werden durch die weiter unten beschriebene Installationsanleitung automatisch hinzugefügt. Sollten Probleme diesbezüglich auftauchen, sind hier nochmal alle relevanten Abhängigkeiten aufgelistet:
- Python: >=3.5
- OpenAI Gym: >=0.9.0
- numpy: >=1.10.4
- pyglet: >=1.4.0, <=1.5.0
- cloudpickle: >=1.2.0, <1.4.0
- scipy
- enum34: ~=1.1.6

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

## Alternative Installation
Falls die direkte Installation des Projektrepositories nicht funktioniert hat, kann alternativ zunächst das originale
miniworld Environment installiert werden:
```
git clone https://github.com/maximecb/gym-miniworld.git
cd gym-miniworld
pip install -e .
```
Anschließend müssen die Dateien mit denen aus dem Wall-A Projekt überschrieben werden.

## Funktionsprüfung    
Nun sollte das Wall-A Projekt installiert und funktionsfähig sein.
Um die Installation zu prüfen, kann im Ordner Env\Hawk20 das Programm
```
python manual_control.py
```
ausgeführt werden. Hier sollte sich ein Fenster öffnen, in welchem ein Labyrinth aus der Vogelperspektive zu sehen ist.
Die Spielfigur (rotes Dreieck) kann mit Hilfe der Pfeiltasten zu den roten Quadraten navigiert werden.
Steht die Spielfigur vor einem Quadrat kann dieses mit der "p" Taste aufgehoben werden.
Ziel des Spiels ist es, alle Kisten im Level aufzuheben.

## Installation von Tensorflow
Bei TensorFlow handelt es sich um eine plattformunabhängige Programmbibliothek unter Open-Source-Lizenz, die sich für Aufgaben rund um maschinelles Lernen und Künstliche Intelligenz (KI) einsetzen lässt.
```
conda install -c conda-forge tensorflow
```
Diese Installation erfordert die Nutzung einer Anaconda Umgebung. Als Alternative bietet sich die Installation mit pip und einer spezifischen Version von TensorFlow für Ihre Plattform an:
```
pip install tensorflow==1.6
```
## Installation von Numpy Bibliothek 
NumPy ist eine Programmbibliothek für die Programmiersprache Python, die eine einfache Handhabung von Vektoren,
Matrizen oder generell großen mehrdimensionalen Arrays ermöglicht. Neben den Datenstrukturen bietet NumPy
auch effizient implementierte Funktionen für numerische Berechnungen an.
```
pip install numpy
```
## Installation von Keras 
Keras  ist eine Open Source Deep-Learning-Bibliothek, geschrieben in Python und  bietet eine einheitliche Schnittstelle für verschiedene Backends, darunter TensorFlow, Microsoft Cognitive Toolkit (vormals CNTK) und Theano. Das Ziel von Keras ist es, die Anwendung dieser Bibliotheken so einsteiger- und nutzerfreundlich wie möglich zu machen.
```
conda install -c conda-forge keras
``` 

## Main Funktion starten 
Um das Programm starten zu können, muss sich der Benutzer zunächst vergewissern, dass alle genannten Bibliotheken installiert und funktionsfähig sind. Dann muss der Benutzer mit dem Terminal zum Ordner "Hawk20-master" navigieren. Von diesem Ordner  kann das Programm mit folgendem Befehl gestartet werden:
```
python Main.py
``` 
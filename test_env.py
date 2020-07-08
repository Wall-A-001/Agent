#   Unittest für das Environment
#   08.07.2020

import unittest
import random
import gym
import gym_miniworld
import numpy as np
import math

class simpleTest(unittest.TestCase):
    # SetUp Methode wird einmalig zu Begin des Tests ausgeführt
    def setUp(self):
       self.env = gym.make('MiniWorld-HAWKMaze-v0')                         # zuerst wird das HawkMaze Environment erstellt
       name = self.shortDescription()
       if name == "Empty":                                                  # wird die setUp Methode mit "Empty" aufgerufen,
           self.env.anzahl_objs = 0                                         # wird die Anzahl der Boxen auf 0 gesetzt
       if name == "Boxes":                                                  # wird die setUp Methode mit "Empty" aufgerufen,
           self.env.anzahl_objs = 10                                        # wird die Anzahl der Boxen auf 10 gesetzt
       self.env.reset()                                                     # anschließend wird das Environment neugestartet (zur Initialisierung)

    # TearDown Methode wird einmalig zu Ende des Tests ausgeführt
    def tearDown(self):
        self.env.close()                                                    # Nachdem der Test beendet wurde, wird das Environment wieder geschlossen

#---------------------------------------------------Test Durchläufe-----------------------------------------------------

    # 1.Test: Prüfung ob der Agent nur 45° Winkel einnimmt
    def testWinkel(self):
        """Empty"""
        theta = 0                                                           # die Variable "theta" wird mit 0 initalisiert
        for i in range (10):                                                # es werden 10 Durchläufe ausgeführt
            obs, reward, done, info = self.env.step(random.randint(0,4))    # ein zufälliger Schritt wird ausgeführt
            theta = self.env.agent.dir *180 /math.pi                        # der Winkel des Agents nach dem Schritt (in Grad) wird in die Variable "theta" geschrieben
            mod = theta % 45                                                # Mit dem Modulo Operator wird geprüft ob der Winkel restlos durch 45° teilbar ist.

        self.assertEqual(mod, 0)                                            # ist das Ergebnis der Modulo Operation 0, wurde der Test bestanden.

    # 2.Test: Prüfen, ob der Schrittzaehler korrekt funktioniert
    def testSchrittZaehler(self):
        """Empty"""
        for j in range (100):                                               # es werden 100 Druchläufe ausgeführt
            obs, reward, done, info = self.env.step(random.randint(0, 4))   # ein zufälliger Schritt wird ausgeführt

        self.assertEqual(self.env.step_count, 100)                          # ist der Schrittzäehler nach 100 zufälligen Schritten gleich 100, wurde der Test bestanden


if __name__ == '__main__':                                                  # Durch diesen Befehl kann der Unittest direkt über das CMD Terminal aufgerufen werden
    unittest.main()
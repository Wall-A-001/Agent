#   Unittest für das Environment
#   08.07.2020

import unittest
import random
import gym
from gym_miniworld.entity import Box, Agent
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
           self.env.reset()                                                 # anschließend wird das Environment neugestartet (zur Initialisierung)

       if name == "Boxes":                                                  # wird die setUp Methode mit "Empty" aufgerufen,
           self.env.anzahl_objs = 10                                        # wird die Anzahl der Boxen auf 10 gesetzt
           self.env.reset()                                                 # anschließend wird das Environment neugestartet (zur Initialisierung)

       if name == "Place_Agent_on_defined_Position":                        # wird die setUp Methode mit "Place_Agent_on_defined_Position" aufgerufen,
           self.env.reset()                                                 # das Environment wird neu gestartet
           self.env.room_size = 100                                         # Der Raum wird auf eine Größe von 100x100 gesetzt, damit es nicht zu Kollisionen kommt
           self.env.place_agent(dir=0, min_x=10 , max_x=10 , min_z=10 , max_z=10)
           self.env.place_entity(ent=Box(color=np.array([1.0, 0.0, 0.0]), size=0.9),dir=0, min_x=15 , max_x=15 , min_z=10 , max_z=10)

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
            mod = theta % self.env.phi_agent                                # Mit dem Modulo Operator wird geprüft ob der Winkel restlos durch 45° teilbar ist.

        self.assertEqual(mod, 0)                                            # ist das Ergebnis der Modulo Operation 0, wurde der Test bestanden.

    # 2.Test: Prüfen, ob der Schrittzaehler korrekt funktioniert
    def testSchrittZaehler(self):
        """Empty"""
        for j in range (100):                                               # es werden 100 Druchläufe ausgeführt
            obs, reward, done, info = self.env.step(random.randint(0, 4))   # ein zufälliger Schritt wird ausgeführt

        self.assertEqual(self.env.step_count, 100)                          # ist der Schrittzäehler nach 100 zufälligen Schritten gleich 100, wurde der Test bestanden

    # 3.Test: Prüfen ob der Reward korrekt berechnet wird
    def testReward(self):
        """Place_Agent_on_defined_Position"""
        for k in range (10):                                                # es werden 10 Druchläufe ausgeführt
            obs, reward, done, info = self.env.step(env.actions.move_forward)   # der Agent führt einen Schritt geradeaus durch
        obs, reward, done, info = self.env.step(env.actions.pickup)         # nach den 10 Schritten wird eine Pickup Aktion ausgeführt

        self.assertEqual(self.env.reward, 0.9926)                           # wenn der Reward dem errechneten Wert 0,99267 entspricht, wurde der Test bestanden


if __name__ == '__main__':                                                  # Durch diesen Befehl kann der Unittest direkt über das CMD Terminal aufgerufen werden
    unittest.main()
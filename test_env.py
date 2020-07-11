#   Unittest für das Environment
#   erstellt vom Environment Team
#   09.07.2020

from time import sleep
import unittest
import time
#import timeout_decorator - muss erst als Modul installiert werden (siehe UnitTest PDF Seite 33)
import random
import gym
from gym_miniworld.entity import Box, Agent
import gym_miniworld
import numpy as np
import math

#--------------------------------------------------Set Up und Tear Down definieren--------------------------------------

class simpleTest(unittest.TestCase):
    # SetUp Methode wird einmalig zu Begin des Tests ausgeführt
    def setUp(self):
       name = self.shortDescription()
       reward = 0

       if name == "Empty":                                                  # wird die setUp Methode mit "Empty" aufgerufen,
           self.env = gym.make('MiniWorld-HAWKMaze-v0')                     # zuerst wird das HawkMaze Environment erstellt
           self.env.room_size = 100                                         # der Raum wird auf eine Größe von 100x100 gesetzt
           self.env.anzahl_objs = 0                                         # wird die Anzahl der Boxen auf 0 gesetzt
           self.env.reset()                                                 # anschließend wird das Environment neugestartet (zur Initialisierung)

       if name == "Boxes":                                                  # wird die setUp Methode mit "Empty" aufgerufen,
           self.env = gym.make('MiniWorld-HAWKMaze-v0')                     # zuerst wird das HawkMaze Environment erstellt
           self.env.anzahl_objs = 10                                        # wird die Anzahl der Boxen auf 10 gesetzt
           self.env.reset()                                                 # anschließend wird das Environment neugestartet (zur Initialisierung)

       if name == "Place_Agent_on_defined_Position":                        # wird die setUp Methode mit "Place_Agent_on_defined_Position" aufgerufen,
           self.env = gym.make('MiniWorld-HAWKMaze-v0')                     # zuerst wird das HawkMaze Environment erstellt
           self.env.room_size = 5                                           # Der Raum wird auf eine Größe von 100x100 gesetzt, damit es nicht zu Kollisionen kommt
           self.env.num_rows = 2
           self.env.num_cols = 2
           self.env.anzahl_objs = 0
           self.env.reset()                                                 # das Environment wird neu gestartet
           self.env.place_entity(                                           # Platzieren einer Box an der Stelle x=15, z=10
               Box(color='red', size=0.9),
               pos=np.array([2, 0, 1]),
               dir=0
           )
           self.env.place_agent(                                            # Platzieren des Agents an einer definierten Stelle
               dir=math.pi / 2,
               min_x = 1.5, max_x = 2, min_z = 3, max_z = 4
           )

    # TearDown Methode wird einmalig zu Ende des Tests ausgeführt
    def tearDown(self):
        self.env.close()                                                    # Nachdem der Test beendet wurde, wird das Environment wieder geschlossen

#---------------------------------------------------Test Durchläufe-----------------------------------------------------

    # 1.Test: Prüfen ob die Parameter aus hawkmaze.py realisiert werden können (ohne den Timeout_Decorator ist dieser Test witzlos)
    #@timeout_decorator.timeout(1)
    def testParams(self):
        self.env = gym.make('MiniWorld-HAWKMaze-v0')  # zuerst wird das HawkMaze Environment erstellt
        self.env.reset()

    # 1.Test: Prüfung ob der Agent nur 45° Winkel einnimmt
    def testWinkel(self):
        """Empty"""
        theta = 0                                                           # die Variable "theta" wird mit 0 initalisiert
        for i in range (100):                                               # es werden 10 Durchläufe ausgeführt
            obs, reward, done, info = self.env.step(random.randint(0,4))    # ein zufälliger Schritt wird ausgeführt
            theta = round(self.env.agent.dir *180 /math.pi *10000) /10000   # der Winkel des Agents nach dem Schritt (in Grad) wird in die Variable "theta" geschrieben (gerundet auf Hunderttausendstel)
            mod = theta % self.env.phi_agent                                # mit dem Modulo Operator wird geprüft ob der Winkel restlos durch 45° teilbar ist.

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
        reward_sum = 0
        for k in range (9):                                                # es werden 10 Druchläufe ausgeführt
            obs, reward, done, info = self.env.step(self.env.actions.move_forward)   # der Agent führt einen Schritt geradeaus durch
            reward_sum += reward
            #self.env.render(view='top')
        obs, reward, done, info = self.env.step(self.env.actions.pickup)    # nach den 10 Schritten wird eine Pickup Aktion ausgeführt
        reward_sum += reward
        #self.env.render(view='top')
        #print(reward)
        self.assertEqual(reward_sum, 0.973)                                 # wenn der Reward dem errechneten Wert 0,99267 entspricht, wurde der Test bestanden

if __name__ == '__main__':                                                  # Durch diesen Befehl kann der Unittest direkt über das CMD Terminal aufgerufen werden
    unittest.main()
#   Unittest für das Environment
#   08.07.2020

import unittest
import random
import gym
import gym_miniworld
import numpy as np
import math

class simpleTest(unittest.TestCase):
    def setUp(self):                                    #SetUp Methode wird einmalig zu Begin des Tests ausgeführt
       self.env = gym.make('MiniWorld-HAWKMaze-v0')
       self.env.reset()


    def tearDown(self):                                 #TearDown Methode wird einmalgi zu Ende des Tests ausgeführt
        self.env.close()


    def testWinkel(self):                               #1. Test: Prüfung ob der Agent nur 45° Winkel einnimmt
        theta = 0
        for i in range (10):
            obs, reward, done, info = self.env.step(random.randint(0,4))
            theta = self.env.agent.dir *180 /math.pi
            #print(theta)
            mod = theta % 45
            #print(mod)

        self.assertEqual(mod, 0)

if __name__ == '__main__':
    unittest.main()
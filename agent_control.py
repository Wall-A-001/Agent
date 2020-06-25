#!/usr/bin/env python3
"""
agent_control.py

Dieses Programm soll es dem Agent ermöglichen sich selbst ein HAWKMaze Environment zu erstellen, ohne dafür auf
manual_control zurückgreifen zu müssen.

Zum aktuellen Stand konnte ich dieses Programm noch nicht ausprobieren, da mir die benötigten Dateien des Agent Ordners
fehlen. Ich weiß daher nicht ob dieses Program funktioniert oder nicht!

Stand: 14.06.2020
"""

# importe von manual_control.py
import sys
import argparse
import pyglet
import math
from pyglet.window import key
from pyglet import clock
import numpy as np
import gym
import gym_miniworld
# from manual_control import * #import manual_control - um die dort definierten Funktionen zu nutzen
from gym_miniworld.params import *

# importe von DQN_test.py
from DQN_Agent import Agent  # Hiermit gibt es scheinbar ein Problem
import tensorflow as tf

# --------------------------------------------------Step function definieren:-------------------------------------------
def step(action):
    #print('step {}/{}: {}'.format(env.step_count + 1, env.max_episode_steps, env.actions(action).name))

    obs, reward, done, info = env.step(action)

    #if reward > 0:
        #print('reward={:.2f}'.format(reward))

    #if done:
        #print('done!')
        #env.reset(agentgroesse, anzahl_obj)

    env.render()
        
# --------------------------------------------------Deklaration der Main Methode----------------------------------------
if __name__ == '__main__':
    env = gym.make('MiniWorld-MazeHAWK-v0')
    tf.compat.v1.disable_eager_execution()
    lr = 0.001
    n_games = 500
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr,
                  input_dims=env.observation_space.shape,
                  n_actions=env.action_space.n, mem_size=1000000, batch_size=64,
                  epsilon_end=0.01)

    # agent.load_model()
    scores = []
    eps_history = []

# --------------------------------------------------Initalisierung für Level:-------------------------------------------
    #env.domain_rand = True
    
    #top -> Draufsicht , agent -> First Person-Ansicht
    view_mode = 'top'

    #Größe des Agent anpassen, wenn nicht gesetzt (None) Standardwert 0.6
    agentgroesse = 0.6
    #Anzahl der Kisten. Bei 0 oder None werden zwischen 1 und 15 Kisten erstellt
    anzahl_obj = 5

    #Schrittweite des Agent
    schritt_agent = 0.50
    schritt_toleranz = 0.02

    #Winkel des Agents (Links-/Rechtsdrehung in Grad)
    phi_agent = 90
    phi_tol = 0

# --------------------------------------------------Leveldurchgang vorbereiten:-----------------------------------------
    for i in range(n_games):
        done = False
        score = 0
        observation = env.reset(agentgroesse, anzahl_obj)
        DEFAULT_PARAMS.set('forward_step', schritt_agent, schritt_agent - schritt_toleranz,
                           schritt_agent + schritt_toleranz)
        DEFAULT_PARAMS.set('turn_step', phi_agent, phi_agent - phi_tol, phi_agent + phi_tol)
        
# --------------------------------------------------Level ablauf--------------------------------------------------------
        while not done:
            env.render(view=view_mode)
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(0) #Hier habe ich env.step() zu step() geändert,...
            # damit die oben definierte Step function aufgerufen wird
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()

# --------------------------------------------------Wenn Level beendet:-------------------------------------------------
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        print('episode: ', i, 'score %.2f' % score,
              'average_score %.2f' % avg_score,
              'epsilon %.2f' % agent.epsilon)
        env.reset(agentgroesse, anzahl_obj)
        
# --------------------------------------------------wenn alle Durchläufe beendet----------------------------------------
    env.close()

    # if i % 10 == 0 and i > 0:
    # agent.save_model()

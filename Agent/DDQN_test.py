#!/usr/bin/env python3

"""
This script allows you to manually control the simulator
using the keyboard arrows.
"""
import sys
import argparse
from DDQN_Agent import DDQN_Agent
import math
import numpy as np
import gym
import gym_miniworld
from collections import deque
from gym_miniworld.params import *

# Helpful preprocessing taken from github.com/ageron/tiny-dqn
def process_frame(frame):
    mspacman_color = np.array([210, 164, 74]).mean()
    img = frame[1:176:2, ::2]  # Crop and downsize
    img = img.mean(axis=2)  # Convert to greyscale
    img[img == mspacman_color] = 0  # Improve contrast by making pacman white
    img = (img - 128) / 128 - 1  # Normalize from -1 to 1.

    return np.expand_dims(img.reshape(30, 40, 1), axis=0)


# Averages images from the last few frame
def blend_images(images, blend):
    avg_image = np.expand_dims(np.zeros((30, 40, 1), np.float64), axis=0)

    for image in images:
        avg_image += image

    if len(images) < blend:
        return avg_image / len(images)
    else:
        return avg_image / blend

def step(action):
    print('step {}/{}: {}'.format(env.step_count + 1, env.max_episode_steps, env.actions(action).name))

    obs, reward, done, info = env.step(action)

    if reward > 0:
        print('reward={:.2f}'.format(reward))

    if done:
        print('done!')
        env.reset(agentgroesse, anzahl_obj)

    return obs, reward, done, info




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--env-name', default='MiniWorld-MazeHAWK-v0')
    parser.add_argument('--domain-rand', action='store_true', help='enable domain randomization')
    parser.add_argument('--no-time-limit', action='store_true', help='ignore time step limits')
    parser.add_argument('--top_view', action='store_true', help='show the top view instead of the agent view')
    args = parser.parse_args()

    env = gym.make(args.env_name)
    if args.no_time_limit:
        env.max_episode_steps = math.inf
        if args.domain_rand:
            env.domain_rand = True
    #
    # '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PARAMETEREINSTELLUNG HAWK-Maze %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    # '---------------------------------------------------------------------------------------------------------------'
    # 'top -> Draufsicht , agent -> First Person-Ansicht'
    view_mode = 'top'

    # 'Größe des Agent anpassen, wenn nicht gesetzt (None) Standardwert 0.6'
    agentgroesse = 0.6
    # 'Anzahl der Kisten. Bei 0 oder None werden zwischen 1 und 15 Kisten erstellt'
    anzahl_obj = 0
    #
    # 'Schrittweite des Agent'
    schritt_agent = 0.50
    schritt_toleranz = 0.02
    #
    # 'Winkel des Agents (Links-/Rechtsdrehung in Grad)'
    phi_agent = 90
    phi_tol = 0
    #
    # '----------------------------------------------------------------------------------------------------------------'

    state_size = (30, 40, 1)
    #action_size = env.action_space.n
    action_size = 6
    agent = DDQN_Agent(state_size, action_size)
    # agent.load('models/')

    episodes = 5000
    batch_size = 32
    skip_start = 90  # MsPacman-v0 waits for 90 actions before the episode begins
    total_time = 0  # Counter for total number of steps taken
    all_rewards = 0  # Used to compute avg reward over time
    blend = 4  # Number of images to blend
    done = False

    for e in range(episodes):
        total_reward = 0
        game_score = 0
        state = process_frame(env.reset())
        images = deque(maxlen=blend)  # Array of images to be blended
        images.append(state)

       # for skip in range(skip_start):  # skip the start of each game
        #    env.step(0)

        for time in range(env.max_episode_steps + 1):

            env.render(view='top')
            total_time += 1

            # Every update_rate timesteps we update the target network parameters
            if total_time % agent.update_rate == 0:
                agent.update_target_model()

            # Return the avg of the last 4 frames
            state = blend_images(images, blend)

            # Transition Dynamics
            action = agent.act(state)
            next_state, reward, done, _ = step(action)

            game_score += reward
            total_reward += reward

            # Return the avg of the last 4 frames
            next_state = process_frame(next_state)
            images.append(next_state)
            next_state = blend_images(images, blend)

            # Store sequence in replay memory
            agent.remember(state, action, reward, next_state, done)

            state = next_state

            if time == env.max_episode_steps:
                done = True



            if done:
                all_rewards += game_score

                print("episode: {}/{}, game score: {}, reward: {}, avg reward: {}, time: {}, total time: {}"
                      .format(e + 1, episodes, game_score, total_reward, all_rewards / (e + 1), time, total_time))

                break

            # if len(agent.memory) > batch_size:
            #     agent.replay(batch_size)

        if e % 10 == 0 and e > 0:
            agent.save('dqn_model.h5')
            print("Model Saved")

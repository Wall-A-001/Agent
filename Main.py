from DDQN_Agent import DDQN_Agent
import random
import gym
import gym_miniworld
import numpy as np
from collections import deque


def step(action):
    print('step {}/{}: {}'.format(env.step_count+1, env.max_episode_steps, env.actions(action).name))

    obs, reward, done, info = env.step(action)

    if reward > 0:
        print('reward={:.2f}'.format(reward))

    if done:
        print('done!')
        env.reset()

    env.render('pyglet', view='top')

    return obs, reward, done, info


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

if __name__ == '__main__':
    env = gym.make('MiniWorld-HAWKMaze-v0')
    state_size = (30, 40, 1)
    action_size = env.action_space.n
    agent = DDQN_Agent(state_size, action_size)

    # Loads a saved model
    #agent.load('dqn_model.h5')

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

      #  for skip in range(skip_start):  # skip the start of each game
      #      env.step(0)

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

        if len(agent.memory) < batch_size:
                agent.replay(batch_size)

        if e % 10 == 0 and e > 0:
          agent.save('dqn_model.h5')
          print("Model Saved")
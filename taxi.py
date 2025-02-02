"""
Dans ce TP, nous allons implémenter un agent qui apprend à jouer au jeu Taxi-v3
de OpenAI Gym. Le but du jeu est de déposer un passager à une destination
spécifique en un minimum de temps. Le jeu est composé d'une grille de 5x5 cases
et le taxi peut se déplacer dans les 4 directions (haut, bas, gauche, droite).
Le taxi peut prendre un passager sur une case spécifique et le déposer à une
destination spécifique. Le jeu est terminé lorsque le passager est déposé à la
destination. Le jeu est aussi terminé si le taxi prend plus de 200 actions.

Vous devez implémenter un agent qui apprend à jouer à ce jeu en utilisant
les algorithmes Q-Learning et SARSA.

Pour chaque algorithme, vous devez réaliser une vidéo pour montrer que votre modèle fonctionne.
Vous devez aussi comparer l'efficacité des deux algorithmes en termes de temps
d'apprentissage et de performance.

A la fin, vous devez rendre un rapport qui explique vos choix d'implémentation
et vos résultats (max 1 page).
"""

import typing as t
import gymnasium as gym
import numpy as np
from qlearning import QLearningAgent
from qlearning_eps_scheduling import QLearningAgentEpsScheduling
from sarsa import SarsaAgent
import time
import os
from gym.wrappers import RecordVideo

env = gym.make("Taxi-v3", render_mode="rgb_array")
n_actions = env.action_space.n  # type: ignore


#################################################
# 1. Play with QLearningAgent
#################################################

# You can edit these hyperparameters!
agent = QLearningAgent(
    learning_rate=0.5, epsilon=0.1, gamma=0.99, legal_actions=list(range(n_actions))
)


def play_and_train(env: gym.Env, agent: QLearningAgent, t_max=int(1e4)) -> float:
    """
    This function should
    - run a full game, actions given by agent.getAction(s)
    - train agent using agent.update(...) whenever possible
    - return total rewardb
    """
    total_reward: t.SupportsFloat = 0.0
    s, _ = env.reset()

    for _ in range(t_max):
        # Get agent to pick action given state s
        a = agent.get_action(s)

        next_s, r, done, _, _ = env.step(a)

        # Train agent for state s
        # BEGIN SOLUTION
        agent.update(s, a, r, next_s)
        total_reward += r
        s = next_s 
        if done:
            break  
        # END SOLUTION

    return total_reward

start_time1 = time.time() 
rewards = []

# TODO: créer des vidéos de l'agent en action

QLearningAgentFolder = "./QLearningAgent_videos"
if not os.path.exists(QLearningAgentFolder):
    os.makedirs(QLearningAgentFolder)

env = RecordVideo(gym.make("Taxi-v3", render_mode="rgb_array"), 
                  video_folder=QLearningAgentFolder,
                  episode_trigger=lambda x: x == 729)

for i in range(1000):
    rewards.append(play_and_train(env, agent))
    if i % 100 == 0:
        print("mean reward", np.mean(rewards[-100:]))

assert np.mean(rewards[-100:]) > 0.0
env.close()

end_time1 = time.time()
rewards_QLearningAgent = rewards

#################################################
# 2. Play with QLearningAgentEpsScheduling
#################################################


agent = QLearningAgentEpsScheduling(
    learning_rate=0.5, epsilon=0.25, gamma=0.99, legal_actions=list(range(n_actions))
)

start_time2 = time.time() 
rewards = []

# TODO: créer des vidéos de l'agent en action
QLearningAgentEpsSchedulingFolder = "./QLearningAgentEpsScheduling_videos"
if not os.path.exists(QLearningAgentEpsSchedulingFolder):
    os.makedirs(QLearningAgentEpsSchedulingFolder)

env = RecordVideo(gym.make("Taxi-v3", render_mode="rgb_array"), 
                video_folder=QLearningAgentEpsSchedulingFolder,
                episode_trigger=lambda x: x == 729)

for i in range(1000):
    rewards.append(play_and_train(env, agent))
    if i % 100 == 0:
        print("mean reward", np.mean(rewards[-100:]))

assert np.mean(rewards[-100:]) > 0.0

end_time2 = time.time() 
rewards_QLearningAgentEpsScheduling = rewards

env.close()

####################
# 3. Play with SARSA
####################


agent = SarsaAgent(learning_rate=0.5, gamma=0.99, legal_actions=list(range(n_actions)))

SarsaAgentFolder = "./SarsaAgent_videos"
if not os.path.exists(SarsaAgentFolder):
    os.makedirs(SarsaAgentFolder)

env = RecordVideo(gym.make("Taxi-v3", render_mode="rgb_array"), 
                  video_folder=SarsaAgentFolder,
                  episode_trigger=lambda x: x == 729)

start_time3 = time.time()
rewards = []

for i in range(1000):
    rewards.append(play_and_train(env, agent))
    if i % 100 == 0:
        print("mean reward", np.mean(rewards[-100:]))

env.close()

end_time3 = time.time()
rewards_SarsaAgent = rewards

print(f"Total training time for QLearningArgent: {end_time1 - start_time1} seconds, Reward mean: {np.mean(rewards_QLearningAgent[-100:])}")
print(f"Total training time for QLearningAgentEpsScheduling: {end_time2 - start_time2} seconds, Reward mean : {np.mean(rewards_QLearningAgentEpsScheduling[-100:])}")
print(f"Total training time for SarsaAgent: {end_time3 - start_time3} seconds, Reward mean : {np.mean(rewards_SarsaAgent[-100:])}")
#!/usr/bin/env python3
import argparse
import collections
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3") # Report only TF errors by default

import gym
import numpy as np
import tensorflow as tf

import wrappers
import time
import torch

from TD3 import TD3

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=True, action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=0, type=int, help="Render some episodes.")
parser.add_argument("--seed", default=88, type=int, help="Random seed.")
parser.add_argument("--threads", default=1, type=int, help="Maximum number of threads to use.")
# For these and any other arguments you add, ReCodEx will keep your default value.

def main(env, args):
    # Fix random seeds and number of threads
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)
    tf.config.threading.set_inter_op_parallelism_threads(args.threads)
    tf.config.threading.set_intra_op_parallelism_threads(args.threads)

    if args.recodex:
        # TODO: Perform evaluation of a trained model.


        

        agent = TD3('Bipedalhardcore', env, batch_size=100, seed=args.seed)
        agent.load_weight()
        while True:
            state, done = env.reset(start_evaluation=True), False
            while not done:
                # TODO: Choose an action
                env.render()
                action = agent.policy(state)

                state, reward, done, _ = env.step(action)

    else:
        # TODO: Perform training

        pass


#if __name__ == "__main__":
#    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
#    env = wrappers.EvaluationWrapper(gym.make("BipedalWalkerHardcore-v3"), args.seed)

#    main(env, args)

max_steps = 3000
falling_down = 0

#def train():
if __name__ == '__main__':
    frame_skip = 3
    env = wrappers.FrameSkipWrapper(wrappers.EvaluationWrapper(gym.make("BipedalWalkerHardcore-v3"), 1),  frame_skip)
    agent = TD3('Bipedalhardcore', env, batch_size=100, seed=1)
    agent.load_weight()
    total_episodes = 100000
    start_timestep = 0
    time_start = time.time()
    ep_reward_list = []
    avg_reward_list = []
    total_timesteps = 0
    pred_loss = 0
    numtrainedexp = 0
    save_time = 0
    expcount = 0
    totrain = 0

    for ep in range(total_episodes):
        state = env.reset()
        episodic_reward = 0
        timestep = 0
        temp_replay_buffer = []

        for st in range(max_steps):

            # Select action randomly or according to policy
            if total_timesteps < start_timestep:
                action = env.action_space.sample()
            else:
                action = agent.policy(state)

            # Recieve state and reward from environment.
            next_state, reward, done, info = env.step(action)
            # change original reward from -100 to -5 and 5*reward for other values
            episodic_reward += reward
            if reward == -100:
                add_reward = -1
                reward = -5
                falling_down += 1
                expcount += 1
            else:
                add_reward = 0
                reward = 5 * reward

            temp_replay_buffer.append((state, action, reward, add_reward, next_state, done))

            # End this episode when `done` is True
            if done:
                if add_reward == -1 or episodic_reward < 250:
                    totrain = 1
                    for temp in temp_replay_buffer:
                        agent.add_to_replay_memory(temp, agent.replay_memory_buffer)
                elif expcount > 0 and np.random.rand() > 0.5:
                    totrain = 1
                    expcount -= 10
                    for temp in temp_replay_buffer:
                        agent.add_to_replay_memory(temp, agent.replay_memory_buffer)
                break
            state = next_state
            timestep += 1
            total_timesteps += 1

        ep_reward_list.append(episodic_reward)
        # Mean of last 100 episodes
        avg_reward = np.mean(ep_reward_list[-100:])
        avg_reward_list.append(avg_reward)

        if avg_reward > 300:
            test_reward = agent.eval_policy(env, seed=1, eval_episodes=10)
            if test_reward > 308:
                final_test_reward = agent.eval_policy(env, seed=1, eval_episodes=100)
                if final_test_reward > 308:
                    torch.save(agent.actor.state_dict(), 'actor.pth')
                    torch.save(agent.critic.state_dict(), 'critic.pth')
                    torch.save(agent.actor_target.state_dict(), 'actor_t.pth')
                    torch.save(agent.critic_target.state_dict(), 'critic_t.pth')
                    torch.save(agent.predmodel.state_dict(), 'predmodel.pth')
                    print("===========================")
                    print('Task Solved')
                    print("===========================")
                    break

        s = (int)(time.time() - time_start)

        # Training agent only when new experiences are added to the replay buffer
        weight = 1 - np.clip(np.mean(ep_reward_list[-100:]) / 300, 0, 1)
        if totrain == 1:
            pred_loss = agent.learn_and_update_weights_by_replay(timestep, weight, totrain)
        else:
            pred_loss = agent.learn_and_update_weights_by_replay(100, weight, totrain)
        totrain = 0

        print(
            'Ep. {}, Timestep {},  Ep.Timesteps {}, Episode Reward: {:.2f}, Moving Avg.Reward: {:.2f}, Time: {:02}:{:02}:{:02} , Falling down: {}, Weight: {}'
            .format(ep, total_timesteps, timestep,
                    episodic_reward, avg_reward, s // 3600, s % 3600 // 60, s % 60, falling_down, weight))
        if s // 1800 == save_time:

            torch.save(agent.actor.state_dict(), 'actor-time{}.pth'.format(save_time))
            torch.save(agent.critic.state_dict(), 'critic-time{}.pth'.format(save_time))
            torch.save(agent.actor_target.state_dict(), 'actor_t-time{}.pth'.format(save_time))
            torch.save(agent.critic_target.state_dict(), 'critic_t-time{}.pth'.format(save_time))
            torch.save(agent.predmodel.state_dict(), 'predmodel-time{}.pth'.format(save_time))
            print("===========================")
            print('Saving Successfully!')
            print("===========================")
            save_time += 1

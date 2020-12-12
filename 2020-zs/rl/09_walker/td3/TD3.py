import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import deque
import torch.optim as optim
import random


class Actor(nn.Module):
    def __init__(self, state_size, action_size, seed, fc_units=400, fc1_units=300):
        super(Actor, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, fc_units)
        self.fc2 = nn.Linear(fc_units, fc1_units)
        self.fc3 = nn.Linear(fc1_units, action_size)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        return F.torch.tanh(self.fc3(x))


class Critic(nn.Module):
    def __init__(self, state_size, action_size, seed, fc1_units=400, fc2_units=300):
        super(Critic, self).__init__()
        self.seed = torch.manual_seed(seed)

        # Q1
        self.l1 = nn.Linear(state_size + action_size, fc1_units)
        self.l2 = nn.Linear(fc1_units, fc2_units)
        self.l3 = nn.Linear(fc2_units, 1)

        # Q2
        self.l4 = nn.Linear(state_size + action_size, fc1_units)
        self.l5 = nn.Linear(fc1_units, fc2_units)
        self.l6 = nn.Linear(fc2_units, 1)

    def forward(self, state, action):
        xa = torch.cat([state, action], 1)

        x1 = F.relu(self.l1(xa))
        x1 = F.relu(self.l2(x1))
        x1 = self.l3(x1)

        x2 = F.relu(self.l4(xa))
        x2 = F.relu(self.l5(x2))
        x2 = self.l6(x2)

        return x1, x2


class PredictionModel(nn.Module):
    def __init__(self, state_size, action_size, fc1_units=400, fc2_units=300):
        super(PredictionModel, self).__init__()
        self.l1 = nn.Linear(state_size + action_size, fc1_units)
        self.l2 = nn.Linear(fc1_units, fc2_units)
        self.l3 = nn.Linear(fc2_units, state_size)

    def forward(self, state, action):
        xa = torch.cat([state, action], 1)

        x1 = F.relu(self.l1(xa))
        x1 = F.relu(self.l2(x1))
        x1 = self.l3(x1)

        return x1


# TODO: refactor to pytorch lightning
class TD3:
    def __init__(
            self, name, env,
            load=False,
            gamma=0.99,  # discount factor
            lr_actor=3e-4,
            lr_critic=3e-4,
            lr_predmodel=3e-4,
            batch_size=100,
            buffer_capacity=1000000,
            tau=0.02,  # target network update factor
            random_seed=np.random.randint(1, 10000),
            cuda=True,
            policy_noise=0.2,
            std_noise=0.1,
            noise_clip=0.5,
            policy_freq=2,  # target network update period
            seed=88
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.env = env
        self.seed = seed
        self.create_actor()
        self.create_critic()
        self.create_prediction_model()
        self.act_opt = optim.Adam(self.actor.parameters(), lr=lr_actor)
        self.crt_opt = optim.Adam(self.critic.parameters(), lr=lr_critic)
        self.pred_opt = optim.Adam(self.predmodel.parameters(), lr=lr_predmodel)
        self.set_weights()
        self.replay_memory_buffer = deque(maxlen=buffer_capacity)
        self.replay_memory_bufferd_dis = deque(maxlen=buffer_capacity)
        self.batch_size = batch_size
        self.tau = tau
        self.policy_freq = policy_freq
        self.gamma = gamma
        self.name = name
        self.upper_bound = self.env.action_space.high[0]  # action space upper bound
        self.lower_bound = self.env.action_space.low[0]  # action space lower bound
        self.obs_upper_bound = self.env.observation_space.high[0]  # state space upper bound
        self.obs_lower_bound = self.env.observation_space.low[0]  # state space lower bound
        self.policy_noise = policy_noise
        self.noise_clip = noise_clip
        self.std_noise = std_noise

    def create_actor(self):
        params = {
            'state_size': self.env.observation_space.shape[0],
            'action_size': self.env.action_space.shape[0],
            'seed': self.seed
        }
        self.actor = Actor(**params).to(self.device)
        self.actor_target = Actor(**params).to(self.device)

    def create_critic(self):
        params = {
            'state_size': self.env.observation_space.shape[0],
            'action_size': self.env.action_space.shape[0],
            'seed': self.seed
        }
        self.critic = Critic(**params).to(self.device)
        self.critic_target = Critic(**params).to(self.device)

    def create_prediction_model(self):
        params = {
            'state_size': self.env.observation_space.shape[0],
            'action_size': self.env.action_space.shape[0]
        }
        self.predmodel = PredictionModel(**params).to(self.device)

    def set_weights(self):
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.critic_target.load_state_dict(self.critic.state_dict())

    def load_weight(self):
        self.actor.load_state_dict(
            torch.load('actor.pth', map_location=self.device))
        self.critic.load_state_dict(
            torch.load('critic.pth', map_location=self.device))
        self.actor_target.load_state_dict(
            torch.load('actor_t.pth', map_location=self.device))
        self.critic_target.load_state_dict(
            torch.load('critic_t.pth', map_location=self.device))
        self.predmodel.load_state_dict(
            torch.load('predmodel.pth', map_location=self.device))

    def add_to_replay_memory(self, transition, buffername):
        buffername.append(transition)

    def get_random_sample_from_replay_mem(self, buffername):
        random_sample = random.sample(buffername, self.batch_size)
        return random_sample

    def learn_and_update_weights_by_replay(self, training_iterations, weight, totrain):
        if len(self.replay_memory_buffer) < 1e4:
            return 1
        for it in range(training_iterations):
            mini_batch = self.get_random_sample_from_replay_mem(self.replay_memory_buffer)
            state_batch = torch.from_numpy(np.vstack([i[0] for i in mini_batch])).float().to(self.device)
            action_batch = torch.from_numpy(np.vstack([i[1] for i in mini_batch])).float().to(self.device)
            reward_batch = torch.from_numpy(np.vstack([i[2] for i in mini_batch])).float().to(self.device)
            add_reward_batch = torch.from_numpy(np.vstack([i[3] for i in mini_batch])).float().to(self.device)
            next_state_batch = torch.from_numpy(np.vstack([i[4] for i in mini_batch])).float().to(self.device)
            done_list = torch.from_numpy(np.vstack([i[5] for i in mini_batch]).astype(np.uint8)).float().to(self.device)

            # Train Critic
            target_actions = self.actor_target(next_state_batch)
            offset_noises = torch.FloatTensor(action_batch.shape).data.normal_(0, self.policy_noise).to(self.device)

            # clip noise
            offset_noises = offset_noises.clamp(-self.noise_clip, self.noise_clip)
            target_actions = (target_actions + offset_noises).clamp(self.lower_bound, self.upper_bound)

            # Compute the target Q value
            Q_targets1, Q_targets2 = self.critic_target(next_state_batch, target_actions)
            Q_targets = torch.min(Q_targets1, Q_targets2)
            Q_targets = reward_batch + self.gamma * Q_targets * (1 - done_list)

            # Compute current Q estimates
            current_Q1, current_Q2 = self.critic(state_batch, action_batch)
            # Compute critic loss
            critic_loss = F.mse_loss(current_Q1, Q_targets.detach()) + F.mse_loss(current_Q2, Q_targets.detach())
            # Optimize the critic
            self.crt_opt.zero_grad()
            critic_loss.backward()
            self.crt_opt.step()

            self.soft_update_target(self.critic, self.critic_target)

            # Train prediction model
            predict_next_state = self.predmodel(state_batch, action_batch) * (1 - done_list)
            next_state_batch = next_state_batch * (1 - done_list)
            prediction_loss = F.mse_loss(predict_next_state, next_state_batch.detach())
            self.pred_opt.zero_grad()
            prediction_loss.backward()
            self.pred_opt.step()

            s_flag = 1 if prediction_loss.item() < 0.020 else 0

            # Train Actor
            # Delayed policy updates
            if it % self.policy_freq == 0 and totrain == 1:
                actions = self.actor(state_batch)
                actor_loss1, _ = self.critic_target(state_batch, actions)
                actor_loss1 = actor_loss1.mean()
                actor_loss = - actor_loss1

                if s_flag == 1:
                    p_actions = self.actor(state_batch)
                    p_next_state = self.predmodel(state_batch, p_actions).clamp(self.obs_lower_bound,
                                                                                self.obs_upper_bound)

                    p_actions2 = self.actor(p_next_state.detach()) * self.upper_bound
                    actor_loss2, _ = self.critic_target(p_next_state.detach(), p_actions2)
                    actor_loss2 = actor_loss2.mean()

                    p_next_state2 = self.predmodel(p_next_state.detach(), p_actions2).clamp(self.obs_lower_bound,
                                                                                            self.obs_upper_bound)
                    p_actions3 = self.actor(p_next_state2.detach()) * self.upper_bound
                    actor_loss3, _ = self.critic_target(p_next_state2.detach(), p_actions3)
                    actor_loss3 = actor_loss3.mean()

                    actor_loss_final = actor_loss - weight * (actor_loss2) - 0.5 * weight * actor_loss3
                else:
                    actor_loss_final = actor_loss

                self.act_opt.zero_grad()
                actor_loss_final.backward()
                self.act_opt.step()

                # Soft update target models

                self.soft_update_target(self.actor, self.actor_target)

        return prediction_loss.item()

    def soft_update_target(self, local_model, target_model):
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(self.tau * local_param.data + (1.0 - self.tau) * target_param.data)

    def policy(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
        self.actor.eval()
        with torch.no_grad():
            actions = self.actor(state).cpu().data.numpy()
        self.actor.train()
        # Adding noise to action
        shift_action = np.random.normal(0, self.std_noise, size=self.env.action_space.shape[0])
        sampled_actions = (actions + shift_action)
        # We make sure action is within bounds
        legal_action = np.clip(sampled_actions, self.lower_bound, self.upper_bound)
        return np.squeeze(legal_action)

    def select_action(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
        with torch.no_grad():
            actions = self.actor_target(state).cpu().data.numpy()
        return np.squeeze(actions)

    def eval_policy(self, env_name, seed, eval_episodes):
        eval_env = env_name
        eval_env.seed(seed + 100)

        avg_reward = 0.
        for _ in range(eval_episodes):
            state, done = eval_env.reset(), False
            while not done:
                action = self.select_action(np.array(state))
                state, reward, done, _ = eval_env.step(action)
                avg_reward += reward
        avg_reward /= eval_episodes

        print("---------------------------------------")
        print(f"Evaluation over {eval_episodes} episodes: {avg_reward:.3f}")
        print("---------------------------------------")
        return avg_reward

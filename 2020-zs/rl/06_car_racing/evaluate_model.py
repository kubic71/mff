# from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import DQN
from pygame.time import Clock
import argparse
import wrappers
import numpy as np
import gym
import os

import pygame

from PIL import Image






parser = argparse.ArgumentParser()

parser.add_argument("--seed", default=22, type=int, help="Random seed.")
parser.add_argument("--frame_skip", default=1, type=int, help="Frame skip.")

parser.add_argument("--render", default=False, action="store_true")

parser.add_argument("--load_from", default="saved_models/gp=15_t=1000000.zip", type=str)
parser.add_argument("--logdir", default="logs", type=str)

parser.add_argument("--action_map", default="small", type=str)
parser.add_argument("--safety", default=0, type=float)

parser.add_argument("--evaluate_for", default=100, type=int) 
parser.add_argument("--decode_vae", default=False, action="store_true") 




def make_env():

    def _init():
        env = gym.make("CarRacingSoftFS{}-v0".format(args.frame_skip))
        env = wrappers.VaeCarWrapper(env,silent=True)
        globals()['vae'] = env.vae
        globals()['vae_wrapper'] = env
        env = wrappers.CarDiscretizatinoWrapper(env, args.action_map == "large")

        env = wrappers.EvaluationWrapper(env, args.seed, evaluate_for=args.evaluate_for, 
                                         report_each=1, logname="/dev/null")
        return env
    return _init

def resize(img, size):
    obs = Image.fromarray(img, mode="RGB").resize((size, size))
    return np.array(obs)

def evaluate(model, env):
    clock = Clock()
    if args.decode_vae:
        pygame.init() 
        screen = pygame.display.set_mode((600, 600))

    print("Evaluating!")

    while True:
        state, done = env.reset(start_evaluation=True), False
        while not done:

            if args.render:
                env.render()
                clock.tick(60)

            # visualization of what agent sees

            if args.decode_vae:
                reconstruct = vae.decode(np.array([vae_wrapper.features]))
                screen.fill((0,0,0))
                screen.blit(pygame.surfarray.make_surface(resize(reconstruct[0].transpose(1, 0, 2), 600)), (0, 0))
                pygame.display.flip()
    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
    
    
            # real speed
            state[32] += args.safety

            # abs 1-4
            state[34:38] += args.safety

            # action = np.argmax(model.forward(state))
            action, _states = model.predict(state, deterministic=True)
            state, reward, done, _ = env.step(action)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    env = make_env()()

    if args.load_from is not None:
        print("loading model", args.load_from)
        model = DQN.load(args.load_from)

    evaluate(model, env)

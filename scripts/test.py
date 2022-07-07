import isaacgym

assert isaacgym
import matplotlib.pyplot as plt
import torch
from tqdm import trange

from mini_gym.envs import *
from mini_gym.envs.base.legged_robot_config import Cfg
from mini_gym.envs.mini_cheetah.mini_cheetah_config import config_mini_cheetah


def run_env(render=False, headless=False):
    # prepare environment
    config_mini_cheetah(Cfg)

    # 5 times per second

    Cfg.env.num_envs = 3
    Cfg.domain_rand.push_interval_s = 1
    Cfg.terrain.num_rows = 3
    Cfg.terrain.num_cols = 5
    Cfg.terrain.border_size = 0
    Cfg.domain_rand.randomize_friction = True
    Cfg.domain_rand.friction_range = [1.0, 1.01]
    Cfg.domain_rand.randomize_base_mass = True
    Cfg.domain_rand.added_mass_range = [0., 6.]
    Cfg.terrain.terrain_noise_magnitude = 0.0
    # Cfg.asset.fix_base_link = True

    env = gym.make("VelocityTrackingEasyEnv-v0", headless=headless, cfg=Cfg)
    env.reset()

    if render and headless:
        img = env.render(mode="rgb_array")
        plt.imshow(img)
        plt.show()
        print("Show the first frame and exit.")
        exit()

    for i in trange(1_000, desc="Running"):
        actions = 0. * torch.ones(env.num_envs, env.num_actions, device=env.device)
        obs, rew, done, info = env.step(actions)

    print("Done")


if __name__ == '__main__':
    # Run this to render to your computer
    run_env(render=True, headless=False)
    # Uncomment this to render using matplotlib
    # run_env(render=False, headless=False)

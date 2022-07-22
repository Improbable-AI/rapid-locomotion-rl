import isaacgym

assert isaacgym
import torch
import numpy as np

from mini_gym.envs import *
from mini_gym.envs.base.legged_robot_config import Cfg
from mini_gym.envs.mini_cheetah.mini_cheetah_config import config_mini_cheetah
from mini_gym.envs.mini_cheetah.velocity_tracking import VelocityTrackingEasyEnv

from tqdm import tqdm


def load_env(headless=False):
    # prepare environment
    config_mini_cheetah(Cfg)

    from ml_logger import logger

    print(logger.glob("*"))
    print(logger.prefix)

    params = logger.load_pkl('parameters.pkl')

    if 'kwargs' in params[0]:
        deps = params[0]['kwargs']

        from mini_gym_learn.ppo.ppo import PPO_Args
        from mini_gym_learn.ppo.actor_critic import AC_Args
        from mini_gym_learn.ppo import RunnerArgs

        AC_Args._update(deps)
        PPO_Args._update(deps)
        RunnerArgs._update(deps)
        Cfg.terrain._update(deps)
        Cfg.commands._update(deps)
        Cfg.normalization._update(deps)
        Cfg.env._update(deps)
        Cfg.domain_rand._update(deps)
        Cfg.rewards._update(deps)
        Cfg.reward_scales._update(deps)
        Cfg.perception._update(deps)
        Cfg.domain_rand._update(deps)
        Cfg.control._update(deps)

    # turn off DR for evaluation script
    Cfg.domain_rand.push_robots = False
    Cfg.domain_rand.randomize_friction = False
    Cfg.domain_rand.randomize_gravity = False
    Cfg.domain_rand.randomize_restitution = False
    Cfg.domain_rand.randomize_motor_offset = False
    Cfg.domain_rand.randomize_motor_strength = False
    Cfg.domain_rand.randomize_friction_indep = False
    Cfg.domain_rand.randomize_ground_friction = False
    Cfg.domain_rand.randomize_base_mass = False
    Cfg.domain_rand.randomize_Kd_factor = False
    Cfg.domain_rand.randomize_Kp_factor = False
    Cfg.domain_rand.randomize_joint_friction = False
    Cfg.domain_rand.randomize_com_displacement = False

    Cfg.env.num_recording_envs = 1
    Cfg.env.num_envs = 1
    Cfg.terrain.num_rows = 3
    Cfg.terrain.num_cols = 5
    Cfg.terrain.border_size = 0

    from mini_gym.envs.wrappers.history_wrapper import HistoryWrapper

    env = VelocityTrackingEasyEnv(sim_device='cuda:0', headless=False, cfg=Cfg)
    env = HistoryWrapper(env)

    # load policy
    from ml_logger import logger
    from mini_gym_learn.ppo.actor_critic import ActorCritic

    actor_critic = ActorCritic(
        num_obs=Cfg.env.num_observations,
        num_privileged_obs=Cfg.env.num_privileged_obs,
        num_obs_history=Cfg.env.num_observations * \
                        Cfg.env.num_observation_history,
        num_actions=Cfg.env.num_actions)

    print(logger.prefix)
    print(logger.glob("*"))
    weights = logger.load_torch("checkpoints/ac_weights_last.pt")
    actor_critic.load_state_dict(state_dict=weights)
    actor_critic.to(env.device)
    policy = actor_critic.act_inference

    return env, policy


def play_mc(headless=True):
    from ml_logger import logger

    from pathlib import Path
    from mini_gym import MINI_GYM_ROOT_DIR
    import glob
    import os

    recent_runs = sorted(glob.glob(f"{MINI_GYM_ROOT_DIR}/runs/rapid-locomotion/*/*/*"), key=os.path.getmtime)
    print(recent_runs)

    logger.configure(Path(recent_runs[-1]).resolve())

    env, policy = load_env(headless=headless)

    num_eval_steps = 250
    x_vel_cmd, y_vel_cmd, yaw_vel_cmd = 3.0, 0.0, 0.0

    measured_x_vels = np.zeros(num_eval_steps)
    target_x_vels = np.ones(num_eval_steps) * x_vel_cmd
    joint_positions = np.zeros((num_eval_steps, 12))

    obs = env.reset()

    for i in tqdm(range(num_eval_steps)):
        with torch.no_grad():
            actions = policy(obs)
        env.commands[:, 0] = x_vel_cmd
        env.commands[:, 1] = y_vel_cmd
        env.commands[:, 2] = yaw_vel_cmd
        obs, rew, done, info = env.step(actions)

        measured_x_vels[i] = env.base_lin_vel[0, 0]
        joint_positions[i] = env.dof_pos[0, :].cpu()

    # plot target and measured forward velocity
    from matplotlib import pyplot as plt
    fig, axs = plt.subplots(2, 1, figsize=(12, 5))
    axs[0].plot(np.linspace(0, num_eval_steps * env.dt, num_eval_steps), measured_x_vels, color='black', linestyle="-", label="Measured")
    axs[0].plot(np.linspace(0, num_eval_steps * env.dt, num_eval_steps), target_x_vels, color='black', linestyle="--", label="Desired")
    axs[0].legend()
    axs[0].set_title("Forward Linear Velocity")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Velocity (m/s)")

    axs[1].plot(np.linspace(0, num_eval_steps * env.dt, num_eval_steps), joint_positions, linestyle="-", label="Measured")
    axs[1].set_title("Joint Positions")
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("Joint Position (rad)")

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # to see the environment rendering, set headless=False
    play_mc(headless=False)

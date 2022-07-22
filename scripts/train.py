def train_mc(headless=True):

    import isaacgym
    assert isaacgym
    import torch

    from mini_gym.envs.base.legged_robot_config import Cfg
    from mini_gym.envs.mini_cheetah.mini_cheetah_config import config_mini_cheetah
    from mini_gym.envs.mini_cheetah.velocity_tracking import VelocityTrackingEasyEnv

    from ml_logger import logger

    from mini_gym_learn.ppo import Runner
    from mini_gym.envs.wrappers.history_wrapper import HistoryWrapper
    from mini_gym_learn.ppo.actor_critic import AC_Args
    from mini_gym_learn.ppo.ppo import PPO_Args
    from mini_gym_learn.ppo import RunnerArgs

    config_mini_cheetah(Cfg)

    env = VelocityTrackingEasyEnv(sim_device='cuda:0', headless=False, cfg=Cfg)

    # log the experiment parameters
    logger.log_params(AC_Args=vars(AC_Args), PPO_Args=vars(PPO_Args), RunnerArgs=vars(RunnerArgs),
                      Cfg=vars(Cfg))

    env = HistoryWrapper(env)
    gpu_id = 0
    runner = Runner(env, device=f"cuda:{gpu_id}")
    runner.learn(num_learning_iterations=4000, init_at_random_ep_len=True, eval_freq=100)


if __name__ == '__main__':
    from pathlib import Path
    from ml_logger import logger
    from mini_gym import MINI_GYM_ROOT_DIR

    stem = Path(__file__).stem
    logger.configure(logger.utcnow(f'rapid-locomotion/%Y-%m-%d/{stem}/%H%M%S.%f'),
                     root=Path(f"{MINI_GYM_ROOT_DIR}/runs").resolve(), )
    logger.log_text("""
                charts: 
                - yKey: train/episode/rew_total/mean
                  xKey: iterations
                - yKey: train/episode/command_area/mean
                  xKey: iterations
                - type: video
                  glob: "videos/*.mp4"
                """, filename=".charts.yml", dedent=True)

    # to see the environment rendering, set headless=False
    train_mc(headless=True)

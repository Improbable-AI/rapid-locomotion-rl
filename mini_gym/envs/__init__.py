import gym

gym.envs.register(
    id="VelocityTrackingEasyEnv-v0",
    entry_point='mini_gym.envs.mini_cheetah.velocity_tracking:VelocityTrackingEasyEnv',
    max_episode_steps=10e30,
    kwargs={'physics_engine': "SIM_PHYSX", 'sim_device': 'cuda:0', 'headless': True}
)
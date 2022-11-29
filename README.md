# Code for Rapid Locomotion via Reinforcement Learning

This repository provides an implementation of the paper:


<td style="padding:20px;width:75%;vertical-align:middle">
      <a href="https://arxiv.org/pdf/2205.02824.pdf">
      <b> Rapid Locomotion via Reinforcement Learning </b>
      </a>
      <br>
      <a href="https://gmargo11.github.io/" target="_blank">Gabriel B. Margolis</a>*,  <a href="https://www.episodeyang.com/" target="_blank">Ge Yang</a>*, <a href="https://kartikpaigwar.github.io/" target="_blank">Kartik Paigwar</a>,
      <a href="https://taochenshh.github.io/" target="_blank">Tao Chen</a>, and <a href="https://people.csail.mit.edu/pulkitag" target="_blank">Pulkit Agrawal</a>
      <br>
      <em>Robotics: Science and Systems</em>, 2022
      <br>
      <a href="https://arxiv.org/pdf/2205.02824.pdf">paper</a> /
      <a href="#bibtex">bibtex</a> /
      <a href="https://agility.csail.mit.edu/" target="_blank">project page</a>
    <br>
</td>

<br>

This environment builds upon the [legged gym environment](https://leggedrobotics.github.io/legged_gym/) by Nikita
Rudin, Robotic Systems Lab, ETH Zurich (Paper: https://arxiv.org/abs/2109.11978) and the Isaac Gym simulator from 
NVIDIA (Paper: https://arxiv.org/abs/2108.10470). Training code builds upon the 
[rsl_rl](https://github.com/leggedrobotics/rsl_rl) repository, also by Nikita
Rudin, Robotic Systems Lab, ETH Zurich. All redistributed code retains its
original [license](LICENSES/legged_gym/LICENSE).

Our initial release provides the following features:
* Support for the MIT Mini Cheetah and Unitree Go1 robots.
* Implementation of the Grid Adaptive Curriculum strategy from [RLvRL](https://arxiv.org/pdf/2205.02824.pdf).
* Implementation of the teacher-student training approach from [RLvRL](https://arxiv.org/pdf/2205.02824.pdf), which is based on [Rapid Motor Adaptation](https://arxiv.org/abs/2107.04034).
* Support for scaling experiment management with [ml_logger](https://github.com/geyang/ml_logger) and [jaynes](https://github.com/geyang/jaynes-starter-kit).

## Quick Start

**CODE STRUCTURE** The main environment for simulating a legged robot is
in [legged_robot.py](mini_gym/envs/base/legged_robot.py). The default configuration parameters including reward
weightings are defined in [legged_robot_config.py::Cfg](mini_gym/envs/base/legged_robot_config.py).

There are three scripts in the [scripts](scripts/) directory:

```bash
scripts
├── __init__.py
├── play.py
├── test.py
└── train.py
```

You can run the `test.py` script to verify your environment setup. If it runs then you have installed the gym
environments correctly. To train an agent, run `train.py`. To evaluate a pretrained agent, run `play.py`. We provie a
pretrained agent checkpoint in the [./runs/](.

### Option A: Using Docker

The recommended way to run the code is to use the docker image. We provide
a [Dockerfile](docker/Dockerfile). To build the docker image, use a Ubuntu 18.04 or Ubuntu 20.04 machine, and
follow these steps:

1. Clone this repository
2. Obtain `IsaacGym_Preview_3_Package.tar.gz` from the NVIDIA website (https://developer.nvidia.com/isaac-gym). You'll
   have to create a free NVIDIA account. After downloading the file, place it in this repo
   at: `docker/rsc/IsaacGym_Preview_3_Package.tar.gz`.
3. Build the docker image: `cd docker && make build`
4. Launch and enter the docker container: `cd docker && make run`
5. [To enable GUI windows] In a separate terminal window, on the host machine, run `bash docker/visualize_access.bash`

### Option B: Native Installation

If you'd prefer to run our code in your own python environment, you can follow the instructions below:

#### Install pytorch 1.10 with cuda-11.3:

```bash
pip3 install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
```

#### Install Isaac Gym

1. Download and install Isaac Gym Preview 3 from https://developer.nvidia.com/isaac-gym
2. unzip the file via:
    ```bash
    tar -xf IsaacGym_Preview_3_Package.tar.gz
    ```

3. now install the python package
    ```bash
    cd isaacgym_lib/python && pip install -e .
    ```
4. Verify the installation by try running an example

    ```bash
    python examples/1080_balls_of_solitude.py
    ```
5. For troubleshooting check docs `isaacgym/docs/index.html`

#### Install the `mini_gym` package

In this repository, run `pip install -e .`

### Verifying the Installation

If everything is installed correctly, you should be able to run the test script with:

```bash
python scripts/test.py
```

The script should print `Simulating step {i}`.
The GUI is off by default. To turn it on, set `headless=False` in `test.py`'s main function call.

### Training a Model

To train the mini-cheetah robot to run and spin fast, run: 

```bash
python scripts/train.py
```

After initializing the simulator, the script will print out a list of metrics every ten training iterations.

Training with the default configuration requires about 12GB of GPU memory. If you have less memory available, you can 
still train by reducing the number of parallel environments used in simulation (the default is `Cfg.env.num_envs = 4000`).

To visualize training progress, first start the ml_dash frontend app:
```bash
python -m ml_dash.app
```
then start the ml_dash backend server by running this command in the parent directory of the `runs` folder:
```bash
python -m ml_dash.server .
```

Finally, use a web browser to go to the app IP (defaults to `localhost:3001`) 
and create a new profile with the credentials:

Username: `runs`
API: [server IP] (defaults to `localhost:8081`)
Access Token: [blank]

Now, clicking on the profile should yield a 

### Evaluating the Model

To evaluate the most recently trained model, run:

```bash
python scripts/play.py
```

The robot is commanded to run forward at 5m/s for 5 seconds. After completing the simulation, 
the script plots the robot's velocity and joint angles. To modify the commanded velocity, you can edit 
[line 109 of the script](https://github.com/gmargo11/model-free-agility/blob/main/scripts/play.py#L109). 

The GUI is on by default. 
If it does not appear, and you're working in docker, make sure you haven't forgotten to run `bash docker/visualize_access.bash`.


## Support

For questions about the code, please create an issue in the repository.

## Bibtex <a name="bibtex"></a>

```
@inproceedings{margolisyang2022rapid,
  title={Rapid Locomotion via Reinforcement Learning},
  author={Margolis, Gabriel and Yang, Ge and Paigwar, 
          Kartik and Chen, Tao and Agrawal, Pulkit},
  booktitle={Robotics: Science and Systems},
  year={2022}
}
```

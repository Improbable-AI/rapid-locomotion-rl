# syntax=docker/dockerfile:experimental

FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

# add new sudo user
ENV USERNAME isaac
ENV HOME /home/$USERNAME
RUN useradd -m $USERNAME && \
        echo "$USERNAME:$USERNAME" | chpasswd && \
        usermod --shell /bin/bash $USERNAME && \
        usermod -aG sudo $USERNAME && \
        mkdir /etc/sudoers.d && \
        echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME && \
        chmod 0440 /etc/sudoers.d/$USERNAME && \
        # Replace 1000 with your user/group id
        usermod  --uid 1000 $USERNAME && \
        groupmod --gid 1000 $USERNAME

# install package
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        sudo \
        less \
        emacs \
        apt-utils \
        tzdata \
        git \
        tmux \
        bash-completion \
        command-not-found \
        libglib2.0-0 \
        gstreamer1.0-plugins-* \
        libgstreamer1.0-* \
        libgstreamer-plugins-*1.0-* \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
 libxcursor-dev \
 libxrandr-dev \
 libxinerama-dev \
 libxi-dev \
 mesa-common-dev \
 zip \
 unzip \
 make \
 gcc-8 \
 g++-8 \
 vulkan-utils \
 mesa-vulkan-drivers \
 pigz \
 git \
 libegl1 \
 git-lfs

# WAR for eglReleaseThread shutdown crash in libEGL_mesa.so.0 (ensure it's never detected/loaded)
# Can't remove package libegl-mesa0 directly (because of libegl1 which we need)
RUN rm /usr/lib/x86_64-linux-gnu/libEGL_mesa.so.0 /usr/lib/x86_64-linux-gnu/libEGL_mesa.so.0.0.0 /usr/share/glvnd/egl_vendor.d/50_mesa.json

COPY nvidia_icd.json /usr/share/vulkan/icd.d/nvidia_icd.json
COPY 10_nvidia.json /usr/share/glvnd/egl_vendor.d/10_nvidia.json


RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

#COPY config/nvidia_icd.json /usr/share/vulkan/icd.d/

RUN apt-get -y update && apt-get install -y git vim tree curl unzip xvfb patchelf ffmpeg cmake swig
RUN apt-get install -y libssl-dev libcurl4-openssl-dev  # Needed for pyCurl
RUN apt-get install -y libglu1-mesa-dev libgl1-mesa-dev libosmesa6-dev
RUN apt-get install -y cmake libopenmpi-dev python3-dev zlib1g-dev
RUN apt-get install -y qtbase5-dev
RUN apt-get install -y qtdeclarative5-dev
RUN apt-get install -y libglib2.0-0


RUN apt-get install -y libssl-dev libcurl4-openssl-dev
RUN apt-get install -y python3.8-dev python3-pip

RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN python -m pip install --upgrade pip
ENV PIP_NO_CACHE_DIR=off

# install Isaac SDK
USER root

COPY ./rsc/IsaacGym_Preview_3_Package.tar.gz /home/$USERNAME/
RUN cd /home/$USERNAME && tar -xvzf IsaacGym_Preview_3_Package.tar.gz

RUN cd /home/$USERNAME/isaacgym/python && pip3 install -e .

RUN apt-get -y update && apt-get install -y git vim tree curl unzip xvfb patchelf ffmpeg cmake swig
RUN apt-get install -y libssl-dev libcurl4-openssl-dev  # Needed for pyCurl
RUN apt-get install -y libglu1-mesa-dev libgl1-mesa-dev libosmesa6-dev
RUN apt-get install -y cmake libopenmpi-dev python3-dev zlib1g-dev
RUN apt-get install -y qtbase5-dev
RUN apt-get install -y qtdeclarative5-dev
RUN apt-get install -y libglib2.0-0
RUN apt-get install -y tcl-dev tk-dev

RUN pip install tensorboard
RUN pip install cycler python-dateutil kiwisolver pyparsing matplotlib

RUN pip install torch==1.10.0+cu113 torchvision==0.11.0+cu113 torchaudio==0.10.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install gym==0.19.0
RUN pip install pytest pytest-forked lz4 pyyaml qt5-py
RUN pip install gym3

RUN pip install scikit-build
RUN pip install kornia opencv-python
RUN pip install filelock

# RUN apt-get install -y software-properties-common
RUN apt-get install -y libgl1-mesa-glx libosmesa6
RUN apt-get install -y libglew-dev
## used for egl rendering
#ENV LD_PRELOAD /usr/lib/x86_64-linux-gnu/libGLEW.so
#:/usr/lib/x86_64-linux-gnu/libGL.so.1

RUN pip install jaynes ml_logger waterbear params-proto functional-notations --no-cache-dir

RUN pip install lcm
RUN apt-get install htop

RUN pip install scikit-image
RUN apt-get install -y python3-tk

# LCM
#RUN cd /home/$USERNAME && git clone https://github.com/lcm-proj/lcm.git && cd lcm && mkdir build && cd build && cmake .. && make -j && make install
#RUN apt-get install -y net-tools && pip install netifaces

#misc
RUN pip install cmx
RUN pip install functional_notations
RUN pip install pandas
RUN pip install tqdm
RUN pip install --upgrade ml_logger jaynes
RUN pip install ml_dash

ENV ISAAC_PREFIX=/home/isaac
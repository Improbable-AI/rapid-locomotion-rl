#!/bin/bash
set -e

cd /home/isaac/rapid-locomotion-rl && pip install -q -e .
export PYTHONPATH=$PYTHONPATH:~/rapid-locomotion-rl

eval "bash"

exec "$@"

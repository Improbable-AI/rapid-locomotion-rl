default: build
build:
	docker build -t rapid-locomotion-rl .
clean-build:
	docker build -t rapid-locomotion-rl . --no-cache=true
run:
	#docker run legged-gym
	docker run -it \
	    --env="DISPLAY" \
	    --env="QT_X11_NO_MITSHM=1" \
	    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
	    --env="XAUTHORITY=${XAUTH}" \
	    --volume="${XAUTH}:${XAUTH}" \
	    --volume="/$(shell pwd)/../:/home/isaac/rapid-locomotion-rl" \
	    --privileged \
	    --runtime=nvidia \
	    --net=host \
	    --workdir="/home/isaac/rapid-locomotion-rl" \
	    rapid-locomotion-rl /home/isaac/rapid-locomotion-rl/docker/entrypoint.sh

#!/bin/sh
echo Setting env vars

export ubuntu_ver=22.04 # For docker image pulling
export ocv_ver=4.8.0 # OpenCV version for wget, cmake configuration, install and post-install commands
export build_thread_count=$(expr $(nproc) - 1)
export image_tag=stud1_opencv_custom
export dockerfile=OpenCVDockerFile.dockerfile

# Check if image is existed before pulling
if docker image inspect ubuntu:$ubuntu_ver 1>/dev/null; then
  echo "Docker image ubuntu:$ubuntu_ver is found."
else
  echo "Pulling docker image ubuntu:$ubuntu_ver..."
  docker pull ubuntu:$ubuntu_ver
fi

echo Building docker
docker build --tag $image_tag \
          --build-arg ubuntu_ver=$ubuntu_ver \
    		 --build-arg ocv_ver=$ocv_ver \
    		 --build-arg build_thread_count=$build_thread_count \
    		 -f $dockerfile .
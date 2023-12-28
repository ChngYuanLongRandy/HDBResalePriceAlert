# base image for arm64 since we are running on raspberry pi4
FROM --platform=linux/arm64 python:3.12.1-bullseye

# arguments
ARG REPO_DIR="."
ARG PROJECT_USER="randy"
ARG HOME_DIR="/home/$PROJECT_USER"
ARG DESTINATION_FOLDER="hdb"

# install chromedriver
RUN apt-get update && apt-get upgrade -y 
RUN apt-get install chromium-driver -y

WORKDIR $HOME_DIR

# # install chromium-chromedriver
RUN apt-get update --allow-releaseinfo-change && apt-get install chromium-driver -y

# The copy is from local (where the docker command is executed) to this 
COPY $REPO_DIR $DESTINATION_FOLDER

# install requirements
RUN pip3 install -r $DESTINATION_FOLDER/app/run-requirements.txt

# run as non-root
RUN groupadd -g 2222 $PROJECT_USER && useradd -u 2222 -g 2222 -m $PROJECT_USER
RUN chown -R 2222:2222 $HOME_DIR && \
    rm /bin/sh && ln -s /bin/bash /bin/sh
USER 2222

# start from this workdir
WORKDIR $HOME_DIR/${DESTINATION_FOLDER}

# execute python file upon running container
CMD [ "python3", "app/app.py" ]
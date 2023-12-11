FROM python:3.12.1-bullseye

ARG REPO_DIR="."
ARG PROJECT_USER="randy"
ARG HOME_DIR="/home/$PROJECT_USER"
ARG DESTINATION_FOLDER="hdb"

WORKDIR $HOME_DIR

# The copy is from local (where the docker command is executed) to this 
COPY $REPO_DIR $DESTINATION_FOLDER

RUN pip install -r $DESTINATION_FOLDER/app/run-requirements.txt

RUN groupadd -g 2222 $PROJECT_USER && useradd -u 2222 -g 2222 -m $PROJECT_USER
RUN chown -R 2222:2222 $HOME_DIR && \
    rm /bin/sh && ln -s /bin/bash /bin/sh
USER 2222

WORKDIR $HOME_DIR/${DESTINATION_FOLDER}

CMD [ "python3 app/app.py" ]
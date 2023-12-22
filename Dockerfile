FROM --platform=linux/arm64 python:3.12.1-bullseye
# FROM python:3.12.1-bullseye


ARG REPO_DIR="."
ARG PROJECT_USER="randy"
ARG HOME_DIR="/home/$PROJECT_USER"
ARG DESTINATION_FOLDER="hdb"

WORKDIR $HOME_DIR

# # install chrome browser (works for x86)
# RUN apt-get install -y wget
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
#     && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# RUN apt-get update && apt-get -y install google-chrome-stable

# install chrome browser arm64
# install manually all the missing libraries
RUN apt-get update -y
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

# install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# The copy is from local (where the docker command is executed) to this 
COPY $REPO_DIR $DESTINATION_FOLDER

RUN pip install -r $DESTINATION_FOLDER/app/run-requirements.txt

RUN groupadd -g 2222 $PROJECT_USER && useradd -u 2222 -g 2222 -m $PROJECT_USER
RUN chown -R 2222:2222 $HOME_DIR && \
    rm /bin/sh && ln -s /bin/bash /bin/sh
USER 2222

WORKDIR $HOME_DIR/${DESTINATION_FOLDER}

CMD [ "python3", "app/app.py" ]
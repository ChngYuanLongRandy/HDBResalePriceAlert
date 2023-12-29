# HDBResalePriceAlert

## What is
Email subscription service for HDB resale prices for the latest 6 months record

## How does it work
Front end is built with JavaScript
Backend is built with Python-Flask. It uses selenium to scrape the results from the HDB website
DB is on mysql. Docker image is meant for the raspberrypi.

## Why build it
I want something to inform me of any latest transaction in places that I am interested in - mainly my own residential unit. I do not want to be going to HDB website and clicking on it all the time and I prefer to be updated by email and that's how this service was born.

## Where to host it
This is primarily intended to be run on a raspberrypi server but can be configured to run on any other servers. 

## How to run this
### Development
- Install conda environment `conda env create -f conda.yml`
- activate conda environment `conda activate hdb-resale-alert-env`
- run flask application `python app/app.py`
- launch localhost:5000

### Testing in Server without docker image

Note that the commands below may be a bit wonky since I used sqlite3 for development and then switched to mysql for production

- Run commands below
- activate environment
- Run flask command `python app/app.py`

```
# update system
sudo apt-get update
sudo apt-get upgrade
sudo reboot

# git repo
git clone https://github.com/ChngYuanLongRandy/HDBResalePriceAlert.git

# for raspberypi 4
python3 -m venv env

# install python packages
pip3 install -r requirements.txt

# some numpy installation issue
sudo apt-get install libopenblas-dev

pip3 install --upgrade --force-reinstall numpy

# Chrome driver
sudo apt-get install chromium-chromedriver
```

### Running in Server with docker-compose

- create docker-compose.yaml file with template below
- place in root and run `docker-compose up`
- Connect to port localhost:5000

```
Docker-compose.yaml
version: '3'

services:
  mysql:
    image: mysql:latest
    expose:
      - 3306
    networks:
      - hdb_alert_network
    environment:
      MYSQL_HOST: mysql
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - /path/from/your/volume:/var/lib/mysql

  python_app:
    image: hashketh/hdb-alert:0.1linuxarm64-dbconfig
    networks:
      - hdb_alert_network
    ports:
      - "5000:5000"
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_HOST: mysql
      MYSQL_PORT: 3306
    depends_on:
      - mysql
    volumes:
      - /path/from/your/volume:/app  # Mount your Python application code

volumes:
  mysql_data:
networks:
  hdb_alert_network:

```
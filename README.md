# Transmission telegram bot

Telegram bot for Searching torrents and passing to Transmission torrent server.

Supported trackers:
* http://nnmclub.to/
* http://rutor.info 
* https://rutracker.org
* https://eztv.re/
* https://kat.sx/

(new will arrive soon)

## Features
1. Search torrents on trackers and passing to Transmission.
2. Direct send torrent files and magnet urls to transmission server for download.
3. Essentials Transmission server actions such as Stop, Start, Delete, View info.

# Usage

This Bot could be used as satelite for Transmission server for search torrent files on predifined web sites. 
Additionally you could setup home DLNA server like Jellyfin or MiniDLNA.

Before building docker image or running python script please register new telegram bot using `BotFather`.
Place bot security token into torrents.ini.

## Preparation
1. Install and configure transmission server web interface with username and password.
   You could use docker image https://hub.docker.com/r/linuxserver/transmission instead of manual (rpm/deb) setup.
   Please check `docker-compose.yaml`
2. Update torrentino.ini configuration file.

## Run python script

1. Clone this repository
2. Update configuration file:
   ```
   # check comments inside the file
   torrentino.ini
   ```
3. Run:
   ```
   pip install -r requirements.txt
   python torrentino.py
   ```

## Run in docker


1. Build docker image:
   ```
   docker build -t my-bot . 
   ```
2. Start docker container as daemon process:
   ```
   docker run -d -v `pwd`/torrentino.ini:/usr/src/app/torrentino.ini my-bot
   ```
3. Check container logs.



## Home DLNA on Raspberry Pi4 setup guide

This section describes how to build home DLNA solution on Raspberry Pi4 with external HDD. 

### Hardware list:

1. Raspberry Pi4 device (4G RAM).
2. External HDD formatted as `ext4` (this guide use `/data/Media` as mountpoint). 

### Software list:

1. Docker with docker-compose. Guides how to setup docker and docker-compose could be found online.
2. Jellyfin docker imagei https://hub.docker.com/r/linuxserver/jellyfin (https://jellyfin.org/).
3. Transmission docker image https://hub.docker.com/r/linuxserver/transmission (https://transmissionbt.com/).
4. Transmission telegram bot docker image built from this repo.


### Installation steps

1. Create folders inside `/data/Media` to organize your data.
For example: Video, TVShows, Soft, Music.:
```
mkdir -p /data/Media/{Video,TVShows,Soft,Music}
```
2. Create dedicated user `dlna` for running docker containers and make this user owner of `/data/Media`:
```
sudo useradd -m -G docker dlna
sudo chown -R dlna:dnla /data/Media
```
3. Login as `dlna` user: 
```
sudo su - dlna
```
4. Clone this git repo into home folder and build transmission-telegram-bot docker image:
```
git clone https://github.com/adskyiproger/transmission-telegram-bot.git
cd transmission-telegram-bot/
docker build -t transmission-telegram-bot .
```
5. Navigate back into home directory and create directory structure to persist docker containers data:
```
cd ~
mkdir -p docker/{jellyfin,torrentino,transmission}/config
```
6. Copy Bot configuration file `torrentino.ini.docker` into `~/docker/torrentino/config` and create empty log file:
```
cp ~/transmission-telegram-bot/torrentino.ini.docker ~/docker/torrentino/config/torrentino.ini
touch docker/torrentino/torrentino.log
```
7. Open `~/docker/torrentino/config/torrentino.ini` in text editor and update `TOKEN` and `ALLOWED_USERS` variables.
8. Copy docker-compose.yaml into `~/docker` directory
```
cp ~/transmission-telegram-bot/docker-compose.yaml docker/
```
9. Update `PUID`, `PGID` variables. Please also update other variables that are not defaults.
10. Run everything:
```
cd ~/docker
docker-compose up -d
```
11. Login into Jellyfin web UI and configure DLNA folders.


### Environemnt description

* Jellyfin web interface is available at `http://<Pi4 hostname or ip>:8096`
* Transmission web interface is available at `http://<Pi4 hostname or ip>:9091`


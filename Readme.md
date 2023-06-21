# Music-Room-Web-App-Django-React

The project is made using django and react.
The users can join a music room using room code to control the host's spotify player.
Users can play and pause the song if host has permitted it.
Users can vote for skipping the song. 

## Setup Instructions

### Clone the repository

```bash
git clone https://github.com/lalitware/music-player-web-app-django-react.git
cd music-player-web-app-django-react
```
### Create and activate the python environment

```bash
python3 -m venv env
source env/bin/activate
```
### Install Required Python Modules

```bash
pip install -r requirements.txt
```
### Create .env file to store environment variables and add your spotify credentials

```bash
cp .env-sample .env
```
### Add your spotify credentials and other details to .env file (ctrl + O and ctrl + X to save changes)

```bash
nano .env
```
### Migrate the database models.

```bash
python manage.py migrate
```

### Start Web Server

To start the web server you need to run the following sequence of commands.

Go to the root directory.
```bash 
cd music-player-web-app-django-react
```
Next run the django web server.
```bash
python manage.py runserver
```

### [Install Node.js](https://nodejs.org/en/)

### Install Node Modules

First cd into the ```frontend``` folder.
```bash
cd frontend
```
Next install all dependicies.
```bash
npm i
```

### Compile the Front-End

Run the production compile script
```bash
npm run build
```
or for development:
```bash
npm run dev
```
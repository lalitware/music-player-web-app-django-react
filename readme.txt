AIM: To create a music web application using djnago and react.
Tutor: Tech with Tim
Youtube link: https://www.youtube.com/playlist?list=PLzMcBGfZo4-kCLWnGmK0jUBmGLaJxvi4j 
github link: https://github.com/techwithtim/Music-Controller-Web-App-Tutorial 

Fetaures: 
  a. To create a music room where the people in the room will be able to control the music player of the host.
  b. Room will be joined using the room code.

Steps:
  1. vscode extensions -> prettier(prettier.io), python(microsoft), django(Baptiste Darthenay), react(dsznajder), javascript(charalampos karypidis)
  
  #### Backend Setup #####
  2. install pip -> check pip --version.
  3. install django and django framework:
    pip install django djangorestframework
  4. create django project -> django-admin startproject musicapp .
  5. create app to handle api:
    a. django-admin startapp api
    b. add the app.apps.ApiConfig class in INSTALLED_APPS list in settings.py
  6. add rest_framework in INSTALLED_APPS list in settings.py
  7. create api.views.main().
  8. create path in musicapp.urls.py to send all the requests to api.urls.py:
    path('', include('api.urls')),
  9. create api.urls.py and define the url pattern to point them to api.views.main() function.
    path('', views.main),
  10. make and run migrations for initial db setup:
    python manage.py makemigrations
    python manage.py migrate
  11. create Room model and function to generate unique code in api.models.py
  12. make and run migrations.
  13. create serializers.py to mention the fields to expose in api.
  14. create RoomView class by extending generics.ListAPIView in api.views.py to view the list of rooms.
  
  #### Frontend Setup (Hard way - manual setup instead of react-app command)####
  15. create frontend app to store all the frontend related informations
    django-admin startapp frontend
    also add 'frontend.apps.FrontendConfig' inside settings.py
  16. run 'npm init -y' -> this will create package.json inside frontend directory.
  17. create src/components, templates, and static/css static/images static/frontend directories in frontend
  18. npm i webpack webpack-cli --save-dev -> this will create package-lock.json
  19. npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev -> to run in older browsers as well.
  20. npm i react react-dom --save-dev -> to install react.
  21. npm install npm install @mui/material @emotion/react @emotion/styled  -> to install material-ui
  22. npm install @babel/plugin-proposal-class-properties -> to have async and await in js code.
  23. npm install react-router-dom -> to reroute the pages
  24. npm install npm install @mui/icons-material
  25. To run configurations script tp handle webpack and babel:
    a. create a babel.config.json file in frontend directory.
    b. copy the script from https://github.com/techwithtim/Music-Controller-Web-App-Tutorial/blob/main/Tutorial%201%20-%204/frontend/babel.config.json
    c. create webpack.config.js file in frontend directory -> to bundle the javascript in one file and serve to the browser.
    d. copy the script from https://github.com/techwithtim/Music-Controller-Web-App-Tutorial/blob/main/Tutorial%201%20-%204/frontend/webpack.config.js
  26. mention the scripts in package.json in scripts:
    "scripts": {
      "dev": "webpack --mode development --watch",
      "build": "webpack --mode production"
    },
  27. create index.js inside src.
  28. django will render the .html and then react will take over that.
  29. create templates/frontend/index.html file. and below divs in the body.
    <div id="main">
      ##### react code will go inside the below div so that react can grap the app div where it will render all its components. #### 
      <div id="app"></div>
    </div>
    <script src="{% static 'frontend/main.js' %}"></script>
  30. define frontend.views.index() function to render frontend/index.html
  31. create frontend.urls.py and add the url to point above index() function.
    path('', views.index()),
  32. also add empty path in musicapp.urls.py.
    path('', include('frontend.urls')),
  33. create a component in src/components/App.js
  34. put the app component inside src/index.js to work.
    import App from "./components/App";
  35. run the server and then run the script (maksure we are in frontend directory) that is inside package.json
    python manage.py runserver
    npm run dev -> this will create frontend/static/frontend/main.js
  
  #### Building the react app ####
  36. create frontend/static/css/index.css file.
  37. create a component HomePage.js in src/components and import it in App.js

  ## Just to check how components render add all of them to App.js temporarly. ##
  38. create a component src/components/RoomJoinPage.js and import it in App.js
  39. create a component src/components/CreateRoomPage.js and import it in App.js

  40. import RoomJoinPage and CreateRoomPage in HomePage.js and remove both of them from App.js
  41. add the path to frontend.urls.py:
    path('join/', index),
    path('create/', index),
  42. create CreateRoomSerializer class in api/serializers.py to send post request to the endpoints.
  43. create a class CreateRoomView in api.views.py
  44. import components from and @mui/material and create the webpage in CreateRoomPage.js
  45. Use state to send the form data to backend.
  46. Use fetch method to send the post request to create-room api.
  47. create a component src/components/Room.js to read and display the music room data.
  48. create route for room page in HomePage.js:
    <Route path="/room/:roomCode" element={<Room />} />
  49. also add the room url in frontend.urls.py:
    path('room/<str:room_code>', index),
  50. Create class GetRoom in api.views.py to get the data of a music room and return json response.
  51. Create getRoomDetails() in Room.js to fetch the data by requesting get-room API.
  52. To redirect the user to room page after room creation:
    a. in CreateRoomPage.js handleRoomButtonPressed() redirect to room page:
      this.props.history.push("/room/" + data.code)
  53. update index.css to center the the pages.
  54. update RoomJoinPage.js page.
  55. create a class view RoomJoin to allow user to join a room in api.views.py.
  56. create url path to point RoomJoin view to join-room endpoint:
    path('join-room/', views.JoinRoom.as_view(), name='join_room'),
  57. send the post request from the frontend RoomJoinPage.roomButtonPressed() method
  58. style the HomePage.js to navigate to create room and join room pages if not joined any room yet.
  59. If already joined any room then redirect the user to the room instead of home page:
    use useEffect hook to request an api to check.
  60. create an api endpoint user-in-room to point it to api.views.UserInRoom view that will check if user aleady in a music room.
  61. create path url for the user-in-room endpoint in api.urls.py.
  62. style the room page and add leave room link in Room.js.
  63. Create a method leaveButtonPressed to leave the current room.
  64. Create an api endpoint leave-room to point api.views.LeaveRoom to leave the current music room.
  65. create path url for the leave-room endpoint in api.urls.py.
  66. Settings page for room host by resuing and modifying the CreateRoomPage component:
    a. create a view UpdateRoom for update-room patch api in api.views.py.
    b. create a serializer class UpdateRoomSerializer in serializers.py.
    c. point the UpdateRoom view to update-room endpoint in api.urls.py.
    d. add the settings button in Room page by adding one more state showSettings.
    e. make a method to check if the current user is the host and set the showSettings state to true for him.
    f. to create the CreateRoomPage component reusable.
    g. install material ui's lab library for better alert messages:
      npm install @mui/lab
  67. Create spotify app for spotify api integration:
    a. python manage.py startapp spotify and mention it in INSTALLED_APPS im settings.py-> 'spotify.app.SpotifyConfig'.
    b. create spotify.urls.py
    c. create credentials.py -> to store spotify credentials.
    d. create a view class AuthURL in spotify.views.py to provide frontend auth URL for spotify authemtication.
    f. point the view to a endpoint in spotify.urls.py:
      path('get-auth-url/', views.AuthURL.as_view(), name='get_auth_url'),
    g. set up url for spotify app in musicapp.urls.py:
      path('spotify-api/', include('spotify.urls')),
    h. create a callack view spotify_callback for redirect_url where spotify will redirect us after the authemtication is done and to get access token and refresh token.
    i. create a model to store the users access token and refresh token corresponding to the session_key:
      i. create a model class SpotifyToken in spotify.models.py
        fields: user, created_at, refresh_token, access_token, expires_in, token_type
      ii. make migratiosns -> python manage.py makemigrations
      iii. run migrations -> python manage.py migrate
    j. store the token info in the SpotifyToken table:
      i. create spotify.utils.py
      ii. create a function spotify.utils.update_or_create_user_token()
      iii. call the above function in the spotify.views.spotify_callback()
      iv. redirect to frontend home page:
        return redirect('frontend:home')
      v. create a redirect path in spotify.urls.py to give spotify a redirect url:
        path('redirect/', views.spotify_callback)
        also add http://127.0.0.1:8000/spotify-api/redirect/ in spotify for callack url.
        same url should be added to REDIRECT_URI in spotify.credentials.py
      vi. add the name of app in frontend.urls.py 
        app_name = 'frontend'
      vii. name the home page of frontend app as home:
        path('', index, name='home'),
    k. create a function is_spotify_authenticated in spotify.utils.py to check users authentication.
    l. create a function refresh_spotify_token in spotify.utils.py to refresh the access token 
      and update the token data in the db and call it in above method if token is expired.
    m. create a class view CheckOrUpdateAuth that will be check or update the authentication.
    n. Create check-update-auth endpoint to point it to CheckOrUpdateAuth in spotify.urls.py
    o. Just after entering the room and if user is the host then authenticate to take contol of the room:
      i. add a state spotifyAuthenticated in Room component.
      ii. create a methos autheticateSpotify() in Room.js for authemtication.
  68. Get the current song:
    a. create view class CurrentSong in spotify.views.py to return current playing song information. 
    b. create a function execute_spotify_api_request if spotify.utils.py to request the spotify api.
    c. call the execute_spotify_api_request in CurrentSong view.
    d. create url endpoint to point the CurrentSong view.
    e. Update the room UI in Room.js and add song state.
    f. create a function getCurrentSong to fetch the current playing song data using get-current-song/ API.
    g. continuously check the latest getCurrentSong response using javascript polling.
      i. use setInterval for get response after every 1 second in useEffect of Room.js.
      ii. also return and call clearInterval in the useEffect
  69. Create Music Player Component.
    a. creaet MusicPlayer.js in frontend/src/components.
    b. Style the component.
    c. access the song info got from getCurrentSong in MusicPlayer using prop.
    d. import this component in Room.js.
  70. Working pause and play button from our web app.
    i. create view PlayOrPauseSong in spotify.views.py
    ii. create put method to update the state of the song to play or pause.
    iii. create play_or_pause_song function in spotify.utils.py and call it in the above put methos.
    iv. create url endpoint to point PlayOrPauseSong in spotify.urls.py
    v. send a request to play-or-pause-song/ endpoint from MusicPlayer.js
  71. To handle the cases when song is not being played or the spotify player is not active:
    a. return different jSX for these cases in MusicPlayer.js.
    b. add a default static image:
      i. add the image in the src of image tag.
        import image from '../../static/images/stay-tuned.jpg';
      ii. add a rule in webpack.congif.js 
        {
          test: /\.(png|jpe?g|gif)$/i,
          type: 'asset/resource',
          generator: {
            filename: 'static/images/[name][ext]',
          },
        },
  72. Skipping the song based on user votes.
    a. create SkipToNextSong view for post api to skip the song.
    b. create skip_to_next_song function in utils.py and call in the above view.
    c. create a url endpoint skip-to-next-song/ to point it to SkipToNextSong.
    d. For non host user votes are required to skip the song
      i. create a model to store the votes in spotify.models.py with fields -> user, created_at, room(ForeignKey), song_id
      ii. add a current_song field in Room Model.
      iii. make and run migrations
      iv. in CurrentSong view write a logic which add the song_id in current_song field in Room model.
      v. In SkipToNextSong view add a logic to create a vote object if non host clicks on skip button.
      vi. pass the votes_count and votes_required in CurrentSong API.
    e. update the MusicPlayer.

  73. Skip and Pause put requests to spotify requires premium version of spotify.

  74. To connect the mobile devices to access the localhost website over the wifi network.
    a. python manage.py runserver 0.0.0.0:8000
    b. add the local ip address in ALLOWED_HOSTS list in settings.py check you local ip 'ip addr show'
      ALLOWED_HOSTS = ['127.0.0.1', 'local ip address got from above command', '0.0.0.0:8000']
    c. configure ubuntu firewall:
      sudo ufw allow 8000
    d. add the callback in spotify configurations and in credentials.py
    e. visit the website http://<your-ubuntu-ip-address>:8000


  ######### Deploy on Digital Ocean #########
  1. If environment was not created while developing the app then follow below steps to create virtual environment and install dependencies:
    a. pip install pipreqs
    b. 'pipreqs --force .' -> this will create requirements.txt file.
    c. pip install venv
    d. python3 -m venv env
    e. source env/bin/activate
    f. pip install -r requirements.txt
  2. To secure the sensitive configurations using python-decouple:
    a. pip install python-decouple
    b. create .env file and add all the environment variables in key value form check .env-sample.
    c. 'from decouple import config' in settings.py
    d. get the variables using config methods.
  3. Create .gitignore file for django from gitignore.io
  4. Create github repository and push the code to github.
  5. Create DigitalOcean droplet uisng ubuntu machine.
  6. choose ssh and generate public key:
    a. Create a new key pair:
      ssh-keygen
    b. let the location be as it is and enter the passphrase for key
    c. copy the public key and paste it to the ssh-key-content in droplet-> settings-> security->edit
      cat ~/.ssh/id_rsa.pub
    d. save the ssh key
    e. open local machine terminal and check if ~/.ssh/id_rsa has only one
    f. run 'ssh root@ip-address' -> copy the ip address from droplet.
    g. if the above command gives permission denied then do the following:
      i. chmod 700 ~/.ssh
      ii. chmod 600 ~/.ssh/*
      iii. eval "$(ssh-agent -s)" -> To first start the ssh agent
      iv. ssh-add -> To then add the ssh key
      v. run 'ssh root@ip-address' again it should work.
  7. Now Set up the environemnt:
    a. sudo apt update
    b. sudo apt upgrade
    c. check python version
    d. apt install nodejs
    e. apt install python3-pip
    f. apt install npm
    g. Create new user:
      i. adduser your_username
      ii. usermod -aG sudo your_username -> Grant administrative privileges to the new user
      iii. su - your_username -> Switch to the new user
    h. connect with github ssh repeat the same steps as 6.
    i. create directory sites
    j. sudo apt install python3.10-venv
    k. python3 -m venv env
    l. source env/bin/activate
    m. pip install -r requirements.txt
    n. cp project directory and cp .env-sample .env and then nano .env to paste the secrets.
    o. python manage.py migrate -> to create db tables.
    p. fontend set up:
      i. cd frontend
      ii. delete node_modeles
      iii. run 'npm install'
      iv. npm run dev
      v. npm run build
    q. domain set up:
      a. create a reserved ip for the droplet.
      b. create A record in DNS settings and point the domain to reserved ip.
    r. Set up the webserver to listen to port 80. With site is accessible without specifying the port number:
      a. currently reserved_ip:8000 is the only way to access the site.
      b. sudo apt update
      c. sudo apt install nginx
      d. to allow access to the service. Nginx registers itself as a service with ufw:
        i. sudo ufw app list
        ii. sudo ufw allow 'Nginx HTTP' -> to allow http traffic on port 80.
        iii. sudo ufw status
        iv. 'systemctl status nginx' -> check status of web server
        v. 'curl -4 icanhazip.com' -> to get public ip address
        vi. 'curl http://your_public_ip' -> it show return a page.
      e. set up Gunicorn:
        i. pip install gunicorn
        ii. gunicorn --bind 0.0.0.0:8000 <project-name>.wsgi -> to test Gunicorn.
      f. set up nginx config:
        i. Create an Nginx server block configuration file: 
          sudo nano /etc/nginx/sites-available/<project-name>
        ii. paste this and update the ip or domain:
          server {
              listen 80;
              server_name <your-domain-or-ip>;

              location / {
                  proxy_pass http://localhost:8000;
                  proxy_set_header Host $host;
                  proxy_set_header X-Real-IP $remote_addr;
                  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              }
          }
        iii. Create a symbolic link for the server block: 
          sudo ln -s /etc/nginx/sites-available/<project-name> /etc/nginx/sites-enabled/
        iv. test Nginx configuration:
          sudo nginx -t
        v. Restart Nginx:
          sudo systemctl restart nginx
      g. cd to project, activate the environment, and run the server
        'python manage.py runserver 0.0.0.0:8000'
      h. add the domain to ALLOWED_HOSTS in settings.py
    
    ########## Method 1(tmux) to keep Gunicorn run ##############
    s. To keep Gunicorn run after even after closing the ssh terminal:
      i. install tmux -> 'sudo apt install tmux'
      ii. start tmux session -> 'tmux'
      iii. navigate to project and activate the environment
      iv. gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application --daemon
      v. Detach from the tmux session:
        press 'Ctrl+B' and then release and then press 'D'
      vi to stop other running tmux sessions:
        a. tmux
        b. ps aux | grep gunicorn
        c. kill <PID>
        d. exit
    ########## Method 2(systemd socket and service) to keep Gunicorn run ##############
    https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04 
    t. To keep Gunicorn run after even after closing the ssh terminal:
      a. creating and opening a systemd socket file:
        sudo nano /etc/systemd/system/gunicorn.socket

        Paste below lines
        [Unit]
        Description=gunicorn socket

        [Socket]
        ListenStream=/run/gunicorn.sock

        [Install]
        WantedBy=sockets.target
      b. create and open a systemd service file for Gunicorn
        sudo nano /etc/systemd/system/gunicorn.service

        paste the below lines.
        [Unit]
        Description=gunicorn daemon
        Requires=gunicorn.socket
        After=network.target

        [Service]
        User=sammy
        Group=www-data
        WorkingDirectory=/home/sammy/myprojectdir
        ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
                  --access-logfile - \
                  --workers 3 \
                  --bind unix:/run/gunicorn.sock \
                  myproject.wsgi:application

        [Install]
        WantedBy=multi-user.target
      c. start and enable the Gunicorn socket:
        sudo systemctl start gunicorn.socket
        sudo systemctl enable gunicorn.socket
      d. Check the status of the process to find out whether it was able to start
        sudo systemctl status gunicorn.socket
      e. check for the existence of the gunicorn.sock file within the /run directory:
        file /run/gunicorn.sock
        expected output -> /run/gunicorn.sock: socket
      f. To test the socket activation mechanism, we can send a connection to the socket through curl by typing:
        curl --unix-socket /run/gunicorn.sock localhost

        expected output: html page.
      g. configure nginx:
        i. sudo nano /etc/nginx/sites-available/myproject:
          server {
              listen 80;
              server_name server_domain_or_IP;

              location = /favicon.ico { access_log off; log_not_found off; }
              location /static/ {
                  root /home/sammy/myprojectdir;
              }

              location / {
                  include proxy_params;
                  proxy_pass http://unix:/run/gunicorn.sock;
              }
          }
        ii. enable the file by linking it to the sites-enabled directory:
          sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
        iii. make sure to have +x permission:
          sudo chmod +x /home
          sudo chmod +x /home/user_name
          sudo chmod +x /home/user_name/path/to/project/directory
          sudo chmod +x /home/user_name/path/to/project/directory/frontend
        iv. sudo systemctl restart nginx





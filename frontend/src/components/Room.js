import React, { useState, useEffect } from "react";
import { Grid, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import CreateRoomPage from "./CreateRoomPage";
import MusicPlayer from "./MusicPlayer";

function Room({ leaveRoomCallback }) {
  const [guestCanPause, setGuestCanPause] = useState(false);
  const [votesToSkip, setVotesToSkip] = useState(2);
  const [isHost, setIsHost] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [spotifyAuthenticated, setSpotifyAuthenticated] = useState(false);
  const [song, setSong] = useState({});

  const navigate = useNavigate();

  // to access the roomcode from url params
  let roomCode = window.location.href.split("/")[4];

  // to perform the fetch request and update the states when the component mounts.
  useEffect(() => {
    getRoomDetails();
    // To get the current song info after every second.
    const intervalID = setInterval(getCurrentSong, 1000);

    return () => {
      clearInterval(intervalID);
    };
  }, []);

  // Function to get the room details.
  function getRoomDetails() {
    fetch("/api/get-room/" + "?code=" + roomCode)
      .then((response) => {
        if (!response.ok) {
          leaveRoomCallback();
          navigate("/");
        }
        return response.json();
      })
      .then((data) => {
        setVotesToSkip(data.votes_to_skip);
        setGuestCanPause(data.guest_can_pause);
        setIsHost(data.is_host);
        if (data.is_host) {
          autheticateSpotify();
        }
      });
  }

  // To authenticate user on spotify.
  // To send request to backend if the user is authenticated.
  // If not then fetch URl and request spotify to authenticate.
  function autheticateSpotify() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    fetch("/spotify-api/check-update-auth/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        setSpotifyAuthenticated(data.status);
        if (!data.status) {
          fetch("/spotify-api/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });
        }
      });
  }

  // To fetch the current playing song data and set the song state if reponse is okay.
  function getCurrentSong() {
    fetch("/spotify-api/get-current-song/")
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          console.error(error);
        }
      })
      .then((data) => {
        setSong(data);
      });
  }

  const leaveButtonPressed = (event) => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };

    fetch("/api/leave-room/", requestOptions)
      .then((_response) => {
        leaveRoomCallback();
        navigate(`/`);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const updateShowSettings = (value) => {
    setShowSettings(value);
  };

  // To show the settings page by modifying the CreateRoomPage component.
  function renderSettings() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <CreateRoomPage
            update={true}
            defaultVotesToSkip={votesToSkip}
            defaultGuestCanPause={guestCanPause}
            roomCode={roomCode}
            updateCallback={getRoomDetails}
          ></CreateRoomPage>
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            variant="contained"
            color="secondary"
            onClick={() => updateShowSettings(false)}
          >
            Close
          </Button>
        </Grid>
      </Grid>
    );
  }

  // To sender settings button
  function renderSettingsButton() {
    return (
      <Grid item xs={12} align="center">
        <Button
          variant="contained"
          color="primary"
          onClick={() => updateShowSettings(true)}
        >
          Settings
        </Button>
      </Grid>
    );
  }

  // To render settings page if settings page is requested.
  if (showSettings) {
    return renderSettings();
  }
  return (
    <Grid container spacing={1}>
      <MusicPlayer {...song} />
      {isHost ? renderSettingsButton() : null}
      <Grid item xs={12} align="center">
        <Button
          color="secondary"
          variant="contained"
          onClick={leaveButtonPressed}
        >
          Leave Room
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography component="h8" variant="h8">
          Code: {roomCode}
        </Typography>
      </Grid>
    </Grid>
  );
}

export default Room;

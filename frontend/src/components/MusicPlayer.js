import React, { useState, useEffect } from "react";
import {
  Grid,
  Typography,
  Card,
  IconButton,
  LinearProgress,
  Tooltip,
} from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import SkipNextIcon from "@mui/icons-material/SkipNext";
import PauseIcon from "@mui/icons-material/Pause";
import image from "../../static/images/stay-tuned.jpg";

function MusicPlayer(props) {
  const songProgress = (props.song_progress_time / props.duration) * 100;

  // Function to play or pause the song.
  const playOrPauseSong = (playOrPauseRequest) => {
    const requestOptions = {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        play_or_pause_request: playOrPauseRequest,
      }),
    };
    // fetch request.
    fetch("/spotify-api/play-or-pause-song/", requestOptions);
  };

  // Function to skip to the next song.
  const skipToNextSong = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    // fetch request.
    fetch("/spotify-api/skip-to-next-song/", requestOptions);
  };

  if (props.status == 204) {
    return (
      <Card>
        <Grid container alignItems="center">
          <Grid item align="center" xs={4}>
            <img src={image} height="100%" width="100%" />
          </Grid>
          <Grid item align="center" xs={8}>
            <Typography component="h7" variant="h7">
              {props.message}
            </Typography>
          </Grid>
        </Grid>
      </Card>
    );
  } else {
    return (
      <Card>
        <Grid container alignItems="center">
          <Grid item align="center" xs={4}>
            <img src={props.image_url} height="100%" width="100%" />
          </Grid>
          <Grid item align="center" xs={8}>
            <Typography component="h5" variant="h5">
              {props.title}
            </Typography>
            <Typography color="textSecondary" variant="subtitle1">
              {props.artist}
              <div>
                <IconButton
                  onClick={() =>
                    props.is_playing
                      ? playOrPauseSong("pause")
                      : playOrPauseSong("play")
                  }
                >
                  {props.is_playing ? <PauseIcon /> : <PlayArrowIcon />}
                </IconButton>
                <Tooltip title="Votes To Skip">
                  <IconButton>
                    {props.votes} / {props.votes_required}
                  </IconButton>
                </Tooltip>
                <IconButton onClick={() => skipToNextSong()}>
                  {<SkipNextIcon />}
                </IconButton>
              </div>
            </Typography>
          </Grid>
        </Grid>
        <LinearProgress variant="determinate" value={songProgress} />
      </Card>
    );
  }
}

export default MusicPlayer;

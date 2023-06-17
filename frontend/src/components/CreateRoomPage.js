import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import {
  Button,
  Grid,
  Typography,
  TextField,
  FormHelperText,
  FormControl,
  FormControlLabel,
  Radio,
  RadioGroup,
  Collapse,
  Alert,
} from "@mui/material";

export default function CreateRoomPage({
  defaultGuestCanPause = true,
  defaultVotesToSkip = 2,
  update = false,
  roomCode = null,
  updateCallback = () => {},
}) {
  const navigate = useNavigate();
  const [votesToSkip, setVotesToSkip] = useState(defaultVotesToSkip);
  const [guestCanPause, setGuestCanPause] = useState(defaultGuestCanPause);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const handleVotesChange = (event) => {
    setVotesToSkip(event.target.value);
  };

  const handleGuestCanPauseChange = (event) => {
    setGuestCanPause(event.target.value === "true" ? true : false);
  };

  // To send the data to backend by sending the post request for create room.
  const handleCreateRoomButtonPressed = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: votesToSkip,
        guest_can_pause: guestCanPause,
      }),
    };
    // fetch request.
    fetch("/api/create-room/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        navigate(`/room/${data.code}`);
      });
  };

  // To send the data to backend by sending the post request for create room.
  const handleUpdateButtonPressed = () => {
    const requestOptions = {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: votesToSkip,
        guest_can_pause: guestCanPause,
        code: roomCode,
      }),
    };
    // fetch request.
    fetch("/api/update-room/", requestOptions).then((response) => {
      if (response.ok) {
        setSuccessMessage("Room updated successfully!");
      } else {
        setErrorMessage("Error occured...!");
      }
      updateCallback();
    });
  };

  // To render the create and back to home button.
  function renderCreateButtons() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={handleCreateRoomButtonPressed}
          >
            Create a room
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }

  function renderUpdateButtons() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={handleUpdateButtonPressed}
          >
            Update Room
          </Button>
        </Grid>
      </Grid>
    );
  }

  const title = update ? "Update Room" : "Create a room";
  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Collapse in={errorMessage != "" || successMessage != ""}>
          {successMessage != "" ? (
            <Alert
              severity="success"
              onClose={() => {
                setSuccessMessage("");
              }}
            >
              {successMessage}
            </Alert>
          ) : (
            <Alert
              severity="error"
              onClose={() => {
                setErrorMessage("");
              }}
            >
              {errorMessage}
            </Alert>
          )}
        </Collapse>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          {title}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl component="fieldset">
          <FormHelperText>
            <div align="center">Guest Control of Playback State</div>
          </FormHelperText>
          <RadioGroup
            row
            defaultValue={defaultGuestCanPause}
            onChange={handleGuestCanPauseChange}
          >
            <FormControlLabel
              value="true"
              control={<Radio color="primary" />}
              label="Play/Pause"
              labelPlacement="bottom"
            />
            <FormControlLabel
              value="false"
              control={<Radio color="secondary" />}
              label="No Control"
              labelPlacement="bottom"
            />
          </RadioGroup>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl>
          <TextField
            required={true}
            type="number"
            onChange={handleVotesChange}
            defaultValue={defaultVotesToSkip}
            InputProps={{
              min: 1,
              style: { textAlign: "center" },
            }}
          />
          <FormHelperText>
            <div align="center">Votes required to skip the song</div>
          </FormHelperText>
        </FormControl>
      </Grid>
      {update ? renderUpdateButtons() : renderCreateButtons()}
    </Grid>
  );
}

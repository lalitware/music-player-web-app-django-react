import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";

export default class App extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="center">
        <HomePage />
      </div>
    );
  }
}

// To access the app container which is indside templates/frontend/index.html
const appDiv = document.getElementById("app");
render(<App />, appDiv);

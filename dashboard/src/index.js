import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App";

const root = document.getElementById("messages-app");
const jobId = root.dataset.jobId;
const sender = root.dataset.sender;

ReactDOM.render(<App jobId={jobId} sender={sender} />, document.getElementById("messages-app"));
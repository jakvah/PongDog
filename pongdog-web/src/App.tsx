import React from "react";
import "./styles.scss";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LeaderboardPage from "./pages/Leaderboard";
import LivePage from "./pages/Live";
import LogdogPage from "./pages/Logdog";

function App() {
  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route path="live" element={<LivePage />} />
          <Route path="leaderboard" element={<LeaderboardPage />} />
          <Route path="logdog" element={<LogdogPage />} />
          <Route path="/" element={<LeaderboardPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

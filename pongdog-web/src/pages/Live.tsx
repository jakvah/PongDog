import React, { useState } from "react";
import MatchPage from "./Match";
import LeaderboardPage from "./Leaderboard";
import { useInterval } from "../hooks";

const FETCH_INTERVAL_MS = 2000;

export interface MatchStats {
  ongoing: 0 | 1;
  start_time: string;

  player1_elo: number;
  player1_elo_loss: number;
  player1_elo_win: number;
  player1_id: number;
  player1_name: string | -1;
  player1_score: number;

  player2_elo: number;
  player2_elo_loss: number;
  player2_elo_win: number;
  player2_id: number;
  player2_name: string | -1;
  player2_score: number;
}

const LivePage: React.FC = () => {
  const [matchStats, setMatchStats] = useState<MatchStats | null>(null);
  useInterval(async () => {
    const response = await fetch(
      "https://jakvah.pythonanywhere.com/get_complete_match_stats"
    )
      .then((response) => response.json())
      .catch((err) => console.log(err));
    setMatchStats(response);
  }, FETCH_INTERVAL_MS);

  if (matchStats?.ongoing === 1) return <MatchPage matchStats={matchStats} />;
  return <LeaderboardPage />;
};

export default LivePage;

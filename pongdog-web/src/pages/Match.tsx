import React, { useState } from "react";
import { FaHotdog, FaTrashAlt } from "react-icons/fa";
import { useInterval } from "../hooks";

interface MatchStats {
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

const FETCH_INTERVAL_MS = 2000;

interface ParticipantProps {
  elo: number;
  elo_loss: number;
  elo_win: number;
  id: number;
  name: string;
  score: number;
}

const Participant: React.FC<ParticipantProps> = ({
  elo,
  elo_loss,
  elo_win,
  id,
  name,
  score,
}) => {
  return (
    <div className="participant">
      <div className="participant__image">
        <img
          alt="Player"
          src={`https://jakvah.pythonanywhere.com/static/imgs/${id}`}
        />
      </div>
      <h2 className="participant__name">{name}</h2>
      <div className="participant__stat">
        <b>ELO:</b> {elo}
      </div>
      <div className="participant__stat" style={{ color: "var(--clr-green)" }}>
        <b>Win:</b> {elo_win} <FaHotdog />
      </div>
      <div className="participant__stat" style={{ color: "var(--clr-red)" }}>
        <b>Loss: </b> {elo_loss} <FaTrashAlt />
      </div>
      <div className="participant__score">{score}</div>
    </div>
  );
};

const MatchPage: React.FC = () => {
  const [matchStats, setMatchStats] = useState<MatchStats | null>(null);
  useInterval(async () => {
    const response = await fetch(
      "https://jakvah.pythonanywhere.com/get_complete_match_stats"
    )
      .then((response) => response.json())
      .catch((err) => console.log(err));
    setMatchStats(response);
  }, FETCH_INTERVAL_MS);

  const [time, setTime] = useState("");
  useInterval(() => {
    if (!matchStats || matchStats.start_time === "-") return setTime("");

    var diff =
      new Date().getTime() - new Date(matchStats.start_time + "0").getTime();

    const min = Math.floor(diff / 1000 / 60);
    const sec = Math.floor(diff / 1000) - min * 60;
    let time =
      min.toString().padStart(2, "0") + ":" + sec.toString().padStart(2, "0");
    setTime(time);
  }, 1000);

  return (
    <div className="match-page">
      <div className="match-page__header">
        <h1>MATCH ONGOING</h1>
        <h2>{time}</h2>
      </div>
      {matchStats ? (
        <div className="match-page__content">
          <Participant
            elo={matchStats.player1_elo}
            elo_loss={matchStats.player1_elo_loss}
            elo_win={matchStats.player1_elo_win}
            id={matchStats.player1_id}
            name={matchStats.player1_name as string}
            score={matchStats.player1_score}
          />
          <div className="match-page__content__vs">VS</div>
          <Participant
            elo={matchStats.player2_elo}
            elo_loss={matchStats.player2_elo_loss}
            elo_win={matchStats.player2_elo_win}
            id={matchStats.player2_id}
            name={matchStats.player2_name as string}
            score={matchStats.player2_score}
          />
        </div>
      ) : null}
    </div>
  );
};

export default MatchPage;

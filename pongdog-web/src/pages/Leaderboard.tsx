import React, { useEffect, useMemo, useState } from "react";
import { FaFirstAid } from "react-icons/fa";
import { ImSpinner } from "react-icons/im";
import { VscGraphLine } from "react-icons/vsc";

import { useInterval } from "../hooks";

const FETCH_INTERVAL_MS = 30 * 1000;

interface Player {
  id: number;
  name: string;
  rank: number;
  score: number;
  wins: number;
  games_played: number;
}

const PodiumCard: React.FC<{ player: Player; rank: 1 | 2 | 3 }> = ({
  player,
  rank,
}) => {
  const rankText = useMemo(() => {
    switch (rank) {
      case 1:
        return "first";
      case 2:
        return "second";
      case 3:
        return "third";
    }
  }, [rank]);

  const [imgUrl, setImgUrl] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(
        `https://jakvah.pythonanywhere.com/static/imgs/${player.id}`,
        { mode: "no-cors" }
      );
      console.log(response);
      if (!response.ok) {
        setImgUrl("https://jakvah.pythonanywhere.com/static/placeholder.png");
      }
      setImgUrl(`https://jakvah.pythonanywhere.com/static/imgs/${player.id}`);
    };
    fetchData();
  }, [player.id]);

  return (
    <div className={"podium__card podium__card--" + rankText}>
      <div
        className="podium__card__image"
        style={{ backgroundImage: `url('${imgUrl}')` }}
      />
      <div className="podium__card__rank">{rank}.</div>
      <div className="podium__card__name">{player.name}</div>
      <div className="podium__card__stats">
        <div>
          {player.score} <VscGraphLine />
        </div>
        <div>{Math.round(player.wins / player.games_played) * 100}% WR</div>
      </div>
    </div>
  );
};

const Podium: React.FC<{ players: Player[] }> = ({
  players: [first, second, third, ...rest],
}) => {
  return (
    <div className="leaderboard-page__podium">
      <PodiumCard player={second} rank={2} />
      <PodiumCard player={first} rank={1} />
      <PodiumCard player={third} rank={3} />
    </div>
  );
};

const List: React.FC<{ players: Player[] }> = ({ players }) => {
  return (
    <div className="rank-list">
      {players.slice(3, 18).map((player) => (
        <div key={player.id} className="rank-list__item">
          <div
            className="rank-list__item__image"
            style={{
              backgroundImage: `url(https://jakvah.pythonanywhere.com/static/imgs/${player.id})`,
            }}
          />
          <div className="rank-list__item__rank">{player.rank}</div>
          <div className="rank-list__item__title">{player.name}</div>

          <div className="rank-list__item__stats">
            <div>
              <b>ELO:</b> {player.score}
            </div>
            <div>
              <b>WR:</b> {Math.round((player.wins / player.games_played) * 100)}
              %
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

const Leaderboard: React.FC = () => {
  const [players, setPlayers] = useState<Player[]>([]);
  const [isFetched, setIsFetched] = useState(false);
  useInterval(async () => {
    const players: Player[] = await fetch(
      "https://jakvah.pythonanywhere.com/get_pongdog_leaderboard"
    )
      .then((response) => response.json())
      .then((response) => response.scores)
      .catch((err) => console.log(err));

    setPlayers(players);
    setIsFetched(true);
  }, FETCH_INTERVAL_MS);

  return (
    <div className="leaderboard-page">
      <div className="leaderboard-page__content">
        {isFetched ? (
          <>
            <Podium players={players} />
            <List players={players} />
          </>
        ) : (
          <ImSpinner className="icon-spin" size={80} />
        )}
      </div>
    </div>
  );
};

export default Leaderboard;

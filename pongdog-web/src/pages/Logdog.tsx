import React, { useState } from "react";
import { BsCircleFill } from "react-icons/bs";
import { useInterval } from "../hooks";

const SECONDS = 1000;
const MINUTES = 60 * SECONDS;

const RoomCard: React.FC<{ id: number; name: string }> = ({ id, name }) => {
  const [users, setUsers] = useState<Array<{ id: number; name: string }>>([]);
  useInterval(async () => {
    const response = await fetch(
      `https://jakvah.pythonanywhere.com/logdog/rooms/${id}`
    ).then((response) => response.json());
    setUsers(response.data.users);
  }, 10 * SECONDS);
  return (
    <div className="room-card">
      <div className="room-card__header">{name}</div>
      <div className="room-card__content">
        {users.map((user) => (
          <div className="room-card__content__user" key={user.id}>
            <BsCircleFill style={{ color: "green" }} />
            {user.name}
            <div className="room-card__content__user__activity">
              (Last seen: 2h ago)
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const LogdogPage: React.FC = () => {
  const [rooms, setRooms] = useState<Array<{ id: number; name: string }>>([]);
  useInterval(async () => {
    const response = await fetch(
      "https://jakvah.pythonanywhere.com/logdog/rooms"
    ).then((response) => response.json());
    setRooms(response.data);
  }, 2 * MINUTES);
  return (
    <div className="logdog-page">
      <div className="logdog-page__header">LogDog</div>
      <div className="logdog-page__content">
        {rooms.map((room) => (
          <RoomCard key={room.id} id={room.id} name={room.name} />
        ))}
      </div>
    </div>
  );
};

export default LogdogPage;

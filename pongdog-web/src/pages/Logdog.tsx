import React, { useState } from "react";
import { BsCircleFill } from "react-icons/bs";
import ReactTimeAgo from "react-time-ago";
import { useInterval } from "../hooks";
import RegisterDoggerModal from "../modals/RegisterDogger";

const SECONDS = 1000;
const MINUTES = 60 * SECONDS;

interface User {
  id: number;
  name: string;
  lastSeenAt: Date;
}

const UserActivity: React.FC<{ user: User }> = ({ user }) => {
  const [color, setColor] = useState<"green" | "orange" | "red">("green");
  useInterval(() => {
    const diffMs = new Date().getTime() - new Date(user.lastSeenAt).getTime();
    const diffMins = Math.floor(diffMs / 60000);
    if (diffMins < 5) {
      setColor("green");
    } else if (diffMins < 15) {
      setColor("orange");
    } else {
      setColor("red");
    }
  }, 1 * SECONDS);
  return (
    <div className="room-card__content__user" key={user.id}>
      <BsCircleFill style={{ color }} />
      {user.name}
      <div className="room-card__content__user__activity">
        (<ReactTimeAgo date={new Date(user.lastSeenAt)} />)
      </div>
    </div>
  );
};

const RoomCard: React.FC<{
  id: number;
  name: string;
}> = ({ id, name }) => {
  const [users, setUsers] = useState<Array<User>>([]);
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
          <UserActivity key={user.id} user={user} />
        ))}
      </div>
    </div>
  );
};

const LogdogPage: React.FC = () => {
  const [rooms, setRooms] = useState<Array<{ id: number; name: string }>>([]);
  const [modalOpen, setModalOpen] = useState(false);
  useInterval(async () => {
    const response = await fetch(
      "https://jakvah.pythonanywhere.com/logdog/rooms"
    ).then((response) => response.json());
    setRooms(response.data);
  }, 10 * SECONDS);
  return (
    <div className="logdog-page">
      {modalOpen ? (
        <RegisterDoggerModal onClose={() => setModalOpen(false)} />
      ) : (
        ""
      )}
      <div className="logdog-page__header">
        LogDog{" "}
        <button className="button" onClick={() => setModalOpen(true)}>
          Register new Dogger
        </button>
      </div>
      <div className="logdog-page__content">
        {rooms.map((room) => (
          <RoomCard key={room.id} id={room.id} name={room.name} />
        ))}
      </div>
    </div>
  );
};

export default LogdogPage;

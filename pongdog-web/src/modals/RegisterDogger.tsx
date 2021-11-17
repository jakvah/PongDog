import React, { useCallback, useEffect, useState } from "react";

interface RegisterDoggerModalProps {
  onClose?: () => void | null;
}

const RegisterDoggerModal: React.FC<RegisterDoggerModalProps> = ({
  onClose,
}) => {
  const [name, setName] = useState("");
  const [room, setRoom] = useState<number>(1);
  const [macPhone, setMacPhone] = useState("");
  const [macLaptop, setMacLaptop] = useState("");

  const [rooms, setRooms] = useState<Array<{ id: number; name: string }>>([]);
  useEffect(() => {
    fetch("https://jakvah.pythonanywhere.com/logdog/rooms")
      .then((response) => response.json())
      .then((response) => setRooms(response.data));
  }, []);

  const handleSubmit = useCallback(() => {
    fetch();
  }, [name, room, macPhone, macLaptop]);

  return (
    <div
      className="modal"
      onClick={(e) => onClose && e.target === e.currentTarget && onClose()}
    >
      <div className="modal__content">
        <h1>Register new Dogger</h1>
        <form className="form" onSubmit={handleSubmit}>
          <label>Name:</label>
          <input
            type="text"
            placeholder="Enter your name..."
            value={name}
            onInput={(e) => setName(e.currentTarget.value)}
            required
          />
          <label>Reading room:</label>
          <select
            value={room}
            onChange={(e) => setRoom(parseInt(e.currentTarget.value))}
            required
          >
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                {room.name}
              </option>
            ))}
          </select>
          <label>Bluetooth Phone:</label>
          <input
            type="text"
            placeholder="Enter MAC-address..."
            minLength={17}
            maxLength={17}
            value={macPhone}
            onInput={(e) => setMacPhone(e.currentTarget.value)}
            required
          />
          <label>
            Bluetooth Laptop <i>(optional)</i>:
          </label>
          <input
            type="text"
            placeholder="Enter MAC-address..."
            minLength={17}
            maxLength={17}
            value={macLaptop}
            onInput={(e) => setMacLaptop(e.currentTarget.value)}
          />
          <input className="form__submit" type="submit" value="Submit" />
        </form>
      </div>
    </div>
  );
};

export default RegisterDoggerModal;

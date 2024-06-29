import "./App.css";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";

function Home() {
  const navigate = useNavigate();
  const [name, setName] = useState("");

  const handleButtonClick = () => {
    if (name.trim() !== "") {
      navigate("/enter", { state: { name } });
    }
  };
  return (
    <div
      style={{
        backgroundImage: `url(frame5.png)`,
        height: "100vh",
        backgroundSize: "cover",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div className="box"></div>
      <div className="box">
        <h3>Hi! I'm Renee</h3>
        <p>I am your medical help assistant! Let's assess your problem!</p>
        <div className="field">
          <input
            type="text"
            placeholder="Enter your name..."
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <button onClick={handleButtonClick}>Enter</button>
        </div>
      </div>
    </div>
  );
}

export default Home;

import "./App.css";
import React, { useState } from "react";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { useLocation } from "react-router-dom";

const bg_color = "#F4F6FA";

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false); // To handle loading state
  //const [sessionId, setSessionId] = useState("");

  const location = useLocation();
  const name = location.state?.name;

  //   useEffect(() => {
  //     // Generate a unique session ID when the component mounts
  //     setSessionId(Math.random().toString(36).substr(2, 9));
  //   }, []);

  const handleSendMessage = async () => {
    if (inputValue.trim() !== "") {
      const userMessage = inputValue;
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "user", text: userMessage },
      ]);
      setInputValue("");
      setIsLoading(true);

      try {
        const response = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: userMessage }),
        });

        if (response.ok) {
          const data = await response.json();
          setMessages((prevMessages) => [
            ...prevMessages,
            { type: "bot", text: data.response },
          ]);
        } else {
          setMessages((prevMessages) => [
            ...prevMessages,
            { type: "bot", text: "Error: Unable to get response from server." },
          ]);
        }
      } catch (error) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { type: "bot", text: `Error: ${error.message}` },
        ]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <div style={{ position: "sticky", height: "100vh" }}>
      <div
        style={{
          backgroundImage: `url(/frame6.png)`,
          height: "25vh",
          position: "sticky",
        }}
      >
        <div
          className="header"
          style={{
            position: "relative",
            paddingTop: "4%",
            paddingLeft: "12%",
          }}
        >
          <h3>Hi {name}! I'm Renee</h3>
          <p>I am your medical help assistant. Let's assess your problem!</p>
        </div>
      </div>
      <div
        style={{
          position: "relative",
          backgroundColor: bg_color,
          height: "calc(75vh - 2%)",
          paddingTop: "2%",
          paddingLeft: "12%",
          paddingRight: "12%",
          overflow: "auto",
        }}
      >
        <div className="chat-box" style={{ height: "100%", overflowY: "auto" }}>
          <div className="chat-output">
            Hello there, {name}! Please let me know what your symptoms are!
          </div>
          {messages.map((message, index) => (
            <div
              key={index}
              className={message.type === "user" ? "chat-input" : "chat-output"}
            >
              {message.text}
            </div>
          ))}
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          bottom: 20,
          width: "80%",
          left: "10%",
          zIndex: 1,
          display: "flex",
        }}
      >
        <button
          className="upload-button"
          style={{ marginRight: "10px" }}
          onClick={handleRefresh}
          disabled={isLoading}
        >
          <i className="fas fa-sync"></i>
        </button>
        <input
          className="input-field"
          type="text"
          placeholder="Type your message here..."
          style={{ marginLeft: "10px" }}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === "Enter") handleSendMessage();
          }}
          disabled={isLoading}
        />
        <button
          className="send-button"
          style={{ marginLeft: "10px" }}
          onClick={handleSendMessage}
          disabled={isLoading}
        >
          <i className="fas fa-chevron-right"></i>
        </button>
      </div>
      <img
        src="/frame3.png"
        style={{
          position: "absolute",
          top: 60,
          right: 200,
          width: "25vh",
          height: "25vh",
          zIndex: 1,
        }}
      />
    </div>
  );
}

export default ChatPage;

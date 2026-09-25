/*
  MessageBubble.jsx — Displays ONE chat message.

  Props:
    message: { role: "user" | "bot", text: string }

  - User messages appear on the RIGHT with a blue background.
  - Bot messages appear on the LEFT with a grey background.
*/
import React from "react";

export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  // Outer wrapper controls LEFT vs RIGHT alignment
  const wrapperStyle = {
    display: "flex",
    justifyContent: isUser ? "flex-end" : "flex-start",
    marginBottom: "12px",
  };

  // The coloured bubble
  const bubbleStyle = {
    maxWidth: "70%",
    padding: "10px 14px",
    borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
    backgroundColor: isUser ? "#2563eb" : "#374151",
    color: "#fff",
    fontSize: "14px",
    lineHeight: "1.5",
    whiteSpace: "pre-wrap",   // preserve newlines from the bot's answer
    wordBreak: "break-word",
  };

  return (
    <div style={wrapperStyle}>
      <div style={bubbleStyle}>
        {message.text}
      </div>
    </div>
  );
}

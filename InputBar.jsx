/*
  InputBar.jsx — Text input + Send button at the bottom of the chat.

  Props:
    onSend:    function(text) — called when the user submits a message
    disabled:  boolean       — true while waiting for a bot reply
*/
import React, { useState } from "react";

export default function InputBar({ onSend, disabled }) {
  const [text, setText] = useState("");

  // Called when the user clicks Send OR presses Enter (without Shift)
  function handleSubmit(e) {
    e.preventDefault();
    if (!text.trim() || disabled) return;
    onSend(text.trim());
    setText("");   // clear the input after sending
  }

  const formStyle = {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    padding: "12px 16px",
    borderTop: "1px solid #374151",
    backgroundColor: "#1f2937",
  };

  const inputStyle = {
    flex: 1,
    padding: "10px 14px",
    borderRadius: "8px",
    border: "1px solid #374151",
    backgroundColor: "#111827",
    color: "#f9fafb",
    fontSize: "14px",
    outline: "none",
  };

  const buttonStyle = {
    padding: "10px 20px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: disabled ? "#374151" : "#2563eb",
    color: disabled ? "#6b7280" : "#fff",
    fontSize: "14px",
    fontWeight: "600",
    cursor: disabled ? "not-allowed" : "pointer",
    transition: "background-color 0.2s",
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <input
        style={inputStyle}
        type="text"
        placeholder={disabled ? "Waiting for response…" : "Type a message…"}
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={disabled}
        // Allow Shift+Enter for newlines; plain Enter = submit
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) handleSubmit(e);
        }}
      />
      <button style={buttonStyle} type="submit" disabled={disabled}>
        Send
      </button>
    </form>
  );
}
